#!/usr/bin/env python3
"""
ZK-LoRa Multi-Language Proof Suite Validator
Watermark: ip zymatica.space | astronautshe.com
Copyright (c) 2026 Zymatica. Licensed under Apache License 2.0.

Automates, builds, and verifies equivalent cryptographic proofs in 6 runtimes:
Python, TypeScript, Rust, Java, PowerShell, and Bash.
"""

import os
import sys
import time
import subprocess
from pathlib import Path

# ANSI colors
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'
    GOLD = '\033[38;2;243;179;0m'

# Override colors if not terminal
if not sys.stdout.isatty():
    for attr in dir(Colors):
        if not attr.startswith('__') and isinstance(getattr(Colors, attr), str):
            setattr(Colors, attr, '')

def run_command(cmd, cwd, env=None):
    start = time.time()
    try:
        res = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, shell=True)
        elapsed = time.time() - start
        return res.returncode == 0, res.stdout, res.stderr, elapsed
    except Exception as e:
        elapsed = time.time() - start
        return False, "", str(e), elapsed

def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
    print("=" * 80)
    print(f"{Colors.GOLD}🛡️  ZYMATICA | ZK-LoRa Multi-Language Proof Suite Orchestrator & Verifier{Colors.END}")
    print("=" * 80)
    print()

    base_dir = Path(__file__).parent.resolve()
    downloads_cargo = Path("C:/Users/DannyB/Downloads/Cargo.toml")
    downloads_cargo_tmp = Path("C:/Users/DannyB/Downloads/Cargo.toml.tmp")

    # 1. Handle Cargo.toml shadowing issue in Downloads folder
    cargo_renamed = False
    if downloads_cargo.exists():
        try:
            if downloads_cargo_tmp.exists():
                downloads_cargo_tmp.unlink()
            downloads_cargo.rename(downloads_cargo_tmp)
            cargo_renamed = True
            print(f"{Colors.YELLOW}⚠️  Temporarily renamed parent Cargo.toml to prevent shadowing...{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}❌ Failed to rename parent Cargo.toml: {e}{Colors.END}")

    # Set Python IO encoding env variable
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # Define runtimes to test
    runtimes = {
        "Python": {
            "cmd": "python Multi_Language_Proofs/python/proof.py",
            "cwd": base_dir,
            "desc": "Interpreted proof validation"
        },
        "TypeScript": {
            "cmd": "npx tsx Multi_Language_Proofs/typescript/proof.ts",
            "cwd": base_dir,
            "desc": "Compiled ES Module runtime verification"
        },
        "Rust": {
            "cmd": "cargo run --manifest-path Multi_Language_Proofs/rust/Cargo.toml --quiet",
            "cwd": base_dir,
            "desc": "Native compiled systems verification"
        },
        "Java": {
            "cmd": "java Multi_Language_Proofs/java/Proof.java",
            "cwd": base_dir,
            "desc": "JVM single-source file verification"
        },
        "PowerShell": {
            "cmd": "powershell -File Multi_Language_Proofs/powershell/proof.ps1",
            "cwd": base_dir,
            "desc": "Windows shell native script validation"
        },
        "Bash": {
            "cmd": 'wsl bash -c "cd Multi_Language_Proofs/bash && ./proof.sh"',
            "cwd": base_dir,
            "desc": "Linux shell script validation via WSL"
        }
    }

    results = []
    has_failures = False

    for name, config in runtimes.items():
        print(f"🚀 Running {Colors.BOLD}{name}{Colors.END} verification proof ({config['desc']})...")
        success, stdout, stderr, elapsed = run_command(config["cmd"], config["cwd"], env)
        
        status_str = f"{Colors.GREEN}✅ PASS{Colors.END}" if success else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"   Status: {status_str} (took {elapsed:.2f}s)")
        if not success:
            print(f"   Error: {Colors.RED}{stderr.strip()}{Colors.END}")
            has_failures = True
        print()

        results.append({
            "name": name,
            "success": success,
            "elapsed": elapsed,
            "stdout": stdout,
            "stderr": stderr
        })

    # 2. Restore Cargo.toml shadowing
    if cargo_renamed and downloads_cargo_tmp.exists():
        try:
            if downloads_cargo.exists():
                downloads_cargo.unlink()
            downloads_cargo_tmp.rename(downloads_cargo)
            print(f"{Colors.YELLOW}🔄 Restored parent Cargo.toml successfully.{Colors.END}\n")
        except Exception as e:
            print(f"{Colors.RED}❌ Failed to restore parent Cargo.toml: {e}{Colors.END}\n")

    # 3. Generate Markdown Verification Report
    report_path = base_dir / "VERIFICATION_REPORT.md"
    report_content = f"""# ZK-LoRa: Multi-Language Proof Suite Verification Report 📋

> **Watermark:** ip zymatica.space | astronautshe.com  
> **Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}  
> **Status:** {"✅ ALL RUNTIMES PASSING" if not has_failures else "❌ SOME RUNTIMES FAILING"}

This report summarizes the verification run and execution logs for the equivalent zero-knowledge and cryptographic routing proof implementations across multiple runtimes.

---

## 📊 Summary Table

| Runtime | Status | Time (s) | Description |
| :--- | :---: | :---: | :--- |
"""
    for name, config in runtimes.items():
        res = next(r for r in results if r["name"] == name)
        status = "✅ PASS" if res["success"] else "❌ FAIL"
        report_content += f"| {name} | {status} | {res['elapsed']:.2f}s | {config['desc']} |\n"

    report_content += """
---

## 📝 Execution Logs

"""
    for res in results:
        status_txt = "SUCCESS" if res["success"] else "FAILURE"
        report_content += f"### 🔍 {res['name']} ({status_txt})\n\n"
        if res["success"]:
            report_content += f"```text\n{res['stdout'].strip()}\n```\n\n"
        else:
            report_content += f"```text\nError:\n{res['stderr'].strip()}\nOutput:\n{res['stdout'].strip()}\n```\n\n"

    report_path.write_text(report_content, encoding="utf-8")
    print(f"📝 Verification report written to: {report_path.name}")
    print()

    print("=" * 80)
    if not has_failures:
        print(f"{Colors.GREEN}🎉 SUCCESS: All {len(runtimes)} active language runtimes passed verification!{Colors.END}")
    else:
        print(f"{Colors.RED}❌ FAILURE: Some runtimes failed verification checks.{Colors.END}")
    print("=" * 80)

if __name__ == "__main__":
    main()
