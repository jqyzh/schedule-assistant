"""
test_schedule.py —— ScheduleManager 的单元测试。

运行：python -m unittest test_schedule -v
"""
import os
import tempfile
import unittest

import database_sqlite
from schedule import ScheduleManager


class TestScheduleManager(unittest.TestCase):

    def setUp(self):
        # 造一个临时文件顶替 data.json，测试不碰真实数据
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        tmp.close()
        database_sqlite.DB_FILE = tmp.name      # 把存储层指向临时文件
        self.mgr = ScheduleManager()       # 雇一个"管家"，连上临时文件
        self.mgr.load()

    def tearDown(self):
        os.unlink(database_sqlite.DB_FILE)      # 测试结束删掉临时文件

    # ---------- 添加 ----------
    def test_add(self):
        self.mgr.add("2026-09-15", "20:00", "写单元测试")
        self.assertEqual(len(self.mgr.all()), 1)
        self.assertEqual(self.mgr.get(0).event, "写单元测试")

    # ---------- 删除 ----------
    def test_delete(self):
        self.mgr.add("2026-09-15", "20:00", "A")
        removed = self.mgr.delete(0)
        self.assertEqual(removed.event, "A")
        self.assertEqual(len(self.mgr.all()), 0)

    # ---------- 删除不存在的编号 ----------
    def test_delete_invalid_index(self):
        """删除不存在的编号，应该什么都不发生、返回 None。"""
        self.mgr.add("2026-09-15", "20:00", "A")
        result = self.mgr.delete(99)
        self.assertIsNone(result)                 # 返回 None
        self.assertEqual(len(self.mgr.all()), 1)  # 日程还在

    # ---------- modify 只改传入的字段 ----------
    def test_modify_date_and_time(self):
        """modify 只改传入的字段（None 表示不改）。"""
        self.mgr.add("2026-09-15", "20:00", "A")
        self.mgr.modify(0, date="2026-09-16")
        s = self.mgr.get(0)
        self.assertEqual(s.date, "2026-09-16")  # 日期变了
        self.assertEqual(s.time, "20:00")       # 时间没变
        self.assertEqual(s.event, "A")          # 内容没变

    # ---------- event=None 表示保持 ----------
    def test_modify_none_means_keep(self):
        """event 传 None 表示保持原内容（不清空）。"""
        self.mgr.add("2026-09-15", "20:00", "原内容")
        self.mgr.modify(0, event=None)
        self.assertEqual(self.mgr.get(0).event, "原内容")

    # ---------- event="" 表示清空 ----------
    def test_modify_empty_string_means_clear(self):
        """event 传 "" 表示清空——这正是 None 和 "" 的区别。"""
        self.mgr.add("2026-09-15", "20:00", "原内容")
        self.mgr.modify(0, event="")
        self.assertEqual(self.mgr.get(0).event, "")

    # ---------- 按日期查询自动补零 ----------
    def test_query_by_date_normalizes(self):
        """按日期查询时自动补零：'2026-9-5' 也要能查到 '2026-09-05'。"""
        self.mgr.add("2026-09-05", "08:00", "早起")
        result = self.mgr.query_by_date("2026-9-5")
        self.assertEqual(len(result), 1)

    # ---------- get 越界 ----------
    def test_get_out_of_range(self):
        """get 越界时返回 None，不崩溃。"""
        self.assertIsNone(self.mgr.get(0))  # 空列表上取第 0 条

    # ---------- 存盘后重新 load 数据还在 ----------
    def test_persistence(self):
        """存盘后，新的 ScheduleManager 重新 load，数据还在。"""
        self.mgr.add("2026-09-15", "20:00", "持久化测试")
        new_mgr = ScheduleManager()   # 换一个"新管家"
        new_mgr.load()                # 从临时文件重新读
        self.assertEqual(len(new_mgr.all()), 1)
        self.assertEqual(new_mgr.get(0).event, "持久化测试")