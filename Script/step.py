import os
import json
import re

def remove_ansi(text):
    """移除控制台 ANSI 颜色控制字符"""
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

def count_reproduction_after_adaptation(log_text: str, cve_id: str, version: str) -> int:
    # 只从包含目标 version 的 Start adapting 行之后开始统计
    start_marker = "[Adapter] Start adapting exploit from"
    exec_pattern = f"[Executor] Executing exploit for {cve_id} on version {version}..."

    lines = log_text.splitlines()
    start_index = None

    for i, line in enumerate(lines):
        if start_marker in line and version in line:
            start_index = i
            break

    if start_index is None:
        return 0

    # 只统计 adaptation 后的内容
    cropped_lines = lines[start_index:]
    cropped_log = "\n".join(cropped_lines)
    count = cropped_log.count(exec_pattern)

    return max(0, count - 1)

def get_log_count(group_name, cve_id, version):
    log_path = os.path.join("result", group_name, "log", f"{cve_id}.txt")
    if not os.path.exists(log_path):
        return 0
    with open(log_path, 'r') as f:
        log_content = remove_ansi(f.read())  # 这里加上 remove_ansi
    return count_reproduction_after_adaptation(log_content, cve_id, version)


def is_version_migrated(result_data, cve_id, version, group_name):
    if cve_id not in result_data:
        return False
    cve_entry = result_data[cve_id]
    group_json_key_map = {
        "Diffploit-Causing": "diffploit-causing",
        "Diffploit-Supporting": "diffploit-supporting",
        "Diffploit-Annealing": "diffploit-annealing",
    }
    json_key = group_json_key_map.get(group_name, group_name.lower())
    if json_key not in cve_entry:
        return False
    intervals = cve_entry[json_key].get("intervals", {})
    return version in intervals and intervals[version] > 0


def main():
    json_path = "/PoCAdaptation/script/batch.json"
    output_path = "/PoCAdaptation/result/abalation_step.txt"
    result_json_path = "/PoCAdaptation/result/abalation.json"
    with open(json_path, 'r') as jf:
        targets = json.load(jf)

    
    with open(result_json_path, 'r') as rf:
        result_data = json.load(rf)

    group_order = [
        "Diffploit",
        "Diffploit-Causing",
        "Diffploit-Supporting",
        "Diffploit-Annealing"
    ]

    
    with open(output_path, 'w') as out:
        for entry in targets:
            cve_id = entry["cve_id"]
            version = entry["version"]
            row = []
            for group in group_order:
                if group == "Diffploit":
                    count = get_log_count(group, cve_id, version)
                elif not is_version_migrated(result_data, cve_id, version, group):
                    count = 999
                else:
                    count = get_log_count(group, cve_id, version)
                row.append(str(count))
            out.write("\t".join(row) + "\n")


if __name__ == "__main__":
    main()
