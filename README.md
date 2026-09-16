# PC版日程记录器 v1.0

一个运行在 PC 上的命令行日程记录器，是嵌入式学习前的第一个完整 Python 工程。

## 功能

- 添加日程（日期 + 时间 + 事件内容）
- 查看日程（查看全部 / 按日期查询）
- 修改日程（改时间或事件内容）
- 删除日程（按编号）
- 自动保存（数据存于 data.json，程序关闭后不丢失）

## 运行环境

- Python 3.x

## 运行方式

```bash
python main.py
```

## 目录结构

```
schedule_manager/
├── main.py      程序入口
├── schedule.py  日程类和业务逻辑
├── database.py  文件读写
├── data.json    数据文件
└── README.md    项目说明
```

## 数据格式

data.json 为 JSON 数组，每项形如：

```json
[{ "date": "2026-09-12", "time": "10:00", "event": "学习Python" }]
```

## 后续升级方向

- v2.0：GUI 界面（Tkinter/PyQt）
- v3.0：数据库 SQLite
- v4.0：树莓派部署
- v5.0：联网同步和提醒功能
