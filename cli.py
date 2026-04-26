"""
============================================================
  ИНТЕРАКТИВНЫЙ CLI — СИСТЕМА УЧЁТА СТУДЕНТОВ
  Запуск: python cli.py
============================================================
"""

from main import StudentManagementSystem, Student


def hr(char="─", width=50):
    print(char * width)


def print_menu():
    hr("═")
    print("  СИСТЕМА УЧЁТА СТУДЕНТОВ")
    hr("═")
    print("  [1]  Регистрация нового студента")
    print("  [2]  Показать всех студентов")
    print("  [3]  Поиск по имени")
    print("  [4]  Поиск по специальности")
    print("  [5]  Добавить / обновить оценку")
    print("  [6]  Сортировка студентов")
    print("  [7]  Обновить данные студента")
    print("  [8]  Удалить студента")
    print("  [9]  Статистика")
    print("  [0]  Выход")
    hr()


def get_input(prompt: str, cast=str, optional=False):
    while True:
        val = input(f"  {prompt}: ").strip()
        if not val and optional:
            return None
        if not val:
            print("  ⚠️  Это поле обязательно.")
            continue
        try:
            return cast(val)
        except (ValueError, TypeError):
            print(f"  ⚠️  Неверный ввод, ожидается {cast.__name__}. Попробуйте снова.")


def run():
    sms = StudentManagementSystem("Университет SDU")

    # Заполнение тестовыми данными
    s1 = sms.register_student("Айдана Бекова", "aidana@sdu.edu.kz", "Информатика", 2)
    s2 = sms.register_student("Данияр Сейтқали", "daniyar@sdu.edu.kz", "Математика", 3)

    s1.add_grade("ООП", 95)
    s1.add_grade("Алгоритмы", 88)
    s2.add_grade("Матанализ", 76)
    s2.add_grade("Линейная алгебра", 82)

    print("  (Загружено 2 тестовых студента)\n")

    while True:
        print_menu()
        choice = input("  Выберите опцию: ").strip()

        try:
            # ── 1. Регистрация ──
            if choice == "1":
                print("\n  — Регистрация нового студента —")
                name  = get_input("ФИО")
                email = get_input("Email")
                major = get_input("Специальность / направление")
                year  = get_input("Курс (1-6)", int)
                sms.register_student(name, email, major, year)

            # ── 2. Список всех ──
            elif choice == "2":
                print(f"\n  — Все студенты ({len(sms)} всего) —")
                sms.print_all()

            # ── 3. Поиск по имени ──
            elif choice == "3":
                q = get_input("Введите имя (можно часть)")
                results = sms.search_by_name(q)
                print(f"\n  Найдено {len(results)} результат(ов):")
                sms.print_all(results)

            # ── 4. Поиск по специальности ──
            elif choice == "4":
                q = get_input("Введите специальность (можно часть)")
                results = sms.search_by_major(q)
                print(f"\n  Найдено {len(results)} результат(ов):")
                sms.print_all(results)

            # ── 5. Оценки ──
            elif choice == "5":
                sid     = get_input("ID студента (только число)", int)
                subject = get_input("Название предмета")
                grade   = get_input("Оценка (0-100)", float)
                sms.add_grade(sid, subject, grade)

            # ── 6. Сортировка ──
            elif choice == "6":
                print("  Сортировка: [1] Имя  [2] GPA  [3] Курс")
                sub = input("  Выбор: ").strip()
                if sub == "1":
                    sms.print_all(sms.sort_by_name())
                elif sub == "2":
                    sms.print_all(sms.sort_by_gpa())
                elif sub == "3":
                    sms.print_all(sms.sort_by_year())

            # ── 7. Обновление ──
            elif choice == "7":
                sid = get_input("ID студента (только число)", int)
                print("  Поля для изменения: name, email, major, year")
                print("  (Нажмите Enter, чтобы пропустить поле)")
                updates = {}

                for field in ("name", "email", "major"):
                    val = get_input(f"Новое значение {field}", optional=True)
                    if val:
                        updates[field] = val

                yr = get_input("Новый курс (1-6)", optional=True)
                if yr:
                    updates["year"] = int(yr)

                if updates:
                    sms.update_student(sid, **updates)
                else:
                    print("  Нет данных для обновления.")

            # ── 8. Удаление ──
            elif choice == "8":
                sid = get_input("ID студента для удаления", int)
                confirm = input(f"  Подтвердите удаление STU-{sid}? (y/n): ").strip().lower()
                if confirm == "y":
                    sms.delete_student(sid)

            # ── 9. Статистика ──
            elif choice == "9":
                sms.print_statistics()

            # ── 0. Выход ──
            elif choice == "0":
                print("\n  Выход... 👋\n")
                break

            else:
                print("  ⚠️  Неизвестная команда. Попробуйте снова.")

        except (ValueError, LookupError, KeyError) as e:
            print(f"\n  ⛔  Ошибка: {e}\n")

        input("\n  [Нажмите Enter, чтобы продолжить...]")


if __name__ == "__main__":
    run()