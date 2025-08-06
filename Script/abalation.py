import os
import shutil
import subprocess
from pathlib import Path
from typing import Callable
from typing import Dict
import argparse
from typing import List
import json


def prompt_and_clear(path: Path, description: str):
    if path.exists() and any(path.iterdir()):
        # response = input(f"[Prompt] Directory '{path}' ({description}) is not empty. Clear it? (yes/no): ").strip().lower()
        response = "yes"
        if response == "yes":
            for item in path.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            print(f"[Cleaner] ✓ Cleared: {path}")
        else:
            print(f"[Abort] ✗ User aborted at step: {description}")
            exit(0)

def run_python_module(script_path: Path, cve_id: str, log_file: Path, version: str = None):
    print(f"[Executor] ▶ Running {script_path.name} for {cve_id}...")
    with open(log_file, 'a') as f:
        process = subprocess.Popen(
            ["python", "-u", str(script_path), cve_id, version],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        for line in process.stdout:
            print(line, end='')  # 实时打印
            f.write(line)
    process.wait()
    print(f"[Executor] ✓ Finished. Log saved to {log_file}")
    return process.returncode


def move_directory(source_root: Path, target_root: Path):
    target_root.mkdir(parents=True, exist_ok=True)

    if not source_root.exists():
        print(f"[Mover] ✗ Source path does not exist: {source_root}")
        return

    for item in source_root.iterdir():
        target_path = target_root / item.name
        shutil.move(str(item), str(target_path))
        print(f"[Mover] ✓ Moved {item} to {target_path} [valid]")

def run_generic_module(cve_id: str, script_path: Path, subfolder: str, versions: List[str] = None):
    valid_path = Path(f"/PoCAdaptation/exploit/valid/{cve_id}")
    result_path = Path(f"/PoCAdaptation/exploit/result/{cve_id}")
    
    
    result_txt = Path(f"/PoCAdaptation/result/{subfolder}/log/{cve_id}.txt")
    with result_txt.open("w", encoding="utf-8") as f:
        f.write(f"Running {script_path.name} for CVE: {cve_id}\n")
        f.write(f"Versions: {', '.join(versions) if versions else 'All'}\n\n")
        
    prompt_and_clear(valid_path, f"Valid Exploit for {subfolder}")
    prompt_and_clear(result_path, f"Result Exploit for {subfolder}")

    results = {}

    for version in versions:
        ret_code = run_python_module(script_path, cve_id, result_txt, version)
        results[version] = ret_code

    target_valid_path = Path(f"/PoCAdaptation/result/{subfolder}/valid/{cve_id}")
    target_result_path = Path(f"/PoCAdaptation/result/{subfolder}/result/{cve_id}")

    prompt_and_clear(target_valid_path, f"Target Valid Exploit for {subfolder}")
    prompt_and_clear(target_result_path, f"Target Result Exploit for {subfolder}")

    move_directory(valid_path, target_valid_path)
    move_directory(result_path, target_result_path)

    lines = []
    lines.append("\n[Executor] ▶ Summary of return codes:")

    print("\n[Executor] ▶ Summary of return codes:")
    for version, code in results.items():
        status = "✓ Success" if code == 0 else "✗ Failed"
        print(f"  - Version {version}: {status} (exit code {code})")
        line = f"  - Version {version}: {status} (exit code {code})"
        lines.append(line)

    with result_txt.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    tmp_json = Path("/PoCAdaptation/script/tmp.json")
    tmp_json.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "cve": cve_id,
        "subfolder": subfolder,
        "results": {
            version: {
                "exit_code": code,
                "status": "success" if code == 0 else "failed"
            }
            for version, code in results.items()
        }
    }

    with tmp_json.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)



MODULES: Dict[str, dict] = {
    "diffploit": {
        "script": Path("/PoCAdaptation/Diffploit/main_process.py"),
        "subfolder": "Diffploit"
    },
    "diffploit-causing": {
        "script": Path("/PoCAdaptation/Abalation/Diffploit-Causing/main_process.py"),
        "subfolder": "Diffploit-Causing"
    },
    "diffploit-supporting": {
        "script": Path("/PoCAdaptation/Abalation/Diffploit-Supporting/main_process.py"),
        "subfolder": "Diffploit-Supporting"
    },
    "diffploit-annealing": {
        "script": Path("/PoCAdaptation/Abalation/Diffploit-Annealing/main_process.py"),
        "subfolder": "Diffploit-Annealing"
    },
    "diffploit-deepseek-only": {
        "script": Path("/PoCAdaptation/Abalation/Diffploit-Deepseek-only/main_process.py"),
        "subfolder": "Diffploit-Deepseek-only"
    },
    "diffploit-chatgpt-only": {
        "script": Path("/PoCAdaptation/Abalation/Diffploit-ChatGPT-only/main_process.py"),
        "subfolder": "Diffploit-ChatGPT-only"
    },
}

def main():
    parser = argparse.ArgumentParser(description="Run PoCAdaptation modules")
    parser.add_argument("--cve", required=True, help="CVE ID, e.g. CVE-2024-1234")
    parser.add_argument("--module", required=True, choices=MODULES.keys(), help="Module to run")
    parser.add_argument("--versions", nargs='+', help="List of versions separated by spaces, e.g. 1.0 1.1 2.0")
    args = parser.parse_args()

    cve_id = args.cve
    module_name = args.module
    config = MODULES[module_name]
    versions = args.versions   

    print(f"[Runner] ▶ Executing module '{module_name}' for {cve_id}...\n")
    run_generic_module(cve_id, config["script"], config["subfolder"],versions)
    print(f"\n[Runner] ✓ Module '{module_name}' completed.")



if __name__ == "__main__":
    main()

