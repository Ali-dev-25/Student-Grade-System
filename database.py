import sqlite3

DB_NAME = "students.db"

def init_db():
    """إنشاء الجدول إذا لم يكن موجوداً"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stdname TEXT,
            stdmail TEXT,
            stdphone TEXT,
            std_id TEXT,
            stdwebdesigning INTEGER,
            stInfo_Sec INTEGER,
            stCommun_Tech INTEGER,
            stDatStructuer INTEGER,
            stWirless_Network INTEGER,
            stCommun_Skill INTEGER
        )
    """)
    conn.commit()
    conn.close()

def add_student(data):
    """دالة لإضافة طالب جديد تستقبل قائمة بيانات"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO student(stdname,stdmail,stdphone,std_id,stdwebdesigning,stInfo_Sec,stCommun_Tech,stDatStructuer,stWirless_Network,stCommun_Skill) 
            VALUES(?,?,?,?,?,?,?,?,?,?)
        """, data)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()

def get_all_students():
    """جلب كل الطلاب"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # هذا يجعل النتائج تظهر كـ Dictionary
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_student_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM student")
    count = cursor.fetchone()[0]
    conn.close()
    return count