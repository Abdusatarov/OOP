"""
============================================================
  STUDENT MANAGEMENT SYSTEM — Учёт студентов
  Final Project | OOP (SFT6002-105-L)
  Demonstrates: Abstraction, Encapsulation,
                Inheritance, Polymorphism
============================================================
"""

from abc import ABC, abstractmethod
from datetime import datetime
import re


# ─────────────────────────────────────────────
#  LAYER 1 — ABSTRACTION
#  Abstract base class that defines a common
#  interface for all "persons" in the system
# ─────────────────────────────────────────────

class Person(ABC):
    """
    Abstract base class for all persons in the system.
    Defines the common interface via abstract methods.
    """

    def __init__(self, name: str, email: str):
        # ENCAPSULATION — private attributes with validation
        self._name = self._validate_name(name)
        self._email = self._validate_email(email)

    # ── Properties (Encapsulation: controlled access) ──

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = self._validate_name(value)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = self._validate_email(value)

    # ── Validation helpers ──

    @staticmethod
    def _validate_name(name: str) -> str:
        name = name.strip()
        if not name or len(name) < 2:
            raise ValueError("Name must be at least 2 characters long.")
        return name

    @staticmethod
    def _validate_email(email: str) -> str:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        if not re.match(pattern, email):
            raise ValueError(f"Invalid email address: '{email}'")
        return email.lower()

    # ── Abstract methods (must be implemented by subclasses) ──

    @abstractmethod
    def role(self) -> str:
        """Return the role of this person."""
        pass

    @abstractmethod
    def get_summary(self) -> str:
        """Return a short summary string."""
        pass

    # ── Concrete method (POLYMORPHISM — reused by subclasses) ──

    def show_info(self) -> str:
        """Display info. Uses role() — polymorphic behaviour."""
        divider = "─" * 40
        return (
            f"\n{divider}\n"
            f"  Role   : {self.role()}\n"
            f"  Name   : {self._name}\n"
            f"  Email  : {self._email}\n"
            f"{self.get_summary()}"
            f"{divider}"
        )

    def __str__(self) -> str:
        return f"{self.role()} | {self._name} <{self._email}>"


# ─────────────────────────────────────────────
#  LAYER 2 — INHERITANCE + ENCAPSULATION
#  Concrete subclasses of Person
# ─────────────────────────────────────────────

class Student(Person):
    """
    Represents a student.
    Inherits from Person, adds student_id and grades.
    """

    # Class-level counter for auto-generating IDs
    _id_counter: int = 1000

    def __init__(self, name: str, email: str, major: str, year: int):
        super().__init__(name, email)

        # Auto-generate unique student ID
        Student._id_counter += 1
        self.__student_id: int = Student._id_counter      # name-mangled (private)
        self._major: str = self._validate_major(major)
        self._year: int = self._validate_year(year)
        self._grades: dict[str, float] = {}               # {subject: grade}
        self._registered_at: str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── Properties ──

    @property
    def student_id(self) -> int:
        return self.__student_id

    @property
    def major(self) -> str:
        return self._major

    @major.setter
    def major(self, value: str):
        self._major = self._validate_major(value)

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, value: int):
        self._year = self._validate_year(value)

    @property
    def grades(self) -> dict:
        return dict(self._grades)   # return a copy — protect internal state

    # ── Validation helpers ──

    @staticmethod
    def _validate_major(major: str) -> str:
        major = major.strip()
        if not major or len(major) < 2:
            raise ValueError("Major must be at least 2 characters.")
        return major

    @staticmethod
    def _validate_year(year: int) -> int:
        if not isinstance(year, int) or year < 1 or year > 6:
            raise ValueError("Year must be an integer between 1 and 6.")
        return year

    # ── Grade management ──

    def add_grade(self, subject: str, grade: float):
        """Add or update a grade for a subject."""
        subject = subject.strip()
        if not subject:
            raise ValueError("Subject name cannot be empty.")
        if not (0.0 <= grade <= 100.0):
            raise ValueError(f"Grade must be between 0 and 100. Got: {grade}")
        self._grades[subject] = round(grade, 1)

    def remove_grade(self, subject: str):
        """Remove a grade entry."""
        if subject not in self._grades:
            raise KeyError(f"Subject '{subject}' not found in grades.")
        del self._grades[subject]

    def average_grade(self) -> float:
        """Calculate GPA (average of all grades)."""
        if not self._grades:
            return 0.0
        return round(sum(self._grades.values()) / len(self._grades), 2)

    def letter_grade(self) -> str:
        """Convert average to letter grade."""
        avg = self.average_grade()
        if avg >= 90:   return "A"
        elif avg >= 75: return "B"
        elif avg >= 60: return "C"
        elif avg >= 50: return "D"
        else:           return "F"

    # ── Abstract method implementations (POLYMORPHISM) ──

    def role(self) -> str:
        return "Student"

    def get_summary(self) -> str:
        avg = self.average_grade()
        grade_str = f"{avg:.2f} ({self.letter_grade()})" if self._grades else "No grades yet"
        subjects = ", ".join(self._grades.keys()) if self._grades else "—"
        return (
            f"  ID     : STU-{self.__student_id}\n"
            f"  Major  : {self._major}  (Year {self._year})\n"
            f"  GPA    : {grade_str}\n"
            f"  Subj.  : {subjects}\n"
            f"  Reg.   : {self._registered_at}\n"
        )

    def __repr__(self) -> str:
        return (f"Student(id=STU-{self.__student_id}, name='{self._name}', "
                f"major='{self._major}', year={self._year}, gpa={self.average_grade()})")


class Teacher(Person):
    """
    Represents a teacher.
    Inherits from Person — demonstrates extensibility of the hierarchy.
    """

    def __init__(self, name: str, email: str, department: str):
        super().__init__(name, email)
        self._department: str = department.strip()
        self._courses: list[str] = []

    @property
    def department(self) -> str:
        return self._department

    def assign_course(self, course: str):
        """Assign a course to the teacher."""
        course = course.strip()
        if course and course not in self._courses:
            self._courses.append(course)

    # ── Abstract method implementations (POLYMORPHISM) ──

    def role(self) -> str:
        return "Teacher"

    def get_summary(self) -> str:
        courses = ", ".join(self._courses) if self._courses else "—"
        return (
            f"  Dept.  : {self._department}\n"
            f"  Courses: {courses}\n"
        )


class Administrator(Person):
    """
    Represents a system administrator.
    Third branch of the Person hierarchy.
    """

    def __init__(self, name: str, email: str, access_level: int = 1):
        super().__init__(name, email)
        self._access_level = max(1, min(3, access_level))  # clamp 1–3

    @property
    def access_level(self) -> int:
        return self._access_level

    # ── Abstract method implementations (POLYMORPHISM) ──

    def role(self) -> str:
        return "Administrator"

    def get_summary(self) -> str:
        return f"  Access : Level {self._access_level}\n"


# ─────────────────────────────────────────────
#  LAYER 3 — SYSTEM CLASS (Facade / Manager)
#  StudentManagementSystem orchestrates all
#  operations on the student registry.
# ─────────────────────────────────────────────

class StudentManagementSystem:
    """
    Core management class.
    Stores and manipulates Student records.
    """

    def __init__(self, institution_name: str = "University"):
        self._institution: str = institution_name
        self._students: list[Student] = []     # private registry

    # ────────────── Registration ──────────────

    def register_student(self, name: str, email: str,
                         major: str, year: int) -> Student:
        """
        Register a new student.
        Raises ValueError if email already exists.
        """
        if self._find_by_email(email):
            raise ValueError(f"A student with email '{email}' is already registered.")
        student = Student(name, email, major, year)
        self._students.append(student)
        print(f"  ✅  Registered: {student}")
        return student

    # ────────────── Search ──────────────

    def search_by_name(self, query: str) -> list[Student]:
        """Case-insensitive partial name search."""
        query = query.strip().lower()
        return [s for s in self._students if query in s.name.lower()]

    def search_by_major(self, major: str) -> list[Student]:
        """Search by field of study."""
        major = major.strip().lower()
        return [s for s in self._students if major in s.major.lower()]

    def search_by_id(self, student_id: int) -> Student | None:
        """Find a student by their numeric ID."""
        for s in self._students:
            if s.student_id == student_id:
                return s
        return None

    def _find_by_email(self, email: str) -> Student | None:
        email = email.strip().lower()
        for s in self._students:
            if s.email == email:
                return s
        return None

    # ────────────── Sorting ──────────────

    def sort_by_name(self, reverse: bool = False) -> list[Student]:
        return sorted(self._students, key=lambda s: s.name.lower(), reverse=reverse)

    def sort_by_gpa(self, reverse: bool = True) -> list[Student]:
        """Sort by GPA — best students first by default."""
        return sorted(self._students, key=lambda s: s.average_grade(), reverse=reverse)

    def sort_by_year(self, reverse: bool = False) -> list[Student]:
        return sorted(self._students, key=lambda s: s.year, reverse=reverse)

    # ────────────── Update ──────────────

    def update_student(self, student_id: int, **kwargs):
        """
        Update one or more fields of a student record.
        Supported keys: name, email, major, year
        """
        student = self.search_by_id(student_id)
        if not student:
            raise LookupError(f"No student found with ID {student_id}.")

        updated_fields = []
        for key, value in kwargs.items():
            if hasattr(student, key):
                setattr(student, key, value)
                updated_fields.append(key)
            else:
                print(f"  ⚠️  Unknown field '{key}' — skipped.")

        if updated_fields:
            print(f"  ✏️  Updated [{', '.join(updated_fields)}] for {student.name}")

    # ────────────── Delete ──────────────

    def delete_student(self, student_id: int) -> bool:
        """Remove a student by ID. Returns True if deleted."""
        student = self.search_by_id(student_id)
        if not student:
            raise LookupError(f"No student found with ID {student_id}.")
        self._students.remove(student)
        print(f"  🗑️  Deleted: {student.name} (STU-{student_id})")
        return True

    # ────────────── Grades ──────────────

    def add_grade(self, student_id: int, subject: str, grade: float):
        student = self.search_by_id(student_id)
        if not student:
            raise LookupError(f"No student found with ID {student_id}.")
        student.add_grade(subject, grade)
        print(f"  📝  Grade added: {student.name} | {subject} = {grade}")

    # ────────────── Reports ──────────────

    def list_all(self) -> list[Student]:
        return list(self._students)

    def print_all(self, students: list[Student] | None = None):
        """Pretty-print a list of students (or all if none given)."""
        target = students if students is not None else self._students
        if not target:
            print("  (No records to display)")
            return
        for s in target:
            print(s.show_info())   # POLYMORPHISM — show_info() calls role() & get_summary()

    def statistics(self) -> dict:
        """Return aggregate statistics for the registry."""
        if not self._students:
            return {"count": 0}

        gpas = [s.average_grade() for s in self._students if s.grades]
        majors: dict[str, int] = {}
        years: dict[int, int] = {}
        for s in self._students:
            majors[s.major] = majors.get(s.major, 0) + 1
            years[s.year]   = years.get(s.year, 0) + 1

        return {
            "count":       len(self._students),
            "avg_gpa":     round(sum(gpas) / len(gpas), 2) if gpas else 0.0,
            "top_student": max(self._students, key=lambda s: s.average_grade()),
            "majors":      majors,
            "years":       years,
        }

    def print_statistics(self):
        stats = self.statistics()
        print("\n" + "═" * 44)
        print(f"  📊  {self._institution} — Statistics")
        print("═" * 44)
        print(f"  Total students : {stats['count']}")
        if stats['count'] > 0:
            print(f"  Average GPA    : {stats['avg_gpa']}")
            top = stats['top_student']
            print(f"  Top student    : {top.name} ({top.average_grade()})")
            print(f"\n  By major:")
            for major, cnt in stats['majors'].items():
                print(f"    • {major:<25} {cnt} student(s)")
            print(f"\n  By year:")
            for yr in sorted(stats['years']):
                print(f"    • Year {yr}: {stats['years'][yr]} student(s)")
        print("═" * 44)

    def __len__(self) -> int:
        return len(self._students)

    def __repr__(self) -> str:
        return f"StudentManagementSystem('{self._institution}', students={len(self)})"


# ─────────────────────────────────────────────
#  DEMO / MAIN — полная демонстрация системы
# ─────────────────────────────────────────────

def demo():
    banner = """
╔══════════════════════════════════════════════╗
║    STUDENT MANAGEMENT SYSTEM  —  DEMO        ║
║    Учёт студентов | Final Project OOP        ║
╚══════════════════════════════════════════════╝"""
    print(banner)

    sms = StudentManagementSystem("SDU University")

    # ── 1. Register students ──────────────────
    print("\n" + "─"*44)
    print("  [1] РЕГИСТРАЦИЯ СТУДЕНТОВ")
    print("─"*44)

    s1 = sms.register_student("Aidana Bekova",    "aidana@sdu.edu.kz",   "Computer Science", 2)
    s2 = sms.register_student("Daniyar Seitkali", "daniyar@sdu.edu.kz",  "Mathematics",       3)
    s3 = sms.register_student("Zhansaya Nurova",  "zhansaya@sdu.edu.kz", "Computer Science",  1)
    s4 = sms.register_student("Bauyrzhan Asanov", "bauyrzhan@sdu.edu.kz","Physics",           4)
    s5 = sms.register_student("Alina Serova",     "alina@sdu.edu.kz",    "Mathematics",       2)

    # ── 2. Add grades ─────────────────────────
    print("\n" + "─"*44)
    print("  [2] ДОБАВЛЕНИЕ ОЦЕНОК")
    print("─"*44)

    sms.add_grade(s1.student_id, "OOP",           95.0)
    sms.add_grade(s1.student_id, "Algorithms",    88.5)
    sms.add_grade(s1.student_id, "Databases",     91.0)

    sms.add_grade(s2.student_id, "Calculus",      76.0)
    sms.add_grade(s2.student_id, "Linear Algebra",82.0)

    sms.add_grade(s3.student_id, "OOP",           55.0)
    sms.add_grade(s3.student_id, "Math",          62.0)

    sms.add_grade(s4.student_id, "Quantum Mech",  98.0)
    sms.add_grade(s4.student_id, "Optics",        94.5)

    sms.add_grade(s5.student_id, "Calculus",      70.0)
    sms.add_grade(s5.student_id, "Statistics",    85.0)

    # ── 3. List all ───────────────────────────
    print("\n" + "─"*44)
    print("  [3] СПИСОК ВСЕХ СТУДЕНТОВ")
    print("─"*44)
    sms.print_all()

    # ── 4. Search by name ─────────────────────
    print("\n" + "─"*44)
    print("  [4] ПОИСК ПО ИМЕНИ: 'dan'")
    print("─"*44)
    results = sms.search_by_name("dan")
    sms.print_all(results)

    # ── 5. Search by major ────────────────────
    print("\n" + "─"*44)
    print("  [5] ПОИСК ПО СПЕЦИАЛЬНОСТИ: 'computer'")
    print("─"*44)
    results = sms.search_by_major("computer")
    sms.print_all(results)

    # ── 6. Sort by GPA ────────────────────────
    print("\n" + "─"*44)
    print("  [6] СОРТИРОВКА ПО GPA (лучшие первые)")
    print("─"*44)
    sorted_students = sms.sort_by_gpa()
    for i, st in enumerate(sorted_students, 1):
        grade_info = f"{st.average_grade():.2f} ({st.letter_grade()})"
        print(f"  {i}. {st.name:<25} GPA: {grade_info}")

    # ── 7. Sort by year ───────────────────────
    print("\n" + "─"*44)
    print("  [7] СОРТИРОВКА ПО КУРСУ")
    print("─"*44)
    sorted_students = sms.sort_by_year()
    for st in sorted_students:
        print(f"  Year {st.year} | {st.name}")

    # ── 8. Update student ─────────────────────
    print("\n" + "─"*44)
    print("  [8] ИЗМЕНЕНИЕ ДАННЫХ СТУДЕНТА")
    print("─"*44)
    sms.update_student(s3.student_id, name="Zhansaya Nurova-Abenova", year=2)
    print(s3.show_info())

    # ── 9. Delete student ─────────────────────
    print("\n" + "─"*44)
    print("  [9] УДАЛЕНИЕ СТУДЕНТА")
    print("─"*44)
    sms.delete_student(s5.student_id)
    print(f"  Total students remaining: {len(sms)}")

    # ── 10. Statistics ────────────────────────
    sms.print_statistics()

    # ── 11. POLYMORPHISM demo ─────────────────
    print("\n" + "─"*44)
    print("  [11] ПОЛИМОРФИЗМ — Person hierarchy")
    print("─"*44)
    print("  Creating a mixed list of Person subclasses...\n")

    people: list[Person] = [
        Student("Nursultan Omarov", "nursultan@sdu.edu.kz", "IT", 1),
        Teacher("Prof. Shayakhmetova", "prof@sdu.edu.kz", "Computer Science"),
        Administrator("Sys Admin", "admin@sdu.edu.kz", access_level=3),
    ]

    for person in people:
        # show_info() calls role() and get_summary()
        # Each subclass responds differently — POLYMORPHISM
        print(person.show_info())

    # ── 12. Exception handling demo ───────────
    print("\n" + "─"*44)
    print("  [12] ОБРАБОТКА ИСКЛЮЧЕНИЙ")
    print("─"*44)
    errors = [
        ("Duplicate email",  lambda: sms.register_student("Test User", "aidana@sdu.edu.kz", "IT", 1)),
        ("Invalid email",    lambda: sms.register_student("Test User", "not-an-email", "IT", 1)),
        ("Invalid year",     lambda: sms.register_student("Test User", "test@x.com", "IT", 9)),
        ("Grade out of range", lambda: s1.add_grade("Test", 120.0)),
        ("Student not found",  lambda: sms.search_by_id(9999) or (_ for _ in ()).throw(LookupError("Not found"))),
    ]

    for label, action in errors:
        try:
            action()
        except (ValueError, LookupError, TypeError) as e:
            print(f"  ⛔  [{label}]: {e}")

    print("\n  ✅  Demo complete.\n")


if __name__ == "__main__":
    demo()