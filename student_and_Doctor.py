# """برنامج لتسجيل درجات طلاب تقنية المعلومات وعرضها باستخدام مكتبة flet وقاعدة بيانات sqlite3
#    مطور البرنامج : ِALi AL-Hatami
#     تاريخ الانشاء : 2024-06-10
# """


from flet import *
from database import init_db, add_student, get_all_students, get_student_count

def main(page: Page):
    # إعدادات الصفحة
    page.title = "Student Grading System"
    page.scroll = "auto"
    page.window_width = 400
    page.window_height = 740
    page.theme_mode = ThemeMode.LIGHT
    page.rtl = True # تفعيل الاتجاه من اليمين لليسار للعربية

    # تهيئة قاعدة البيانات عند التشغيل
    init_db()

    # --- عناصر واجهة الإدخال ---
    tname = TextField(label="اسم الطالب", icon=Icons.PERSON, height=40)
    tmail = TextField(label="البريد الإلكتروني", icon=Icons.EMAIL, height=40)
    tphone = TextField(label="رقم الهاتف", icon=Icons.PHONE, keyboard_type=KeyboardType.PHONE, height=40)
    tid = TextField(label="الرقم الجامعي", icon=Icons.BADGE, height=40)

    # درجات المواد
    web_design = TextField(label="Web Design", width=110, height=40, keyboard_type=KeyboardType.NUMBER)
    data_struct = TextField(label="Data Struct", width=110, height=40, keyboard_type=KeyboardType.NUMBER)
    info_sec = TextField(label="Info Security", width=110, height=40, keyboard_type=KeyboardType.NUMBER)
    comm_tech = TextField(label="Comm Tech", width=110, height=40, keyboard_type=KeyboardType.NUMBER)
    wireless = TextField(label="Wireless Net", width=110, height=40, keyboard_type=KeyboardType.NUMBER)
    comm_skill = TextField(label="Comm Skills", width=110, height=40, keyboard_type=KeyboardType.NUMBER)

    # عداد الطلاب المسجلين
    count_text = Text(str(get_student_count()), size=20, weight="bold")

    # --- الدوال (Logic) ---

    def calculate_grade(grade):
        """دالة مساعدة لحساب التقدير"""
        if grade < 50: return "ضعيف 😒", "red"
        if 50 <= grade < 65: return "مقبول 👍", "orange"
        if 65 <= grade < 80: return "جيد 👌", "blue"
        if 80 <= grade < 90: return "جيد جداً 😘", "indigo"
        return "ممتاز 😍", "green"

    def add_data(e):
        try:
            # التحقق من أن الحقول الرقمية تحتوي أرقاماً فعلاً
            # هذا يمنع البرنامج من التوقف اذا ادخل المستخدم نصاً
            marks = [
                int(web_design.value), int(info_sec.value), int(comm_tech.value),
                int(data_struct.value), int(wireless.value), int(comm_skill.value)
            ]
            
            data_to_save = (
                tname.value, tmail.value, tphone.value, tid.value,
                *marks 
            )

            if add_student(data_to_save):
                page.snack_bar = SnackBar(Text("تمت إضافة الطالب بنجاح"), bgcolor="green")
                page.snack_bar.open = True
                # تحديث العداد
                count_text.value = str(get_student_count())
                # تفريغ الحقول
                tname.value = ""
                page.update()
            else:
                page.snack_bar = SnackBar(Text("حدث خطأ في قاعدة البيانات"), bgcolor="red")
                page.snack_bar.open = True
                
        except ValueError:
            page.snack_bar = SnackBar(Text("الرجاء إدخال أرقام صحيحة في خانة الدرجات"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    def show_students_view(e):
        page.clean()
        
        students = get_all_students()
        
        # زر العودة
        page.add(ElevatedButton("رجوع", icon=Icons.ARROW_BACK, on_click=lambda _: go_home()))

        if not students:
            page.add(Text("لا يوجد طلاب مسجلين", size=20))
            page.update()
            return

        for std in students:
            # تحويل القيم من قاعدة البيانات لأرقام للحساب
            # ملاحظة: sqlite.Row يسمح بالوصول بالاسم
            total_marks = (
                std['stdwebdesigning'] + std['stInfo_Sec'] + std['stCommun_Tech'] +
                std['stDatStructuer'] + std['stWirless_Network'] + std['stCommun_Skill']
            )
            average = total_marks / 6
            grade_text, grade_color = calculate_grade(average)

            # ... (الكود السابق لحساب المعدل average و grade_text) ...

            card = Card(
                color='white',
                elevation=5,
                margin=10,
                content=Container(
                    padding=15,
                    content=Column([
                        # 1. رأس البطاقة (الاسم والرقم)
                        ListTile(
                            leading=Icon(Icons.PERSON, color='blue', size=30),
                            title=Text(std['stdname'], weight="bold", size=18),
                            subtitle=Text(f"ID: {std['std_id']}", color='grey'),
                        ),
                        
                        Divider(height=5, color="transparent"), # مسافة صغيرة

                        # 2. رقم الهاتف
                        Row([
                            Icon(Icons.PHONE, size=16, color='green'),
                            Text(f" {std['stdphone']}", color='green', size=14)
                        ], alignment=MainAxisAlignment.CENTER),

                        Divider(thickness=1, color="#eeeeee"), # خط فاصل خفيف

                        # 3. درجات المواد (تم تصحيح المتغير إلى std وترتيبها)
                        Row([
                            Text(f"Web Design: {std['stdwebdesigning']}", color='blue'),
                            Text(f"Data Struct: {std['stDatStructuer']}", color='blue'),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),

                        Row([
                            Text(f"Info Security: {std['stInfo_Sec']}", color='blue'),
                            Text(f"Comm Tech: {std['stCommun_Tech']}", color='blue'),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),

                        Row([
                            Text(f"Wireless Net: {std['stWirless_Network']}", color='blue'),
                            Text(f"Comm Skills: {std['stCommun_Skill']}", color='blue'),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),

                        Divider(thickness=1, color="black"), # خط فاصل للنتيجة النهائية

                        # 4. المعدل والتقدير
                        Row([
                            Text(f"المعدل: {average:.1f}%", weight="bold", size=16),
                            Text(grade_text, color=grade_color, weight="bold", size=16)
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    ])
                )
            )
            
            page.add(card)
        page.update()

    def go_home():
        page.clean()
        # إعادة بناء الصفحة الرئيسية
        page.add(
            Column([
                Row([Icon(Icons.SCHOOL, size=50, color="blue")], alignment=MainAxisAlignment.CENTER),
                Row([Text("نظام درجات الطلاب", size=25, weight="bold")], alignment=MainAxisAlignment.CENTER),
                Row([Text("الطلاب المسجلين: "), count_text], alignment=MainAxisAlignment.CENTER),
                Divider(),
                tname, tmail, tphone, tid,
                Text("ادخال الدرجات", weight="bold"),
                Row([web_design, info_sec]),
                Row([comm_tech, data_struct]),
                Row([wireless, comm_skill]),
                Divider(),
                Row([
                    ElevatedButton("إضافة طالب", on_click=add_data, bgcolor="blue", color="white", expand=True),
                    ElevatedButton("عرض الطلاب", on_click=show_students_view, bgcolor="green", color="white", expand=True),
                ])
            ], scroll="auto")
        )
        page.update()

    # تشغيل الواجهة الرئيسية أول مرة
    go_home()

app(target=main, assets_dir="assets")


