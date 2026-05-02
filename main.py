def get_text(prompt):
    while True:
        text = input(prompt).strip()
        if not text:
            print("Input cannot be empty!")
            continue
        return text

def get_name(prompt, min, max):
    while True:
        name = get_text(prompt)
        if min <= len(name) <= max:
            return name
        else:
            print(f"The name should be between {min} and {max} characters!")
            continue

def get_int(prompt, min, max):
    while True:
        num = get_text(prompt)
        try:
            num = int(num)
            if min <= num <= max:
                return num
            print(f"The number must be between {min} and {max}!")
        except ValueError:
            print("Enter a valid number!")

def get_clear(prompt):
    while True:
        clearify = get_text(prompt).lower()
        if clearify in ("yes", "no"):
            return clearify
        print("Reply in yes or no!")

class Student():
    def __init__(self, roll, name):
        self.roll = roll
        self.name = name
        self.marks = {}

    def add_marks(self, subject, obtained, total):
        self.marks[subject] = (obtained, total)
    
    def percentage(self):
        total = sum(total for _, total in self.marks.values())
        obtained = sum(obtain for obtain, _ in self.marks.values())
        if total == 0:
            return 0
        return (obtained/total) * 100
    
    def grade(self):
        p = self.percentage()
        if p >= 90:
            return "A+"
        elif p >= 80:
            return "A"
        elif p >= 65:
            return "B"
        elif p >= 50:
            return "C"
        elif p >= 33:
            return "D"
        else:
            return "F"
    
    def status(self):
        for obtained, total in self.marks.values():
            if total == 0:
                continue
            if (obtained / total)*100 < 33 :
                return "FAIL"
        return "PASS"
    
    def show_result(self, rank):
        t = sum(t for o, t in self.marks.values())
        o = sum(o for o, t in self.marks.values())
        p = str(round(self.percentage(), 2)) + "%"
        print(f"{rank:<10}{self.roll:<10}{self.name:<20}", end="")
        for sub, (obtained, total) in self.marks.items():
            print(f"{obtained:<3}/{total:<6}", end="")
        print(f"{t:<10}{o:<10}{p:<10}{self.grade():<10}{self.status():<10}")
    
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

def get_sorted(data):
    return sorted(data, key=lambda x: x.percentage(), reverse=True)

def get_rank(student, data):
    data = get_sorted(data)
    rank = 0
    prev_per = None

    for s in data:
        current_per = s.percentage()
        if current_per != prev_per:
            rank += 1
        if s.roll == student.roll:
            return rank
        prev_per = current_per

import json
import os
def load_data():
    if not os.path.exists("students_data.json"):
        return []
    try:
        with open("students_data.json","r") as p:
            data =  json.load(p)
            return [Student.from_dict(s) for s in data]
    except:
        return []

def save_data(data):
    with open("students_data.json","w") as p:
        data = [s.to_dict() for s in data]
        json.dump(data, p, indent=4)

subjects = ["Math", "Urdu", "Phy", "Eng", "Isl", "Chem", "Com/Bio"]
def add_student():
    students = load_data()
    while True:

        roll = get_int("Roll No: ", 1, 10000)
        if any(s.roll == roll for s in students):
            print("Roll No already exist!")
            return
        name = get_name("Name: ", 3, 17)
        s = Student(roll, name)
        for sub in subjects:
            t = get_int(f"{sub}'s total marks: ", 1, 100)
            o = get_int(f"{sub}'s obtained marks: ", 0, t)
            s.add_marks(sub, o, t)
        students.append(s)

        choice = get_clear("Add another student? (yes or no): ")
        if choice == "no":
            save_data(students)
            return

def topper(data):
    return [t for t in data if get_rank(t, data) == 1]

def failed(data):
    return [f for f in data if f.status() == "FAIL"]

def print_header():
    print(f"{'Rank':<10}{'Roll No':<10}{'Name':<20}", end="")
    for sub in subjects:
        print(f"{sub:<10}", end="")
    print(f"{'Total':<10}{'Obtained':<10}{'Per(%)':<10}{'Grade':<10}{'Status':<10}")
    print("="*160)

def show_toppers():
    data = load_data()
    if not data:
        print("No students are available!")
        return
    top_data = topper(data)
    print_header()
    for t in top_data:
        t.show_result(rank=1)
        print("-"*160)
    print("="*160)

def show_failed():
    data = load_data()
    if not data:
        print("No students are available!")
        return
    fail_data = failed(data)
    print_header()
    for f in fail_data:
        rank = get_rank(f, data)
        f.show_result(rank)
        print("-"*160)
    print("="*160)

def show_class_result():
    students = load_data()
    if not students:
        print("NO students are available!")
        return

    print(f"{'='*65}  C L A S S      R E S U L T  {'='*65}")
    print(f"{'Students: ' + str(len(students)):^160}")
    print_header()
    for s in students:
        rank = get_rank(s, students)
        s.show_result(rank)
        print('-'*160)
    print("="*160)
    print(f"First Rank: {len(topper(students))}")
    print(f"Failed: {len(failed(students))}")
    print("="*160)

def search_by_name():
    data = load_data()
    if not data:
        print("No students are available!")
        return

    name = get_name("Name: ", 1, 17)
    for s in data:
        if name.lower() in s.name.lower():
            print_header()
            rank = get_rank(s, data)
            s.show_result(rank)
            print("-"*160)
    print("="*160)

def search_by_roll():
    data = load_data()
    if not data:
        print("No students are available!")
        return

    roll = get_int("Roll NO: ", 1, 10000)
    if not any(s.roll == roll for s in data):
        print("Student with this roll no does not exist!")
        return
    print_header()
    for s in data:
        if s.roll == roll:
            rank = get_rank(s, data)
            s.show_result(rank)
            print("-"*160)
    print("="*160)

def load_deleted_data():
    if not os.path.exists("deleted_data.json"):
        return []
    try:
        with open("deleted_data.json", "r") as d:
            data = json.load(d)
            return [Student.from_dict(d) for d in data]
    except:
        return []

def save_deleted_data(data):
    deleted = load_deleted_data()
    deleted.append(data)
    with open("deleted_data.json", "w") as d:
        correct_data = [d.to_dict() for d in deleted]
        json.dump(correct_data, d, indent=4)

def move_to_recycle_bin():
    data = load_data()
    if not data:
        print("No students are available!")
        return
    
    roll = get_int("Roll No: ", 1, 10000)
    if not any(s.roll == roll for s in data):
        print("Student with this roll no does not exist!")
        return
    
    updated_data = []
    for s in data:
        if s.roll == roll:
            print_header()
            rank = get_rank(s, data)
            s.show_result(rank)
            print("="*160)
            choice = get_clear("Are sure! You really want to move this student's data to recycle bin!\nIf you needed it you can recycle from recycle bin!\n\t")
            if choice == "no":
                print("Deletion Canceled!")
                return
            save_deleted_data(s)
        if s.roll != roll:
            updated_data.append(s)
    save_data(updated_data)

def recycle_bin():
    deleted = load_deleted_data()
    if not deleted:
        print("Recycle bin is empty!")
        return
    print_header()
    for d in deleted:
        d.show_result("-")
        print("-"*160)
    print("="*160)

def delete_permanently():
    deleted = load_deleted_data()
    if not deleted:
        print("Recycle bin is empty!")
        return
    roll = get_int("Roll No: ", 1, 10000)

    if not any(d.roll == roll for d in deleted):
        print("The student with this roll no does not exist in reclye bin!")
        return
    
    remaining = []
    
    for d in deleted:
        if d.roll == roll:
            print_header()
            d.show_result("-")
            print("-"*160)
            choice = get_clear("Do you really want to delete this student's data permanently?\nOnce it is deleted from recle bin it can never be recovered!\n\t")
            if choice == "no":
                print("Deletion Canceled!")
                return
            continue
        remaining.append(d)
    with open("deleted_data.json", "w") as f:
        json.dump([d.to_dict() for d in remaining], f, indent=4)

def clear_recycle_bin():
    choice = get_clear("Do you really want to delete this all the data permanently?\nOnce it is deleted from recle bin it can never be recovered!\n\t")
    if choice == "no":
        return
    with open("deleted_data.json", "w") as d:
        json.dump([], d)

def recycle():

    data = load_data()
    deleted = load_deleted_data()
    
    if not deleted:
        print("Recycle bin is empty!")
        return
    print_header()
    for d in deleted:
        d.show_result("-")
        print("-"*160)
    print("="*160)
    
    roll = get_int("Roll No: ", 1, 10000)
    student = next((s for s in deleted if s.roll == roll), None)
    if student is None:
        print("The student with this roll no does not exist in recucle bin\nPlease check again!")
        return
    if any(s.roll == roll for s in data):
        print("Student with this roll no also exist in student data!")
        return

    print_header()
    student.show_result("-")
    print("="*160)

    choice = get_clear("Do you really want to recycle this data? (yes or no): ")
    if choice == "no":
        print("Recyling Canceled!")
        return

    data.append(student)
    save_data(data)
    data_to_recover = [obj for obj in deleted if obj.roll != roll]
    data_to_recover = [dl.to_dict() for dl in data_to_recover]
    with open("deleted_data.json", "w") as f:
        json.dump(data_to_recover, f, indent=4)
        print("Student successfully recovered!")

def rename():
    data = load_data()
    if not data:
        print("No students are available!")
        return
    
    roll = get_int("Roll No: ", 1, 10000)
    names = next((n for n in data if n.roll == roll), None)
    if names is None:
        print("Student not found!")
        return
    new_name = get_name("New Name: ", 3, 17)
    print_header()
    rank = get_rank(names, data)
    names.show_result(rank)
    print("="*160)
    choice = get_clear("\nDo you really want to rename this student? (yes or no): ")
    if choice == "no":
        print("Renaming Canceled!")
        return
    names.name = new_name
    save_data(data)
    print("Student renamed successfully!")

def change_marks():
    data = load_data()

    if not data:
        print("No students are available!")
        return
    roll = get_int("Roll No: ", 1, 10000)
    student = next((s for s in data if s.roll == roll), None)
    
    if student is None:
        print("Student with this roll no does not exist!")
        return
    
    while True:
        sub = get_text("Subject: ")
        subject = next((subj for subj in subjects if subj == sub), None)
        if subject is None:
            print("Subject name should be like('Math', 'Urdu', 'Phy', 'Eng', 'Isl', 'Chem', 'Com/Bio')")
            continue
        t = get_int(f"Total marks of {subject}: ", 1, 100)
        o = get_int(f"Obtained marks of {subject}: ", 0, t)
        student.marks[subject] = (o, t)
        break
    save_data(data)

def menu():
    print(f"{'='*20}{'Menu'}{'='*20}")
    print("1.  Add student.")
    print("2.  Show Class Result.")
    print("3.  Show toppers.")
    print("4.  Show failed students.")
    print("5.  Search student by roll no.")
    print("6.  Search student by name.")
    print("7.  Move to recycle bin.")
    print("8.  Recycle bin.")
    print("9.  Delete permanently from recycle bin.")
    print("10. Clear recycle bin.")
    print("11. Recycle student from recycle bin.")
    print("12. Rename student.")
    print("13. Change marks.")
    print("14. Exit.")
    print("="*44)

    while True:
        choice = get_int("Enter a number (1-14): ", 1, 14)
        if choice == 1:
            add_student()
        elif choice == 2:
            show_class_result()
        elif choice == 3:
            show_toppers()
        elif choice == 4:
            show_failed()
        elif choice == 5:
            search_by_roll()
        elif choice == 6:
            search_by_name()
        elif choice == 7:
            move_to_recycle_bin()
        elif choice == 8:
            recycle_bin()
        elif choice == 9:
            delete_permanently()
        elif choice == 10:
            clear_recycle_bin()
        elif choice == 11:
            recycle()
        elif choice == 12:
            rename()
        elif choice == 13:
            change_marks()
        elif choice == 14:
            print("Goodbye!")
            break
menu()