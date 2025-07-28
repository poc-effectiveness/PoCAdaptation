import subprocess
import json
from pathlib import Path
from typing import List

MODULE_LIST = [
    "diffploit"
    "diffploit-causing",
    "diffploit-supporting",
    "diffploit-annealing",
    "diffploit-deepseek-only",
    "diffploit-chatgpt-only",
]

TMP_JSON = Path("/PoCAdaptation/script/tmp.json")


import json
from pathlib import Path

def write_ablation_summary(cve_id: str, module_name: str, interval_counts: dict, total_sum: int):
    result_path = Path("/PoCAdaptation/result/abalation.json")
    
    if result_path.exists():
        with result_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    if cve_id not in data:
        data[cve_id] = {}

    data[cve_id][module_name] = {
        "intervals": interval_counts,
        "total": total_sum
    }

    with result_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[Writer] ✓ Wrote ablation summary to {result_path}")




def run_diffploit_batch(cve_id: str, versions: List[str], version_counts):
    for module_name in MODULE_LIST:
        print(f"\n[BatchRunner] ▶ Running module: {module_name}")
        # 构造命令
        command = [
            "python", "/PoCAdaptation/script/abalation.py",
            "--cve", cve_id,
            "--module", module_name,
            "--versions", *versions
        ]

        # 执行命令
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[BatchRunner] ✗ Module {module_name} failed with return code {e.returncode}")
            continue

        # 读取 tmp.json
                
        sum = 0
        if TMP_JSON.exists():
            print(f"[BatchRunner] ✓ Output from {TMP_JSON}:")
            try:
                with TMP_JSON.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    interval_counts = {}
                    for version, result in data.get("results", {}).items():
                        status = result.get("status", "unknown")
                        code = result.get("exit_code", "N/A")
                        print(f"Version {version}: {status} (exit code {code})")


                        if code != 0:
                            interval_count = 0
                        else :
                            interval_count = version_counts.get((cve_id, version), 0)

                        print(f"Number: {interval_count}")
                        sum = sum + int(interval_count)
                        interval_counts[version] = interval_count
                    
                    print(f"Total number of versions in the {module_name}: {sum}")
                    write_ablation_summary(cve_id, module_name, interval_counts, sum)

            except Exception as e:
                print(f"[BatchRunner] ✗ Failed to parse JSON: {e}")
        else:
            print("[BatchRunner] ✗ tmp.json not found")


import json
from collections import defaultdict

def load_batch_jobs_from_json(file_path):
    batch_jobs = defaultdict(list)
    version_counts = {}

    with open(file_path, 'r') as f:
        data = json.load(f)

    for item in data:
        cve_id = item["cve_id"]
        version = item["version"]
        count = int(item["count"])
        
        batch_jobs[cve_id].append(version)
        version_counts[(cve_id, version)] = count

    return dict(batch_jobs), version_counts


if __name__ == "__main__":

    batch_jobs, version_counts = load_batch_jobs_from_json("/PoCAdaptation/script/batch.json")

    for cve_id, versions in batch_jobs.items():
        print(f"\n[BatchRunner] ▶ Processing CVE: {cve_id} with versions: {', '.join(versions)}")
        run_diffploit_batch(cve_id, versions, version_counts)
