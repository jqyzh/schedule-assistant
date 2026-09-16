"""
database_sqlite.py —— SQLite 版存储层。

与 database.py 接口完全一致：上层（schedule.py）无需关心数据存在哪。
数据文件为 schedule.db（SQLite 数据库，一个文件就是一个库）。
"""
import os
import sqlite3

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schedule.db")


def _connect():
    """连接数据库。row_factory 让查询结果可以像字典一样按列名取值。"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db(conn):
    """建表（表已存在则跳过）。"""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schedules (
            date  TEXT NOT NULL,
            time  TEXT NOT NULL,
            event TEXT NOT NULL
        )
        """
    )
    conn.commit()


def load_data():
    """读出全部日程，返回字典列表。数据库不存在时返回 []。"""
    if not os.path.exists(DB_FILE):
        return []
    conn = _connect()
    try:
        _init_db(conn)
        rows = conn.execute("SELECT date, time, event FROM schedules").fetchall()
        return [dict(row) for row in rows]   # Row → 普通字典
    finally:
        conn.close()


def save_data(schedules):
    """把日程列表整体写入数据库：先清空表，再批量插入。"""
    conn = _connect()
    try:
        _init_db(conn)
        conn.execute("DELETE FROM schedules")   # 清空旧数据
        conn.executemany(                        # 批量插入，一条 SQL 插多条
            "INSERT INTO schedules (date, time, event) VALUES (?, ?, ?)",
            [(s["date"], s["time"], s["event"]) for s in schedules],
        )
        conn.commit()
    finally:
        conn.close()