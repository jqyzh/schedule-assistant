"""
main.py —— 程序入口。

使用 while 循环 + input 实现命令行菜单：
  1 添加  2 查看  3 修改  4 删除  5 退出

约定：在任意子菜单的输入处输入 0，即可返回上一级（不保存当前操作）。
"""

from datetime import datetime

from schedule import ScheduleManager


# 哨兵对象：表示"用户输入了 0，想返回上一级"  人为创建的一个特殊标记
BACK = object()


# ---------- 输入校验 ----------
def input_date(prompt="请输入日期(YYYY-MM-DD)：", allow_blank=False, use_now=False):
    """输入日期并校验格式。

    allow_blank=True：直接回车返回 None（修改时用来保持原值）。
    use_now=True：直接回车返回今天的日期（添加时用来快捷填入）。
    输入 0 返回 BACK（返回上一级）。
    """
    while True:
        s = input(prompt).strip()
        if s == "0":
            return BACK
        if s == "":
            if use_now:
                return datetime.now().strftime("%Y-%m-%d")
            if allow_blank:
                return None
        try:
            return datetime.strptime(s, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("日期格式不对，请按 YYYY-MM-DD 输入，例如 2026-09-12。")


def input_time(prompt="请输入时间(HH:MM)：", allow_blank=False, use_now=False):
    """输入时间并校验格式，规则同 input_date。"""
    while True:
        s = input(prompt).strip()
        if s == "0":
            return BACK
        if s == "":
            if use_now:
                return datetime.now().strftime("%H:%M")
            if allow_blank:
                return None
        try:
            return datetime.strptime(s, "%H:%M").strftime("%H:%M")
        except ValueError:
            print("时间格式不对，请按 HH:MM 输入，例如 10:00。")


def input_event(prompt="请输入事件内容：", allow_blank=False):
    """输入事件内容，不允许为空；输入 0 返回上一级。"""
    while True:
        s = input(prompt).strip()
        if s == "0":
            return BACK
        if allow_blank and s == "":
            return None
        if s == "":
            print("事件内容不能为空。")
            continue
        return s


def choose_index(manager):
    """列出所有日程，让用户选一个编号，返回索引(0 起)。

    没有日程时返回 None；输入 0 返回 BACK。
    """
    schedules = manager.all()
    if not schedules:
        print("还没有任何日程。")
        return None
    for i, s in enumerate(schedules, start=1):
        print(f"  {i}. {s}")
    while True:
        raw = input("请输入日程编号(0 返回)：").strip()
        if raw == "0":
            return BACK
        if not raw.isdigit():
            print("编号必须是数字。")
            continue
        idx = int(raw) - 1
        if 0 <= idx < len(schedules):
            return idx
        print("编号超出范围，请重新输入。")


# ---------- 菜单动作 ----------
def add_schedule(manager):   #增加一个日程
    date = input_date("请输入日期(YYYY-MM-DD)，直接回车使用今天，0 返回：", use_now=True)
    if date is BACK:
        return
    time = input_time("请输入时间(HH:MM)，直接回车使用现在，0 返回：", use_now=True)
    if time is BACK:
        return
    event = input_event("请输入事件内容(0 返回)：")
    if event is BACK:
        return
    manager.add(date, time, event)
    print(f"已添加日程：{date} {time}  {event}")


def view_all(manager):#看所有日程
    schedules = manager.all()
    print("\n全部日程：")
    for i, s in enumerate(schedules, start=1):
        print(f"  {i}. {s}")
    print(f"共 {len(schedules)} 条。")


def view_by_date(manager):#根据输入的日期来查询日程
    date = input_date("请输入日期(YYYY-MM-DD)，0 返回：")
    if date is BACK:
        return
    result = manager.query_by_date(date)
    if not result:
        print(f"{date} 没有日程。")
        return
    print(f"\n{date} 的日程：")
    for i, s in enumerate(result, start=1):
        print(f"  {i}. {s}")
    print(f"共 {len(result)} 条。")


def view_one(manager):
    """列出全部日程，让用户按编号选择查看其中一条。"""
    idx = choose_index(manager)
    if idx is None or idx is BACK:
        return
    s = manager.get(idx)
    print("\n日程详情：")
    print(f"  日期：{s.date}")
    print(f"  时间：{s.time}")
    print(f"  事件：{s.event}")


def view_schedule(manager): #开始菜单
    if not manager.all():
        print("还没有任何日程。")
        return
    print("\n请选择查看方式：")
    print("  1 查看全部")
    print("  2 按日期查询")
    print("  3 按编号查看单条")
    print("  0 返回")
    choice = input("请选择：").strip()
    if choice == "0":
        return
    if choice == "2":
        view_by_date(manager)
    elif choice == "3":
        view_one(manager)
    else:
        view_all(manager)


def modify_schedule(manager):
    idx = choose_index(manager)
    if idx is None or idx is BACK:
        return
    s = manager.get(idx)
    print(f"当前日程：{s}")
    date = input_date("新日期(直接回车保持不变，0 返回)：", allow_blank=True)
    if date is BACK:
        return
    time = input_time("新时间(直接回车保持不变，0 返回)：", allow_blank=True)
    if time is BACK:
        return
    # 内容修改方式选择
    print("\n请选择内容修改方式：")
    print("  1 覆盖（用新内容替换）")
    print("  2 追加（在原有内容后面加）")
    print("  3 清空（删除原有内容）")
    print("  0 保持不变")
    mode = input("请选择：").strip()

    if mode == "1":  # 覆盖
        event = input_event("请输入新内容(0 返回)：")
        if event is BACK:
            return
    elif mode == "2":  # 追加
        add = input_event("请输入要追加的内容(0 返回)：")
        if add is BACK:
            return
        event = s.event + add
    elif mode == "3":  # 清空
        event = ""
    else:  # 0 或无效输入，内容保持不变
        print("内容保持不变。")
        event = None

    manager.modify(idx, date, time, event)
    print("已修改日程。")


def delete_schedule(manager):
    idx = choose_index(manager)
    if idx is None or idx is BACK:
        return
    s = manager.get(idx)
    manager.delete(idx)
    print(f"已删除日程：{s}")


def print_menu():
    print("\n" + "=" * 30)
    print("日程记录器 v1.0")
    print("  1 添加日程")
    print("  2 查看日程")
    print("  3 修改日程")
    print("  4 删除日程")
    print("  5 退出")
    print("=" * 30)
    print("（子菜单里输入 0 可返回上一级）")

def main():
    manager = ScheduleManager()
    manager.load()
    while True:
        print_menu()
        choice = input("请选择：").strip()
        if choice == "1":
            add_schedule(manager)
        elif choice == "2":
            view_schedule(manager)
        elif choice == "3":
            modify_schedule(manager)
        elif choice == "4":
            delete_schedule(manager)
        elif choice in ("5", "0"):
            manager.save()
            print("数据已保存，再见！")
            break
        else:
            print("输入无效，请输入 1-5。")


if __name__ == "__main__":
    main()
