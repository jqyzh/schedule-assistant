"""
database.py —— 负责日程数据的文件读写。

v1.0 使用 JSON 文件(data.json)保存数据，程序关闭后数据不会丢失。
本模块只关心"把数据存进文件"和"从文件读出数据"，不涉及业务逻辑。
"""

import json
import os

# data.json 与本文件放在同一目录下
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


# 从 data.json 读取所有日程返回列表；文件不存在或损坏时返回 []，程序仍能正常启动。
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 确保读出来的是列表，否则视为无效数据
        if isinstance(data, list):
            return data
        return []
    except (json.JSONDecodeError, OSError):
        # 文件损坏 / 读取失败时，返回空列表，不崩溃
        return []


# 把日程列表写入 data.json（ensure_ascii=False 中文正常显示，indent=2 格式整齐）。
def save_data(schedules):
    tmp = DATA_FILE + ".tmp"          # ① 先造一个新文件，比如 data.json.tmp
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(schedules, f,ensure_ascii=False, indent=2)   # ② 往这个新文件里写
    os.replace(tmp, DATA_FILE)         # ③ 写完了，用它替换掉旧的 data.json