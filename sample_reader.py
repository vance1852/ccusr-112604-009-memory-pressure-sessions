"""读取运维演练采集的合成资料。"""

import argparse
import json
from pathlib import Path


def load_inventory(root):
    with (root / "inventory.json").open(encoding="utf-8") as source:
        inventory = json.load(source)
    if not isinstance(inventory, dict) or not inventory:
        raise ValueError("清册应为非空对象")
    return inventory


def load_timeline(path):
    previous = 0
    with path.open(encoding="utf-8") as source:
        for number, line in enumerate(source, start=1):
            try:
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise ValueError("事件应为对象")
                if type(record.get("at")) is not int or record["at"] < previous:
                    raise ValueError("接收时刻应为顺序排列的非负整数")
                kind = record.get("kind")
                if not isinstance(kind, str) or not kind:
                    raise ValueError("缺少事件类别")
            except ValueError as error:
                raise ValueError(f"{path.name}:{number} {error}") from error
            previous = record["at"]
            yield record


def main():
    parser = argparse.ArgumentParser(description="浏览演练资料")
    parser.add_argument("timeline", type=Path, help="演练事件文件")
    parser.add_argument("--kind", help="按事件类别查看")
    args = parser.parse_args()
    try:
        load_inventory(args.timeline.parent)
        for record in load_timeline(args.timeline):
            if args.kind is None or record["kind"] == args.kind:
                print(json.dumps(record, ensure_ascii=False))
    except (OSError, ValueError) as error:
        parser.exit(2, f"无法读取演练资料：{error}\n")


if __name__ == "__main__":
    main()
