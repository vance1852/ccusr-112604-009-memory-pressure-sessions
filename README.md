# 会议运行节点的内存压迫处置与会话接续

这里保存一套可脱机使用的合成运维资料。两个事件文件各自从相同清册开始，模拟两次独立运行。

## 清册和事件

`samples/inventory.json` 记录演练开始时已知的资源、对象与约定。限制、观察和估算均为 MiB。容量要同时考虑进程和所在 rack。mode 指能从一类检查点继续运行的进程能力。会话对可选输出的同意由 optional_tracks 表示，段编号在每条轨道上独立递增。

`samples/shift-log.jsonl` 和 `samples/recovery-burst.jsonl` 每行是一个 JSON 对象。通用字段 `at` 是资料到达值班侧的演练秒，`kind` 标明来源记录的类型。同一秒内保持给定文件顺序。事实发生时间由记录自身字段提供。pressure 可在 rack 或 node 范围给出有时效的观察。progress 表示接收端实际看到的轨及段。move 是迁移请求，moved 表示已接收的检查点，moved 后源机也可能有最后的 progress；disposition 包含从接收者实际观察到的资源效果。

文件可包括申请、已发指令、状态观测和外部回执。出现于记录中的申请或意图可能未获准，外部回执可能迟到或与此前观测冲突。

## 浏览资料

在仓库根目录用 Python 3.11 运行。只需标准库。

```sh
python3 sample_reader.py samples/shift-log.jsonl
python3 -m unittest discover -s tests -v
```

原始资料可按 `--kind` 筛选。程序按接收顺序显示记录。单元测试核对资料能够读取，以及事件夹具的基本结构。
