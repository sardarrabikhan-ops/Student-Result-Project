def get_text(prompt):
    while True:
        text = input(prompt).strip()
        if not text:
            print("Input cannot be empty!")
            continue
        return text

def get_name(prompt, min, max):
    while True:
        name = input(prompt).strip()
        if not name:
            print("Input cannot be empty!")
            continue
        if min > len(name) or len(name) > max:
            print(f"The name must contain more than {min} and less than {max} characters!")
            continue
        return name
    
def get_int(prompt, min = 0, max = 100):
    while True:
        num = get_text(prompt)
        try:
            num = int(num)
            if min <= num <= max:
                return num
            else:
                print(f"The number must be between {min} and {max}!")
        except ValueError:
            print("Enter a valid number!")

def get_clear(prompt):
    while True:
        clear = get_text(prompt).lower()
        if clear in ("yes", "no"):
            return clear
        print("Reply in 'yes' or 'no'!")


subjects = ["Math","Urdu","Phy","Eng","Isl","Chem","Com/Bio"]
students = []


class Student:
    def __init__(self, roll, name):
        self.roll = roll
        self.name = name
        self.marks = {}
    
    def add_marks(self, subject, obtained, total):
        self.marks[subject] = (obtained, total)
    
    def total_obtained_marks(self):
        return sum(obtained for obtained, total in self.marks.values())
    
    def percentage(self):
        total = sum(total for obtained, total in self.marks.values())
        if total == 0:
            return 0
        return round((self.total_obtained_marks()/total)*100, 2)
    
    def grade(self):
        p = self.percentage()
        if p >= 90:
            return "A+"
        elif p >= 80:
            return "A"
        elif p >= 70:
            return "B"
        elif p >= 50:
            return "C"
        elif p >= 33:
            return "D"
        else:
            return "F"
    
    def status(self):
        for obtained, total in self.marks.values():
            if (obtained/total)*100 < 33:
                return "FAIL"
        return "PASS"
    
    def to_dict(self):
        return {
            "roll": self.roll,
            "name": self.name,
            "marks": self.marks
        }
    
    @staticmethod
    def from_dict(data):
        s = Student(data["roll"], data["name"])
        s.marks = {k: tuple(v) for k, v in data["marks"].items()}
        return s
    
    def show_result(self, rank):
        p = self.percentage()
        g = self.grade()
        s = self.status()
        g_total = sum(total for obtained, total in self.marks.values())
        
        print(f"{rank:<10}{self.roll:<13}{self.name:<16}",end="")
        for subject, (obtained, total_marks) in self.marks.items():
            print(f"{obtained:<3}/{total_marks:<6}",end="")
        print(f"{g_total:<10}{self.total_obtained_marks():<10}{str(p) + '%':10}{g:<10}{s:<10}")

import json
import os
def load_data():
    if not os.path.exists("students_data.json"):
        return []
    try:
        with open("students_data.json","r") as f:
            return json.load(f)
    except:
        return []

def save_data(students):
    with open("students_data.json","w") as f:
        json.dump(students, f, indent=4)

def load_students():
    return [Student.from_dict(s) for s in load_data()]

def save_students(students):
    save_data([s.to_dict() for s in students])

def get_rank(student, students):
    sorted_students = sorted(students, key = lambda s: s.percentage(), reverse = True)

    rank = 0
    prev_per = None

    for s in sorted_students:
        current_per = s.percentage()
        
        if current_per != prev_per:
            rank += 1

        if s.roll == student.roll:
            return rank
        prev_per = current_per

    return None

def get_sorted_students(students):
    return sorted(students, key=lambda s: s.percentage(), reverse=True)

def add_students():
    students = load_students()
    roll_no = {s.roll for s in students}
    while True:
        roll = get_int("Enter student's Roll no: ", 1, 10000)
        if roll in roll_no:
            print("This roll no is taken.")
            continue
        name = get_name("Enter student's name: ", 3, 14)
        s = Student(roll, name)

        for sub in subjects:
            total = get_int(f"Enter total marks of {sub}: ", 1, 100)
            obtained = get_int(f"Enter obtained marks of {sub}: ", 0, total)
            s.add_marks(sub, obtained, total)
        students.append(s)
        roll_no.add(roll)

        clearify = get_clear("Add another student ('yes' or 'no')?")
        if clearify == "no":
            break
    save_students(students)

def failed(students):
    return sum(1 for s in students if s.status() == "FAIL")

def show_class_result():

    students = load_students()
    students = get_sorted_students(students)
    if students:
        print(f"{'='*68}{'C L A S S    R E S U L T'}{'='*68}")
        print(f"{'Total Students: ' + str(len(students)):^160}")
        print("="*160)
        print(f"{'Rank':<10}{'Roll No':<13}{'Name':<16}",end="")
        for sub in subjects:
            print(f"{sub:<10}",end="")
        print(f"{'Total':<10}{'Obtained':<10}{'Per(%)':<10}{'Grade':<10}{'Status':<10}")
        print("="*160)
        for s in students:
            rank = get_rank(s, students)
            s.show_result(rank)
            print("-"*160)
        print("="*160)
        avg = sum(s.percentage() for s in students)/len(students)
        print(f"Average: {avg:.2f}%")
        print(f"Failed: {failed(students)}")
        print("="*160)
    else:
        print("No students are available.")

# SEARCHING PROCESS

def search_by_roll():

    students = load_students()
    if students:
        search_roll = get_int("Enter roll no of student: ", 1, 10000)
        for s in students:
            if s.roll == search_roll:
                print("\nStudent found\n")
                print(f"{'Rank':<10}{'Roll No':<13}{'Name':<16}",end="")
                for sub in subjects:
                    print(f"{sub:<10}",end="")
                print(f"{'Total':<10}{'Obtained':<10}{'Per(%)':<10}{'Grade':<10}{'Status':<10}")
                print("="*160)
                rank = get_rank(s, students)
                s.show_result(rank)
                return
        print("Student not found.")
    else:
        print("No students are available.")

def search_by_name():

    students = load_students()

    if not students:
        print("No students are available.")
        return
    search_name = get_name("Enter student's name: ", 1, 14).lower()
    found_students = []
    for s in students:
        if search_name in s.name.lower():
            found_students.append(s)
    
    if found_students:
        print("\nStudent(s) found\n")
        print(f"{'Rank':<10}{'Roll No':<13}{'Name':<16}",end="")
        for sub in subjects:
            print(f"{sub:<10}",end="")
        print(f"{'Total':<10}{'Obtained':<10}{'Per(%)':<10}{'Grade':<10}{'Status':<10}")
        print("="*160)

        for s in found_students:
            rank = get_rank(s, students)
            s.show_result(rank)
    else:
        print("Student not found.")

def search_student():
    print("1. Search by roll no.")
    print("2. Search by name.")

    choice = get_int("Enter choice (1-2): ", 1, 2)
    if choice == 1:
        search_by_roll()
    elif choice == 2:
        search_by_name()

# TOPPER
def topper_student():
    students = load_students()
    if not students:
        print("No students available.")
        return
    sorted_students = get_sorted_students(students)
    print("\nTopper of class\n")
    print(f"{'Rank':<10}{'Roll No':<13}{'Name':<16}",end="")
    for sub in subjects:
        print(f"{sub:<10}",end="")
    print(f"{'Total':<10}{'Obtained':<10}{'Per(%)':<10}{'Grade':<10}{'Status':<10}")
    print("="*160)
    
    top_per = sorted_students[0].percentage()

    for s in sorted_students:
        if s.percentage() == top_per:
            s.show_result(rank=1)
        else:
            break

def load_del_students():
    if not os.path.exists("deleted_data.json"):
        return []
    try:
        with open("deleted_data.json","r") as f:
            return json.load(f)
    except:
        return []

def move_to_recycle_bin(student_dict):
    data = load_del_students()
    data.append(student_dict)
    with open("deleted_data.json","w") as f:
        json.dump(data, f, indent=4)

# DELETING FULL STUDENT
def delete_student():
    students = load_students()

    rol = get_int("Enter student's roll no: ", 1, 10000)

    student_to_delete = None
    for s in students:
        if s.roll == rol:
            student_to_delete = s
            break
    if student_to_delete is None:
        print("Student not found.")
        return
    
    rank = get_rank(student_to_delete, students)
    print(f"{'Rank':<10}{'Roll No':<13}{'Name':<16}",end="")
    for sub in subjects:
        print(f"{sub:<10}",end="")
    print(f"{'Total':<10}{'Obtained':<10}{'Per(%)':<10}{'Grade':<10}{'Status':<10}")
    print("="*160)
    student_to_delete.show_result(rank)

    choice = get_clear("Are you sure you really want to delete this student's data?\nIt will be thrown to recycle bin!\n(yes or no): ")
    if choice == "yes":
            
        move_to_recycle_bin(student_to_delete.to_dict())

        students = [s for s in students if s.roll != rol]
        save_students(students)
        print("Student Deleted Succesfully!")
    else:
        print("Deletion Canceled.")

def recycle():
    students = load_students()
    deleted = load_del_students()
    if not deleted:
        print("Recycle bin is empty.")
        return
    deleted_students = [Student.from_dict(s) for s in deleted]
    print(f"{'Rank':<10}{'Roll No':<13}{'Name':<16}",end="")
    for sub in subjects:
        print(f"{sub:<10}",end="")
    print(f"{'Total':<10}{'Obtained':<10}{'Per(%)':<10}{'Grade':<10}{'Status':<10}")
    print("="*160)
    for d in deleted_students:
        d.show_result("-")
    
    choice = get_clear("Do you want to recover any student's data? (yes or no): ")
    if choice == "yes":
        roll = get_int("Enter the roll no of student you want to recover: ", 1, 10000)
        student_data = next((d for d in deleted if d["roll"] == roll ), None)
        if student_data is None:
            print("This roll no does not exist in recycle bin\nPlease check again!")
            return
        
        if any(s.roll == roll for s in students):
            print("A student with this roll already exists!")
            return
        
        recovered = Student.from_dict(student_data)

        students.append(recovered)
        save_students(students)
        deleted = [d for d in deleted if d["roll"] != roll]
        
        with open("deleted_data.json","w") as f:
            json.dump(deleted, f, indent=4)
    else:
        return

def delete_from_recycle_bin():
    deleted = load_del_students()
    if not deleted:
        print("Recycle bin is empty.")
        return
    deleted_students = [Student.from_dict(s) for s in deleted]
    print(f"{'Rank':<10}{'Roll No':<13}{'Name':<16}",end="")
    for sub in subjects:
        print(f"{sub:<10}",end="")
    print(f"{'Total':<10}{'Obtained':<10}{'Per(%)':<10}{'Grade':<10}{'Status':<10}")
    print("="*160)
    for d in deleted_students:
        d.show_result("-")

    choice = get_clear("Do you want to delete any student's data permanently from recycle bin? (yes or no): ")
    if choice == "yes":
        rol = get_int("Enter the student's roll no you want to delete his data: ")
        if not any(s["roll"] == rol for s in deleted):
            print(f"The Student with the roll no {rol} does not exist in recycle bin!")
            return
        remaining = []
        for s in deleted:
            if s["roll"] == rol:
                continue
            remaining.append(s)
        
        with open("deleted_data.json","w") as f:
            json.dump(remaining, f, indent=4)
    else:
        return

def rename():
    students = load_students()

    rol = get_int("Enter student's roll no: ", 1, 10000)
    replacing = get_name("Enter new name: ", 1, 14)
    found = False

    for s in students:
        if s.roll == rol:
            s.name = replacing
            found = True
            break
    if found:
       print("Replaced successfully.")
    else:
        print("Student not found")

    save_students(students) 


# MENU
def menu():
    while True:
        print("\n======MENU======")
        print("1. Add students")
        print("2. Show class result.")
        print("3. Search student.")
        print("4. Show Topper.")
        print("5. Move to recycle bin.")
        print("6. Recycle student's data.")
        print("7. Replacing a name.")
        print("8. Delete permanently from recycle bin.")
        print("9. Exit.")

        get_choice = get_int("Enter choice (1-9): ", 1, 9)

        if get_choice == 1:
            add_students()
        elif get_choice == 2:
            show_class_result()
        elif get_choice == 3:
            search_student()
        elif get_choice == 4:
            topper_student()
        elif get_choice == 5:
            delete_student()
        elif get_choice == 6:
            recycle()
        elif get_choice == 7:
            rename()
        elif get_choice == 8:
            delete_from_recycle_bin()
        elif get_choice == 9:
            print("Goodbye!")
            break
menu()