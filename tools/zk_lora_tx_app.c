/*
 * zk_lora_tx_app.c — ZK-LoRa deterministic file payload transmitter (RakMiner-A).
 * HAL API: sx1302_hal v2.1.0 (lgw_txgain_setconf(rf_chain, lut), lgw_status(chain,select,code)).
 *
 * Sends a file's bytes as repeated LoRa frames (max 255 B/frame) at M1 RF params:
 * 903.9 MHz, SF9, BW 125 kHz, 14 dBm, RF chain 0, SX1250 single input.
 * Evidence contract: prints A_LORA_TX_FILE_SEND_COMPLETE=YES only if every
 * scheduled send reached TX_FINISHED via lgw_status(TX_STATUS).
 *
 * Build (from libloragw/): gcc -O2 -o tst/zk_lora_tx_app tst/zk_lora_tx_app.c -Iinc -I../libtools/inc -L. -lloragw -lm -ltinymt32 -lrt
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include "loragw_hal.h"

#define SPI_DEV_DEFAULT "/dev/spidev0.0"
#define MAX_FRAME 255

static void usage(void) {
    printf("zk_lora_tx_app — ZK-LoRa deterministic file transmitter (sx1302_hal v2.1.0 API)\n");
    printf("  -f <float>  TX frequency MHz (default 903.9)\n");
    printf("  -s <uint>   SF (default 9)\n");
    printf("  -b <uint>   BW kHz (default 125)\n");
    printf("  -p <int>    power dBm (default 14)\n");
    printf("  -n <uint>   number of sends of the frame (default 5)\n");
    printf("  -i <path>   input payload file (required)\n");
    printf("  -d <path>   SPI device (default %s)\n", SPI_DEV_DEFAULT);
}

int main(int argc, char **argv) {
    const char *com_path = SPI_DEV_DEFAULT;
    const char *file_path = NULL;
    double freq_mhz = 903.9;
    unsigned sf = 9, bw_khz = 125, nb_send = 5;
    int rf_power = 14;
    int opt;

    while ((opt = getopt(argc, argv, "f:s:b:p:n:i:d:h")) != -1) {
        switch (opt) {
            case 'f': freq_mhz = atof(optarg); break;
            case 's': sf = atoi(optarg); break;
            case 'b': bw_khz = atoi(optarg); break;
            case 'p': rf_power = atoi(optarg); break;
            case 'n': nb_send = atoi(optarg); break;
            case 'i': file_path = optarg; break;
            case 'd': com_path = optarg; break;
            default: usage(); return (opt == 'h') ? 0 : 1;
        }
    }
    if (!file_path) { fprintf(stderr, "ERROR: -i <payload file> required\n"); usage(); return 1; }

    /* Read payload file (one frame, max 255 bytes) */
    FILE *fp = fopen(file_path, "rb");
    if (!fp) { perror("fopen"); return 1; }
    uint8_t frame[MAX_FRAME];
    size_t n = fread(frame, 1, MAX_FRAME, fp);
    int ferr = ferror(fp);
    fclose(fp);
    if (ferr || n == 0) { fprintf(stderr, "ERROR: reading payload file (%s)\n", file_path); return 1; }

    printf("zk_lora_tx_app: payload=%s bytes=%zu freq=%.1fMHz SF%u BW%ukHz %ddBm sends=%u\n",
           file_path, n, freq_mhz, sf, bw_khz, rf_power, nb_send);

    /* Board + radio configuration — mirrors test_loragw_hal_tx M1 defaults */
    struct lgw_conf_board_s board;
    memset(&board, 0, sizeof board);
    board.lorawan_public = true;
    board.clksrc = 0;
    board.com_type = LGW_COM_SPI;
    snprintf(board.com_path, sizeof board.com_path, "%s", com_path);

    struct lgw_conf_rxrf_s rfconf;
    memset(&rfconf, 0, sizeof rfconf);
    rfconf.enable = true;
    rfconf.freq_hz = (uint32_t)(freq_mhz * 1e6);
    rfconf.tx_enable = true;
    rfconf.type = LGW_RADIO_TYPE_SX1250;
    rfconf.single_input_mode = true; /* -j equivalent */

    struct lgw_conf_rxrf_s rfconf2;
    memset(&rfconf2, 0, sizeof rfconf2); /* radio B off */
    rfconf2.enable = false;

    struct lgw_tx_gain_lut_s txlut;
    memset(&txlut, 0, sizeof txlut);
    txlut.size = 1;
    txlut.lut[0].rf_power = (int8_t)rf_power;
    txlut.lut[0].pa_gain = 1;
    txlut.lut[0].mix_gain = 5; /* stock tool's workaround: HAL validates mix_gain [5..15] even for SX1250 */
    txlut.lut[0].pwr_idx = 12; /* --pwid 12 of the M1 TX command line */

    if (lgw_board_setconf(&board) != LGW_HAL_SUCCESS) { fprintf(stderr, "ERROR: board_setconf\n"); return 1; }
    if (lgw_rxrf_setconf(0, &rfconf) != LGW_HAL_SUCCESS) { fprintf(stderr, "ERROR: rxrf_setconf(0)\n"); return 1; }
    if (lgw_rxrf_setconf(1, &rfconf2) != LGW_HAL_SUCCESS) { fprintf(stderr, "ERROR: rxrf_setconf(1)\n"); return 1; }
    if (lgw_txgain_setconf(0, &txlut) != LGW_HAL_SUCCESS) { fprintf(stderr, "ERROR: txgain_setconf\n"); return 1; }

    /* Board reset immediately before lgw_start — stock tool parity (reset_lgw.sh in CWD) */
    if (system("./reset_lgw.sh start") != 0) {
        fprintf(stderr, "ERROR: failed to reset SX1302 (reset_lgw.sh start)\n");
        return 1;
    }

    if (lgw_start() != LGW_HAL_SUCCESS) { fprintf(stderr, "ERROR: lgw_start\n"); return 1; }

    struct lgw_pkt_tx_s pkt;
    memset(&pkt, 0, sizeof pkt);
    pkt.freq_hz = (uint32_t)(freq_mhz * 1e6);
    pkt.tx_mode = IMMEDIATE;
    pkt.rf_chain = 0;
    pkt.rf_power = (int8_t)rf_power;
    pkt.modulation = MOD_LORA;
    pkt.bandwidth = BW_125KHZ; /* HAL expects a BW enum index, not kHz (stock tool parity) */
    pkt.datarate = sf;
    pkt.coderate = 1; /* CR 4/5 — matches stock tool's CR 1 */
    pkt.preamble = 8;
    pkt.invert_pol = false;
    pkt.size = n;
    memcpy(pkt.payload, frame, n);

    unsigned sent_ok = 0;
    for (unsigned i = 0; i < nb_send; i++) {
        int r = lgw_send(&pkt);
        if (r != LGW_HAL_SUCCESS) {
            printf("A_LORA_TX_FILE_SEND_%u_STATUS=SEND_FAIL\n", i + 1);
            continue;
        }
        /* Poll TX_STATUS until the modem returns to TX_FREE (stock tool's loop) */
        uint8_t code = TX_STATUS_UNKNOWN;
        int spins = 0;
        do {
            usleep(5000);
            r = lgw_status(0, TX_STATUS, &code);
            spins++;
        } while (r == LGW_HAL_SUCCESS && code != TX_FREE && spins < 4000);
        if (r == LGW_HAL_SUCCESS && code == TX_FREE) {
            sent_ok++;
            printf("A_LORA_TX_FILE_SEND_%u_STATUS=TX_DONE\n", i + 1);
        } else {
            printf("A_LORA_TX_FILE_SEND_%u_STATUS=TX_ERROR(code=%u)\n", i + 1, code);
        }
        sleep(1);
    }

    lgw_stop();

    if (sent_ok == nb_send) {
        printf("A_LORA_TX_FILE_SEND_COMPLETE=YES (%u/%u sends, %zu bytes)\n", sent_ok, nb_send, n);
        return 0;
    }
    printf("A_LORA_TX_FILE_SEND_COMPLETE=NO (%u/%u)\n", sent_ok, nb_send);
    return 1;
}
