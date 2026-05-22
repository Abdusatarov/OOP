"""
============================================================
  СИСТЕМА УЧЁТА СТУДЕНТОВ
  Итоговый проект | ООП (SFT6002-105-L)
  Демонстрирует: Абстракцию, Инкапсуляцию,
                 Наследование, Полиморфизм
============================================================
"""

from abc import ABC, abstractmethod
from datetime import datetime
import re


# ─────────────────────────────────────────────
#  УРОВЕНЬ 1 — АБСТРАКЦИЯ
#  Абстрактный базовый класс, определяющий общий
#  интерфейс для всех "персон" в системе
# ─────────────────────────────────────────────

class Person(ABC):
    """
    Абстрактный базовый класс для всех персон в системе.
    Определяет общий интерфейс через абстрактные методы.
    """

    def __init__(self, name: str, email: str):
        # ИНКАПСУЛЯЦИЯ — приватные атрибуты с валидацией
        self._name = self._validate_name(name)
        self._email = self._validate_email(email)

    # ── Свойства (инкапсуляция: контролируемый доступ) ──

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

    # ── Вспомогательные методы валидации ──

    @staticmethod
    def _validate_name(name: str) -> str:
        name = name.strip()
        if not name or len(name) < 2:
            raise ValueError("Имя должно содержать минимум 2 символа.")
        return name

    @staticmethod
    def _validate_email(email: str) -> str:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        if not re.match(pattern, email):
            raise ValueError(f"Некорректный email адрес: '{email}'")
        return email.lower()

    # ── Абстрактные методы (должны быть реализованы в наследниках) ──

    @abstractmethod
    def role(self) -> str:
        """Вернуть роль человека."""
        pass

    @abstractmethod
    def get_summary(self) -> str:
        """Вернуть краткое описание."""
        pass

    # ── Конкретный метод (ПОЛИМОРФИЗМ — используется наследниками) ──

    def show_info(self) -> str:
        """Показ информации. Использует role() — полиморфное поведение."""
        divider = "─" * 40
        return (
            f"\n{divider}\n"
            f"  Роль   : {self.role()}\n"
            f"  Имя    : {self._name}\n"
            f"  Email  : {self._email}\n"
            f"{self.get_summary()}"
            f"{divider}"
        )

    def __str__(self) -> str:
        return f"{self.role()} | {self._name} <{self._email}>"


# ─────────────────────────────────────────────
#  УРОВЕНЬ 2 — НАСЛЕДОВАНИЕ + ИНКАПСУЛЯЦИЯ
#  Конкретные подклассы Person
# ─────────────────────────────────────────────

class Student(Person):
    """
    Представляет студента.
    Наследуется от Person, добавляет student_id и оценки.
    """

    # Счётчик для автоматической генерации ID
    _id_counter: int = 1000

    def __init__(self, name: str, email: str, major: str, year: int):
        super().__init__(name, email)

        # Генерация уникального ID студента
        Student._id_counter += 1
        self.__student_id: int = Student._id_counter
        self._major: str = self._validate_major(major)
        self._year: int = self._validate_year(year)
        self._grades: dict[str, float] = {}  # {предмет: оценка}
        self._registered_at: str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── Свойства ──

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
        return dict(self._grades)

    # ── Валидация ──

    @staticmethod
    def _validate_major(major: str) -> str:
        major = major.strip()
        if not major or len(major) < 2:
            raise ValueError("Специальность должна содержать минимум 2 символа.")
        return major

    @staticmethod
    def _validate_year(year: int) -> int:
        if not isinstance(year, int) or year < 1 or year > 6:
            raise ValueError("Курс должен быть числом от 1 до 6.")
        return year

    # ── Управление оценками ──

    def add_grade(self, subject: str, grade: float):
        """Добавить или обновить оценку по предмету."""
        subject = subject.strip()
        if not subject:
            raise ValueError("Название предмета не может быть пустым.")
        if not (0.0 <= grade <= 100.0):
            raise ValueError(f"Оценка должна быть от 0 до 100. Получено: {grade}")
        self._grades[subject] = round(grade, 1)

    def remove_grade(self, subject: str):
        """Удалить оценку по предмету."""
        if subject not in self._grades:
            raise KeyError(f"Предмет '{subject}' не найден.")
        del self._grades[subject]

    def average_grade(self) -> float:
        """Средний балл (GPA)."""
        if not self._grades:
            return 0.0
        return round(sum(self._grades.values()) / len(self._grades), 2)

    def letter_grade(self) -> str:
        """Преобразование GPA в буквенную оценку."""
        avg = self.average_grade()
        if avg >= 90:   return "A"
        elif avg >= 75: return "B"
        elif avg >= 60: return "C"
        elif avg >= 50: return "D"
        else:           return "F"

    # ── Реализация абстрактных методов ──

    def role(self) -> str:
        return "Студент"

    def get_summary(self) -> str:
        avg = self.average_grade()
        grade_str = f"{avg:.2f} ({self.letter_grade()})" if self._grades else "Нет оценок"
        subjects = ", ".join(self._grades.keys()) if self._grades else "—"
        return (
            f"  ID     : STU-{self.__student_id}\n"
            f"  Спец.  : {self._major}  (Курс {self._year})\n"
            f"  GPA    : {grade_str}\n"
            f"  Предм. : {subjects}\n"
            f"  Рег.   : {self._registered_at}\n"
        )

    def __repr__(self) -> str:
        return (f"Student(id=STU-{self.__student_id}, name='{self._name}', "
                f"major='{self._major}', year={self._year}, gpa={self.average_grade()})")


class Teacher(Person):
    """
    Представляет преподавателя.
    """

    def __init__(self, name: str, email: str, department: str):
        super().__init__(name, email)
        self._department: str = department.strip()
        self._courses: list[str] = []

    @property
    def department(self) -> str:
        return self._department

    def assign_course(self, course: str):
        """Назначить курс преподавателю."""
        course = course.strip()
        if course and course not in self._courses:
            self._courses.append(course)

    def role(self) -> str:
        return "Преподаватель"

    def get_summary(self) -> str:
        courses = ", ".join(self._courses) if self._courses else "—"
        return (
            f"  Каф.   : {self._department}\n"
            f"  Курсы  : {courses}\n"
        )


class Administrator(Person):
    """
    Администратор системы.
    """

    def __init__(self, name: str, email: str, access_level: int = 1):
        super().__init__(name, email)
        self._access_level = max(1, min(3, access_level))

    @property
    def access_level(self) -> int:
        return self._access_level

    def role(self) -> str:
        return "Администратор"

    def get_summary(self) -> str:
        return f"  Доступ : Уровень {self._access_level}\n"


# ─────────────────────────────────────────────
#  УРОВЕНЬ 3 — СИСТЕМА (ФАСАД / МЕНЕДЖЕР)
# ─────────────────────────────────────────────

class StudentManagementSystem:
    """
    Основной класс управления системой.
    """

    def __init__(self, institution_name: str = "Университет"):
        self._institution: str = institution_name
        self._students: list[Student] = []

    # ───────────── Регистрация ─────────────

    def register_student(self, name: str, email: str,
                         major: str, year: int) -> Student:
        """Регистрация нового студента."""
        if self._find_by_email(email):
            raise ValueError(f"Студент с email '{email}' уже существует.")
        student = Student(name, email, major, year)
        self._students.append(student)
        print(f"  ✅  Зарегистрирован: {student}")
        return student

    # ───────────── Поиск ─────────────

    def search_by_name(self, query: str) -> list[Student]:
        """Поиск по имени."""
        query = query.strip().lower()
        return [s for s in self._students if query in s.name.lower()]

    def search_by_major(self, major: str) -> list[Student]:
        """Поиск по специальности."""
        major = major.strip().lower()
        return [s for s in self._students if major in s.major.lower()]

    def search_by_id(self, student_id: int) -> Student | None:
        """Поиск по ID."""
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

    # ───────────── Сортировка ─────────────

    def sort_by_name(self, reverse: bool = False) -> list[Student]:
        return sorted(self._students, key=lambda s: s.name.lower(), reverse=reverse)

    def sort_by_gpa(self, reverse: bool = True) -> list[Student]:
        return sorted(self._students, key=lambda s: s.average_grade(), reverse=reverse)

    def sort_by_year(self, reverse: bool = False) -> list[Student]:
        return sorted(self._students, key=lambda s: s.year, reverse=reverse)

    # ───────────── Обновление ─────────────

    def update_student(self, student_id: int, **kwargs):
        """Обновление данных студента."""
        student = self.search_by_id(student_id)
        if not student:
            raise LookupError(f"Студент с ID {student_id} не найден.")

        updated_fields = []
        for key, value in kwargs.items():
            if hasattr(student, key):
                setattr(student, key, value)
                updated_fields.append(key)
            else:
                print(f"  ⚠️  Неизвестное поле '{key}' — пропущено.")

        if updated_fields:
            print(f"  ✏️  Обновлено [{', '.join(updated_fields)}] для {student.name}")

    # ───────────── Удаление ─────────────

    def delete_student(self, student_id: int) -> bool:
        """Удалить студента по ID."""
        student = self.search_by_id(student_id)
        if not student:
            raise LookupError(f"Студент с ID {student_id} не найден.")
        self._students.remove(student)
        print(f"  🗑️  Удалён: {student.name} (STU-{student_id})")
        return True

    # ───────────── Оценки ─────────────

    def add_grade(self, student_id: int, subject: str, grade: float):
        student = self.search_by_id(student_id)
        if not student:
            raise LookupError(f"Студент с ID {student_id} не найден.")
        student.add_grade(subject, grade)
        print(f"  📝  Добавлена оценка: {student.name} | {subject} = {grade}")

    # ───────────── Отчёты ─────────────

    def list_all(self) -> list[Student]:
        return list(self._students)

    def print_all(self, students: list[Student] | None = None):
        """Красивый вывод списка студентов."""
        target = students if students is not None else self._students
        if not target:
            print("  (Нет данных для отображения)")
            return
        for s in target:
            print(s.show_info())

    def statistics(self) -> dict:
        """Агрегированная статистика."""
        if not self._students:
            return {"count": 0}

        gpas = [s.average_grade() for s in self._students if s.grades]
        majors: dict[str, int] = {}
        years: dict[int, int] = {}

        for s in self._students:
            majors[s.major] = majors.get(s.major, 0) + 1
            years[s.year] = years.get(s.year, 0) + 1

        return {
            "count": len(self._students),
            "avg_gpa": round(sum(gpas) / len(gpas), 2) if gpas else 0.0,
            "top_student": max(self._students, key=lambda s: s.average_grade()),
            "majors": majors,
            "years": years,
        }

    def print_statistics(self):
        stats = self.statistics()
        print("\n" + "═" * 44)
        print(f"  📊  {self._institution} — Статистика")
        print("═" * 44)
        print(f"  Всего студентов : {stats['count']}")
        if stats['count'] > 0:
            print(f"  Средний GPA     : {stats['avg_gpa']}")
            top = stats['top_student']
            print(f"  Лучший студент  : {top.name} ({top.average_grade()})")
            print(f"\n  По специальностям:")
            for major, cnt in stats['majors'].items():
                print(f"    • {major:<25} {cnt} студент(ов)")
            print(f"\n  По курсам:")
            for yr in sorted(stats['years']):
                print(f"    • Курс {yr}: {stats['years'][yr]} студент(ов)")
        print("═" * 44)

    def __len__(self) -> int:
        return len(self._students)

    def __repr__(self) -> str:
        return f"StudentManagementSystem('{self._institution}', students={len(self)})"


# ─────────────────────────────────────────────
#  ДЕМО / MAIN
# ─────────────────────────────────────────────

def demo():
    banner = """
╔══════════════════════════════════════════════╗
║    СИСТЕМА УЧЁТА СТУДЕНТОВ — ДЕМО            ║
║    ООП проект | Итоговая работа             ║
╚══════════════════════════════════════════════╝"""
    print(banner)

    sms = StudentManagementSystem("Университет SDU")

    print("\n" + "─"*44)
    print("  [1] РЕГИСТРАЦИЯ СТУДЕНТОВ")
    print("─"*44)

    s1 = sms.register_student("Айдана Бекова", "aidana@sdu.edu.kz", "Информатика", 2)
    s2 = sms.register_student("Данияр Сейтқали", "daniyar@sdu.edu.kz", "Математика", 3)
    s3 = sms.register_student("Жансая Нурова", "zhansaya@sdu.edu.kz", "Информатика", 1)
    s4 = sms.register_student("Бауыржан Асанов", "bauyrzhan@sdu.edu.kz", "Физика", 4)
    s5 = sms.register_student("Алина Серова", "alina@sdu.edu.kz", "Математика", 2)

    print("\n" + "─"*44)
    print("  [2] ДОБАВЛЕНИЕ ОЦЕНОК")
    print("─"*44)

    sms.add_grade(s1.student_id, "ООП", 95.0)
    sms.add_grade(s1.student_id, "Алгоритмы", 88.5)
    sms.add_grade(s1.student_id, "Базы данных", 91.0)

    sms.add_grade(s2.student_id, "Матанализ", 76.0)
    sms.add_grade(s2.student_id, "Линейная алгебра", 82.0)

    sms.add_grade(s3.student_id, "ООП", 55.0)
    sms.add_grade(s3.student_id, "Математика", 62.0)

    sms.add_grade(s4.student_id, "Квантовая механика", 98.0)
    sms.add_grade(s4.student_id, "Оптика", 94.5)

    sms.add_grade(s5.student_id, "Матанализ", 70.0)
    sms.add_grade(s5.student_id, "Статистика", 85.0)

    print("\n" + "─"*44)
    print("  [3] СПИСОК ВСЕХ СТУДЕНТОВ")
    print("─"*44)
    sms.print_all()

    print("\n" + "─"*44)
    print("  [4] ПОИСК ПО ИМЕНИ: 'dan'")
    print("─"*44)
    results = sms.search_by_name("dan")
    sms.print_all(results)

    print("\n" + "─"*44)
    print("  [5] ПОИСК ПО СПЕЦИАЛЬНОСТИ: 'информатика'")
    print("─"*44)
    results = sms.search_by_major("информатика")
    sms.print_all(results)

    print("\n" + "─"*44)
    print("  [6] СОРТИРОВКА ПО GPA (лучшие первые)")
    print("─"*44)
    sorted_students = sms.sort_by_gpa()
    for i, st in enumerate(sorted_students, 1):
        grade_info = f"{st.average_grade():.2f} ({st.letter_grade()})"
        print(f"  {i}. {st.name:<25} GPA: {grade_info}")

    print("\n" + "─"*44)
    print("  [7] СОРТИРОВКА ПО КУРСУ")
    print("─"*44)
    sorted_students = sms.sort_by_year()
    for st in sorted_students:
        print(f"  Курс {st.year} | {st.name}")

    print("\n" + "─"*44)
    print("  [8] ОБНОВЛЕНИЕ ДАННЫХ СТУДЕНТА")
    print("─"*44)
    sms.update_student(s3.student_id, name="Жансая Нурова-Абенова", year=2)
    print(s3.show_info())

    print("\n" + "─"*44)
    print("  [9] УДАЛЕНИЕ СТУДЕНТА")
    print("─"*44)
    sms.delete_student(s5.student_id)
    print(f"  Осталось студентов: {len(sms)}")

    sms.print_statistics()

    print("\n" + "─"*44)
    print("  [11] ПОЛИМОРФИЗМ — иерархия Person")
    print("─"*44)
    print("  Создание смешанного списка объектов...\n")

    people: list[Person] = [
        Student("Нурсултан Омаров", "nursultan@sdu.edu.kz", "IT", 1),
        Teacher("Проф. Шаяхметова", "prof@sdu.edu.kz", "Информатика"),
        Administrator("Системный администратор", "admin@sdu.edu.kz", access_level=3),
    ]

    for person in people:
        print(person.show_info())

    print("\n" + "─"*44)
    print("  [12] ОБРАБОТКА ИСКЛЮЧЕНИЙ")
    print("─"*44)

    errors = [
        ("Дубликат email", lambda: sms.register_student("Test", "aidana@sdu.edu.kz", "IT", 1)),
        ("Неверный email", lambda: sms.register_student("Test", "not-email", "IT", 1)),
        ("Неверный курс", lambda: sms.register_student("Test", "test@x.com", "IT", 9)),
        ("Оценка вне диапазона", lambda: s1.add_grade("Test", 120.0)),
        ("Студент не найден", lambda: sms.search_by_id(9999) or (_ for _ in ()).throw(LookupError("Не найден"))),
    ]

    for label, action in errors:
        try:
            action()
        except (ValueError, LookupError, TypeError) as e:
            print(f"  ⛔  [{label}]: {e}")

    print("\n  ✅  Демонстрация завершена.\n")


if __name__ == "__main__":
    demo()