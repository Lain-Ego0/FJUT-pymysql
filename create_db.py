import sqlite3

# 数据库文件保存到桌面（明确路径，避免找不到）
DB_FILE = "C:\\Users\\23021\\Desktop\\book_borrow.db"  # 替换「你的用户名」（比如Admin、你的电脑名）

# 手动创建数据库和表
def create_db_manually():
    try:
        # 连接数据库（不存在则自动创建）
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        print("数据库文件创建成功！")

        # 创建3张核心表（和原程序一致）
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (isbn TEXT PRIMARY KEY, book_name TEXT NOT NULL, authors TEXT NOT NULL, publisher TEXT NOT NULL, price REAL NOT NULL, intro TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS borrowers (borrower_id TEXT PRIMARY KEY, name TEXT NOT NULL, unit TEXT NOT NULL, occupation TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS borrow_records (record_id INTEGER PRIMARY KEY AUTOINCREMENT, borrower_id TEXT NOT NULL, book_isbn TEXT NOT NULL, borrow_date TEXT NOT NULL, due_date TEXT NOT NULL, return_date TEXT, FOREIGN KEY (borrower_id) REFERENCES borrowers (borrower_id), FOREIGN KEY (book_isbn) REFERENCES books (isbn))''')

        conn.commit()
        conn.close()
        print("数据表创建成功！")
    except Exception as e:
        print(f"错误信息：{e}")
        input("按回车键退出...")

if __name__ == "__main__":
    create_db_manually()
    input("创建完成，按回车键退出...")