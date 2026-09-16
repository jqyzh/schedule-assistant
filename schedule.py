"""
schedule.py —— 日程类与业务逻辑。

包含两个类：
1. Schedule：表示一条日程（date 日期 / time 时间 / event 事件内容）。
2. ScheduleManager：负责日程的增、删、改、查，并和文件读写对接。
"""

from datetime import datetime

from database_sqlite import load_data, save_data


def _norm_date(d):
    """把日期统一成 YYYY-MM-DD，便于比较（如 "2026-9-12" -> "2026-09-12"）。"""
    try:
        return datetime.strptime(str(d), "%Y-%m-%d").strftime("%Y-%m-%d")

    except ValueError:
        return d


class Schedule:
    """一条日程。"""

    def __init__(self, date, time, event):
        self.date = date    # 日期，如 "2026-09-12"
        self.time = time    # 时间，如 "10:00"
        self.event = event  # 事件内容，如 "学习Python"

    def to_dict(self):
        """转成字典，方便用 json 保存。"""
        return {"date": self.date, "time": self.time, "event": self.event}

    @classmethod
    def from_dict(cls, data):
        """从字典还原成 Schedule 对象。"""
        return cls(data.get("date", ""), data.get("time", ""), data.get("event", ""))

    def __str__(self):
        return f"{self.date} {self.time}  {self.event}"


class ScheduleManager:
    """日程管理：负责增删改查，并和文件读写对接。"""

    def __init__(self):
        self.schedules = []  # 存放 Schedule 对象的列表

    def load(self):
        """启动时从文件载入已有日程。"""
        self.schedules = [Schedule.from_dict(d) for d in load_data()]

    def save(self):
        """把件当前所有日程写回文件。"""
        save_data([s.to_dict() for s in self.schedules])

    def get(self, index):
        """按编号返回日程，编号非法时返回 None。"""
        if 0 <= index < len(self.schedules):
            return self.schedules[index]
        return None

    # ---- 增 ----
    def add(self, date, time, event):        #在日程管理表中增加一个日程
        self.schedules.append(Schedule(date, time, event))
        self.save()

    # ---- 删 ----
    def delete(self, index):
        """按编号删除，编号合法时返回被删除的日程，否则返回 None。"""
        if 0 <= index < len(self.schedules):
            removed = self.schedules.pop(index)
            self.save()
            return removed
        return None

    # ---- 改 ----
    def modify(self, index, date=None, time=None, event=None):
        """按编号修改，只修改传入的字段（None 表示不改）。

        event 特例：None 表示不改，"" 表示清空内容，其他字符串表示覆盖/追加。
        """
        s = self.get(index)
        if s is None:
            return None
        if date:
            s.date = date
        if time:
            s.time = time
        if event is not None:
            s.event = event
        self.save()
        return s

    # ---- 查 ----
    def query_by_date(self, date):
        """按日期查询，返回匹配的日程列表（自动统一日期格式）。"""
        result = []

        for s in self.schedules:

            if _norm_date(s.date) == _norm_date(date):
                result.append(s)

        return result

    def all(self):
        """返回全部日程列表。"""
        return list(self.schedules)  ##复制一个新的列表，不然的话就是指向对应的原来的schedules
