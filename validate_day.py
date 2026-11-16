#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

def validate(day_num, filepath):
    path = Path(filepath)
    if not path.exists():
        print(f"Error: {filepath} does not exist")
        return False

    content = path.read_text(encoding="utf-8")
    
    json_file = "phase5_topics.json"
    if 61 <= day_num <= 75:
        json_file = "phase6_topics.json"
    elif 76 <= day_num <= 90:
        json_file = "phase7_topics.json"
    elif 91 <= day_num <= 135:
        json_file = "phase8_topics.json"
    
    with open(json_file, "r", encoding="utf-8") as f:
        days_data = json.load(f)

    target_day = None
    for d in days_data:
        if f"Day {day_num}:" in d["day_title"]:
            target_day = d
            break

    if not target_day:
        print(f"Error: Day {day_num} not found in phase5_topics.json")
        return False

    expected_topics = target_day["topics"]
    expected_count = len(expected_topics)

    open_details = len(re.findall(r'<details class="t">', content))
    close_details = len(re.findall(r'</details>', content))
    open_pre = len(re.findall(r'<pre>', content))
    close_pre = len(re.findall(r'</pre>', content))

    errors = []
    if open_details != expected_count:
        errors.append(f"Details count mismatch: got {open_details}, expected {expected_count}")
    if open_details != close_details:
        errors.append(f"Mismatched details tags: {open_details} open vs {close_details} close")
    if open_pre != close_pre:
        errors.append(f"Mismatched pre tags: {open_pre} open vs {close_pre} close")

    # Check that day heading exists
    if f"Day {day_num}:" not in content:
        errors.append(f"Day heading for Day {day_num} not found")

    if errors:
        print(f"Validation FAILED for Day {day_num}:")
        for e in errors:
            print(f"  - {e}")
        return False

    print(f"Validation PASSED for Day {day_num} ({open_details}/{expected_count} topics valid)")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 validate_day.py <day_num> <filepath>")
        sys.exit(1)
    day = int(sys.argv[1])
    fpath = sys.argv[2]
    if not validate(day, fpath):
        sys.exit(1)
