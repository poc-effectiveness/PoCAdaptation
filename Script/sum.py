import json
from collections import defaultdict

# 读取 JSON 文件
with open('/PoCAdaptation/result/abalation.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 用来累加每个变体的总数
variant_totals = defaultdict(int)

# 遍历每个 CVE 和其内部各变体的 total 字段
for cve, variants in data.items():
    for variant_name, variant_info in variants.items():
        variant_totals[variant_name] += variant_info.get('total', 0)

# 输出每个变体的最终数量
for variant, total in variant_totals.items():
    print(f"{variant}: {total}")
