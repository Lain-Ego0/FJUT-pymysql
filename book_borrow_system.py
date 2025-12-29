import sqlite3
import datetime
import os

# 数据库文件路径（自动生成在当前目录，无需手动创建）
DB_FILE = "book_borrow.db"

# -------------------------- 数据库初始化（自动创建表） --------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 1. 创建图书表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            isbn TEXT PRIMARY KEY,
            book_name TEXT NOT NULL,
            authors TEXT NOT NULL,
            publisher TEXT NOT NULL,
            price REAL NOT NULL,
            intro TEXT
        )
    ''')

    # 2. 创建借阅者表（借书证）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowers (
            borrower_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            occupation TEXT NOT NULL
        )
    ''')

    # 3. 创建借阅记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrow_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            borrower_id TEXT NOT NULL,
            book_isbn TEXT NOT NULL,
            borrow_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (borrower_id) REFERENCES borrowers (borrower_id),
            FOREIGN KEY (book_isbn) REFERENCES books (isbn)
        )
    ''')

    conn.commit()
    conn.close()

# -------------------------- 工具函数（简化操作） --------------------------
# 清屏（跨平台）
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# 日期转换：字符串转datetime
def str_to_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        return None

# 计算应还日期（借阅日期+30天）
def get_due_date(borrow_date):
    borrow_date_obj = str_to_date(borrow_date)
    if borrow_date_obj:
        due_date_obj = borrow_date_obj + datetime.timedelta(days=30)
        return due_date_obj.strftime("%Y-%m-%d")
    return None

# -------------------------- 图书管理模块 --------------------------
# 添加图书
def add_book():
    clear_screen()
    print("===== 添加图书 =====")
    isbn = input("请输入图书ISBN（唯一）：").strip()
    if not isbn:
        print("ISBN不能为空！")
        input("按回车键返回...")
        return

    # 检查ISBN是否已存在
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE isbn=?", (isbn,))
    if cursor.fetchone():
        print("该ISBN已存在！")
        conn.close()
        input("按回车键返回...")
        return

    book_name = input("请输入图书名称：").strip()
    authors = input("请输入作者（多个用逗号分隔）：").strip()
    publisher = input("请输入出版社：").strip()
    try:
        price = float(input("请输入图书定价：").strip())
    except:
        print("定价必须是数字！")
        conn.close()
        input("按回车键返回...")
        return
    intro = input("请输入图书简介（可选，直接回车跳过）：").strip()

    # 插入数据
    cursor.execute('''
        INSERT INTO books (isbn, book_name, authors, publisher, price, intro)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (isbn, book_name, authors, publisher, price, intro))
    conn.commit()
    conn.close()
    print("图书添加成功！")
    input("按回车键返回...")

# 查询图书
def query_book():
    clear_screen()
    print("===== 查询图书 =====")
    keyword = input("请输入书名或ISBN（模糊查询，直接回车显示所有图书）：").strip()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    if keyword:
        # 模糊查询
        cursor.execute('''
            SELECT * FROM books WHERE book_name LIKE ? OR isbn LIKE ?
        ''', (f"%{keyword}%", f"%{keyword}%"))
    else:
        # 查询所有
        cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()
    conn.close()

    if not books:
        print("未查询到图书！")
    else:
        print(f"共查询到 {len(books)} 本图书：")
        print("ISBN\t\t\t书名\t\t作者\t\t出版社\t\t定价")
        print("-" * 80)
        for book in books:
            isbn, book_name, authors, publisher, price, intro = book
            # 格式化输出，避免排版混乱
            print(f"{isbn}\t{book_name[:10]}\t{authors[:8]}\t{publisher[:8]}\t{price:.2f}")
    input("按回车键返回...")

# -------------------------- 借阅者管理模块 --------------------------
# 添加借阅者（办借书证）
def add_borrower():
    clear_screen()
    print("===== 办理借书证（添加借阅者） =====")
    borrower_id = input("请输入借书证编号（唯一）：").strip()
    if not borrower_id:
        print("借书证编号不能为空！")
        input("按回车键返回...")
        return

    # 检查借书证是否已存在
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM borrowers WHERE borrower_id=?", (borrower_id,))
    if cursor.fetchone():
        print("该借书证编号已存在！")
        conn.close()
        input("按回车键返回...")
        return

    name = input("请输入借阅者姓名：").strip()
    unit = input("请输入所在单位：").strip()
    occupation = input("请输入职业：").strip()

    # 插入数据
    cursor.execute('''
        INSERT INTO borrowers (borrower_id, name, unit, occupation)
        VALUES (?, ?, ?, ?)
    ''', (borrower_id, name, unit, occupation))
    conn.commit()
    conn.close()
    print("借书证办理成功！")
    input("按回车键返回...")

# 查询借阅者
def query_borrower():
    clear_screen()
    print("===== 查询借阅者 =====")
    keyword = input("请输入姓名或借书证编号（模糊查询，直接回车显示所有）：").strip()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    if keyword:
        cursor.execute('''
            SELECT * FROM borrowers WHERE name LIKE ? OR borrower_id LIKE ?
        ''', (f"%{keyword}%", f"%{keyword}%"))
    else:
        cursor.execute("SELECT * FROM borrowers")

    borrowers = cursor.fetchall()
    conn.close()

    if not borrowers:
        print("未查询到借阅者！")
    else:
        print(f"共查询到 {len(borrowers)} 位借阅者：")
        print("借书证编号\t姓名\t\t单位\t\t职业")
        print("-" * 60)
        for borrower in borrowers:
            borrower_id, name, unit, occupation = borrower
            print(f"{borrower_id}\t\t{name}\t\t{unit[:10]}\t{occupation}")
    input("按回车键返回...")

# -------------------------- 借阅业务模块 --------------------------
# 借书操作（校验最多8本）
def borrow_book():
    clear_screen()
    print("===== 图书借阅 =====")
    borrower_id = input("请输入借书证编号：").strip()
    book_isbn = input("请输入图书ISBN：").strip()

    # 检查借阅者和图书是否存在
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 检查借阅者
    cursor.execute("SELECT * FROM borrowers WHERE borrower_id=?", (borrower_id,))
    if not cursor.fetchone():
        print("该借阅者不存在！")
        conn.close()
        input("按回车键返回...")
        return

    # 检查图书
    cursor.execute("SELECT * FROM books WHERE isbn=?", (book_isbn,))
    if not cursor.fetchone():
        print("该图书不存在！")
        conn.close()
        input("按回车键返回...")
        return

    # 检查当前未还图书数量（return_date为NULL）
    cursor.execute('''
        SELECT COUNT(*) FROM borrow_records
        WHERE borrower_id=? AND return_date IS NULL
    ''', (borrower_id,))
    borrow_count = cursor.fetchone()[0]

    if borrow_count >= 8:
        print(f"借阅失败！当前已借 {borrow_count} 本，最多可借8本。")
        conn.close()
        input("按回车键返回...")
        return

    # 获取当前日期作为借阅日期
    borrow_date = datetime.date.today().strftime("%Y-%m-%d")
    # 计算应还日期（+30天）
    due_date = get_due_date(borrow_date)

    # 插入借阅记录
    cursor.execute('''
        INSERT INTO borrow_records (borrower_id, book_isbn, borrow_date, due_date)
        VALUES (?, ?, ?, ?)
    ''', (borrower_id, book_isbn, borrow_date, due_date))
    conn.commit()
    conn.close()

    print(f"借阅成功！")
    print(f"借阅日期：{borrow_date}")
    print(f"应还日期：{due_date}")
    input("按回车键返回...")

# 还书操作（校验30天期限）
def return_book():
    clear_screen()
    print("===== 图书归还 =====")
    record_id = input("请输入借阅记录ID：").strip()
    if not record_id.isdigit():
        print("记录ID必须是数字！")
        input("按回车键返回...")
        return
    record_id = int(record_id)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 检查借阅记录是否存在，且未归还
    cursor.execute('''
        SELECT * FROM borrow_records
        WHERE record_id=? AND return_date IS NULL
    ''', (record_id,))
    record = cursor.fetchone()
    if not record:
        print("该借阅记录不存在或已归还！")
        conn.close()
        input("按回车键返回...")
        return

    # 解析记录
    record_id, borrower_id, book_isbn, borrow_date, due_date, return_date = record
    # 获取当前日期
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    # 检查是否逾期
    due_date_obj = str_to_date(due_date)
    current_date_obj = str_to_date(current_date)
    if current_date_obj > due_date_obj:
        overdue_days = (current_date_obj - due_date_obj).days
        print(f"提示：该图书已逾期 {overdue_days} 天！")

    # 更新还书日期
    cursor.execute('''
        UPDATE borrow_records
        SET return_date=?
        WHERE record_id=?
    ''', (current_date, record_id))
    conn.commit()
    conn.close()

    print("图书归还成功！")
    input("按回车键返回...")

# 查询借阅记录
def query_borrow_record():
    clear_screen()
    print("===== 查询借阅记录 =====")
    borrower_id = input("请输入借书证编号（直接回车显示所有记录）：").strip()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    if borrower_id:
        cursor.execute('''
            SELECT br.record_id, br.borrower_id, b.name, br.book_isbn, bo.book_name,
                   br.borrow_date, br.due_date, br.return_date
            FROM borrow_records br
            LEFT JOIN borrowers b ON br.borrower_id = b.borrower_id
            LEFT JOIN books bo ON br.book_isbn = bo.isbn
            WHERE br.borrower_id=?
        ''', (borrower_id,))
    else:
        cursor.execute('''
            SELECT br.record_id, br.borrower_id, b.name, br.book_isbn, bo.book_name,
                   br.borrow_date, br.due_date, br.return_date
            FROM borrow_records br
            LEFT JOIN borrowers b ON br.borrower_id = b.borrower_id
            LEFT JOIN books bo ON br.book_isbn = bo.isbn
        ''')

    records = cursor.fetchall()
    conn.close()

    if not records:
        print("未查询到借阅记录！")
    else:
        print(f"共查询到 {len(records)} 条借阅记录：")
        print("记录ID\t借书证\t姓名\t图书ISBN\t书名\t借阅日期\t应还日期\t实际还书日期")
        print("-" * 100)
        for record in records:
            record_id, borrower_id, name, book_isbn, book_name, borrow_date, due_date, return_date = record
            return_date = return_date if return_date else "未归还"
            print(f"{record_id}\t{borrower_id}\t{name}\t{book_isbn}\t{book_name[:8]}\t{borrow_date}\t{due_date}\t{return_date}")
    input("按回车键返回...")

# -------------------------- 主菜单 --------------------------
def main_menu():
    while True:
        clear_screen()
        print("===== 图书借阅管理系统（大作业简易版） =====")
        print("1. 图书管理")
        print("2. 借阅者管理")
        print("3. 借阅业务")
        print("0. 退出系统")
        print("=" * 40)
        choice = input("请输入操作编号：").strip()

        if choice == "1":
            # 图书管理子菜单
            while True:
                clear_screen()
                print("===== 图书管理 =====")
                print("1. 添加图书")
                print("2. 查询图书")
                print("0. 返回主菜单")
                sub_choice = input("请输入操作编号：").strip()
                if sub_choice == "1":
                    add_book()
                elif sub_choice == "2":
                    query_book()
                elif sub_choice == "0":
                    break
                else:
                    print("无效编号，请重新输入！")
                    input("按回车键返回...")
        elif choice == "2":
            # 借阅者管理子菜单
            while True:
                clear_screen()
                print("===== 借阅者管理 =====")
                print("1. 办理借书证（添加借阅者）")
                print("2. 查询借阅者")
                print("0. 返回主菜单")
                sub_choice = input("请输入操作编号：").strip()
                if sub_choice == "1":
                    add_borrower()
                elif sub_choice == "2":
                    query_borrower()
                elif sub_choice == "0":
                    break
                else:
                    print("无效编号，请重新输入！")
                    input("按回车键返回...")
        elif choice == "3":
            # 借阅业务子菜单
            while True:
                clear_screen()
                print("===== 借阅业务 =====")
                print("1. 借书")
                print("2. 还书")
                print("3. 查询借阅记录")
                print("0. 返回主菜单")
                sub_choice = input("请输入操作编号：").strip()
                if sub_choice == "1":
                    borrow_book()
                elif sub_choice == "2":
                    return_book()
                elif sub_choice == "3":
                    query_borrow_record()
                elif sub_choice == "0":
                    break
                else:
                    print("无效编号，请重新输入！")
                    input("按回车键返回...")
        elif choice == "0":
            clear_screen()
            print("感谢使用图书借阅管理系统，再见！")
            break
        else:
            print("无效编号，请重新输入！")
            input("按回车键返回...")

# -------------------------- 程序入口 --------------------------
if __name__ == "__main__":
    # 初始化数据库（自动创建表）
    init_db()
    # 启动主菜单
    main_menu()