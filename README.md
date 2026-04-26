# 🎓 Student Management System — Учёт студентов

**Final Project | OOP (SFT6002-105-L)**

---

## 📁 Файлдар / Файлы

| Файл | Мазмұны |
|------|---------|
| `main.py` | Барлық класстар + демо функциясы |
| `cli.py`  | Интерактивті мәзір (терминал) |

---

## 🚀 Іске қосу / Запуск

```bash
# Демо (авто-демонстрация всех функций)
python main.py

# Интерактивное меню
python cli.py
```

---

## 🏗️ Архитектура классов

```
Person (ABC — абстрактный)
├── Student       ← основной класс
├── Teacher       ← расширяемость
└── Administrator ← расширяемость

StudentManagementSystem   ← управляет коллекцией Student
```

---

## 🔑 ООП-принципы

### 1. Абстракция (`ABC`)
`Person` — абстрактный базовый класс.  
Определяет **интерфейс** через абстрактные методы `role()` и `get_summary()`.  
Нельзя создать объект `Person` напрямую — только через наследников.

```python
class Person(ABC):
    @abstractmethod
    def role(self) -> str: ...

    @abstractmethod
    def get_summary(self) -> str: ...
```

---

### 2. Инкапсуляция
Все атрибуты скрыты через `_` и `__` префиксы.  
Доступ — только через `@property` с валидацией.

```python
class Student(Person):
    def __init__(self, ...):
        self.__student_id = ...   # name-mangled (полностью приватный)
        self._name = ...          # protected
        self._grades = {}         # внутреннее состояние

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self._validate_name(value)  # валидация
```

---

### 3. Наследование
`Student`, `Teacher`, `Administrator` наследуют от `Person`.  
Переиспользуют `__init__`, `show_info()`, валидаторы.

```python
class Student(Person):
    def __init__(self, name, email, major, year):
        super().__init__(name, email)   # вызов родителя
        ...

class Teacher(Person):
    def __init__(self, name, email, department):
        super().__init__(name, email)
        ...
```

---

### 4. Полиморфизм
`show_info()` определён в `Person` и вызывает `role()` / `get_summary()`.  
Каждый наследник реализует их по-своему — **один вызов, разное поведение**.

```python
people = [
    Student("Ali", "ali@x.com", "CS", 1),
    Teacher("Dana", "dana@x.com", "IT Dept"),
    Administrator("Admin", "admin@x.com", 3),
]

for person in people:
    print(person.show_info())   # ← одна строка, три разных вывода
```

---

## ✅ Реализованные функции

| Функция | Метод |
|---------|-------|
| Регистрация студента | `sms.register_student(...)` |
| Просмотр списка | `sms.print_all()` |
| Добавление оценки | `sms.add_grade(id, subject, grade)` |
| Поиск по имени | `sms.search_by_name(query)` |
| Поиск по специальности | `sms.search_by_major(query)` |
| Сортировка по GPA | `sms.sort_by_gpa()` |
| Сортировка по курсу | `sms.sort_by_year()` |
| Сортировка по имени | `sms.sort_by_name()` |
| Изменение данных | `sms.update_student(id, **kwargs)` |
| Удаление студента | `sms.delete_student(id)` |
| Статистика | `sms.print_statistics()` |

---

## 🛡️ Обработка исключений

- `ValueError` — неверные данные (email, имя, оценка вне 0–100)
- `LookupError` — студент не найден по ID
- `KeyError` — предмет не найден в оценках

---

## 📊 Оценивание (самооценка)

| Критерий | Реализация |
|----------|-----------|
| Архитектура | `Person → Student / Teacher / Admin`, `StudentManagementSystem` |
| ООП | Все 4 принципа с примерами в коде |
| Функциональность | 11 функций |
| Исключения | `ValueError`, `LookupError`, `KeyError` |
| Стиль | docstrings, type hints, PEP 8 |
