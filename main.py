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
            print(f"The name must contain more than {min} and less than {max} alphabets1")
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
        s.marks = data["marks"]
        return s
    
    def show_result(self, rank):
        p = self.percentage()
        g = self.grade()
        s = self.status()
        g_total = sum(total for obtained, total in self.marks.values())
        
        print(f"{rank:<10}{self.roll:<13}{self.name:<16}",end="")
        for subjects, (obtained, total_marks) in self.marks.items():
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

def get_rank(student):
    students = load_data()
    students = [Student.from_dict(s) for s in students]
    sorted_students = sorted(students, key = lambda s: s.percentage(), reverse = True)

    for i, s in enumerate(sorted_students, start=1):
        if s.roll == student.roll:
            return i
    return None

def get_sorted_students(students):
    return sorted(students, key=lambda s: s.percentage(), reverse=True)

def Add_students():
    students = load_data()
    students = [Student.from_dict(s) for s in students]
    while True:
        roll = get_int("Enter student's Roll no: ", 1, 10000)
        name = get_name("Enter student's name: ", 3, 14)
        s = Student(roll, name)

        for sub in subjects:
            total = get_int(f"Enter total marks of {sub}: ", 1, 100)
            obtained = get_int(f"Enter obtained marks of {sub}: ", 0, total)
            s.add_marks(sub, obtained, total)
        students.append(s)

        clearify = get_clear("Add another student ('yes' or 'no')?")
        if clearify == "no":
            break
    save_data([s.to_dict() for s in students])

def failed(students):
    c = 0
    for s in students:
        if s.percentage() < 33:
            c += 1
    return c

def show_class_result():

    students = load_data()
    students = [Student.from_dict(s) for s in students]
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
            rank = get_rank(s)
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

    students = load_data()
    students = [Student.from_dict(s) for s in students]
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
                rank = get_rank(s)
                s.show_result(rank)
                return
        print("Student not found.")
    else:
        print("No students are available.")

def search_by_name():

    students = load_data()
    students = [Student.from_dict(s) for s in students]

    if not students:
        print("No students are available.")
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
            rank = get_rank(s)
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
    students = load_data()
    students = ([Student.from_dict(s) for s in students])
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
    sorted_students[0].show_result(1)

# DELETING FULL STUDENT
def delete_student():
    students = load_data()
    students = [Student.from_dict(s) for s in students]

    rol = get_int("Enter student's roll no: ", 1, 10000)
    updated_students = []
    found = False

    for s in students:
        if s.roll == rol:
            found = True
            continue
        updated_students.append(s)
    
    if found:
        print("Student deleted successfully!")
    else:
        print("Student not found")
    
    save_data([s.to_dict() for s in updated_students])

def replace_name():
    students = load_data()
    students = [Student.from_dict(s) for s in students]

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

    save_data([s.to_dict() for s in students]) 


# MENU
def Menu():
    while True:
        print("\n======MENU======")
        print("1. Add students")
        print("2. Show class result.")
        print("3. Search student.")
        print("4. Show Topper.")
        print("5. Delete student.")
        print("6. Replacing a name.")
        print("7. Exit.")

        get_choice = get_int("Enter choice (1-7): ", 1, 7)

        if get_choice == 1:
            Add_students()
        elif get_choice == 2:
            show_class_result()
        elif get_choice == 3:
            search_student()
        elif get_choice == 4:
            topper_student()
        elif get_choice == 5:
            delete_student()
        elif get_choice == 6:
            replace_name()
        elif get_choice == 7:
            print("Goodbye!")
            break
Menu()