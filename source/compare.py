

from collections import Counter

def compare_with_lists(gold_lines, new_lines):
    return [f'Gold: {line}' for line in gold_lines if line not in new_lines] + \
           [f'New: {line}' for line in new_lines if line not in gold_lines]

def compare_with_counters(gold_lines, new_lines):
    gold_count = Counter(gold_lines)
    new_count = Counter(new_lines)
    differences = []

    all_lines = set(gold_count) | set(new_count)
    for line in all_lines:
        diff = gold_count[line] - new_count[line]
        if diff > 0:
            differences.extend([f'Gold: {line}'] * diff)
        elif diff < 0:
            differences.extend([f'New: {line}'] * (-diff))
    differences.sort()
    return differences

def compare_with_counters_only(gold_lines, new_lines):
    gold_count = Counter(gold_lines)
    new_count = Counter(new_lines)
    differences = []

    gold_diff = gold_count - new_count
    new_diff = new_count - gold_count

    for gold_line, g_count in gold_diff.items():
        differences.extend([f'Gold: {gold_line}'] * g_count)

    for new_line, n_count in new_diff.items():
        differences.extend([f'New: {new_line}'] * n_count)

    return differences
