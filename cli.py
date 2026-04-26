"""
============================================================
  INTERACTIVE CLI — Student Management System
  Запускается: python cli.py
============================================================
"""

from main import StudentManagementSystem, Student


def hr(char="─", width=50):
    print(char * width)


def print_menu():
    hr("═")
    print("  STUDENT MANAGEMENT SYSTEM")
    hr("═")
    print("  [1]  Register new student")
    print("  [2]  List all students")
    print("  [3]  Search by name")
    print("  [4]  Search by major")
    print("  [5]  Add / update grade")
    print("  [6]  Sort students")
    print("  [7]  Update student info")
    print("  [8]  Delete student")
    print("  [9]  Statistics")
    print("  [0]  Exit")
    hr()


def get_input(prompt: str, cast=str, optional=False):
    while True:
        val = input(f"  {prompt}: ").strip()
        if not val and optional:
            return None
        if not val:
            print("  ⚠️  This field is required.")
            continue
        try:
            return cast(val)
        except (ValueError, TypeError):
            print(f"  ⚠️  Invalid input, expected {cast.__name__}. Try again.")


def run():
    sms = StudentManagementSystem("SDU University")

    # Seed with sample data for convenience
    s1 = sms.register_student("Aidana Bekova",    "aidana@sdu.edu.kz",   "Computer Science", 2)
    s2 = sms.register_student("Daniyar Seitkali", "daniyar@sdu.edu.kz",  "Mathematics",       3)
    s1.add_grade("OOP", 95); s1.add_grade("Algorithms", 88)
    s2.add_grade("Calculus", 76); s2.add_grade("Linear Algebra", 82)
    print("  (2 sample students pre-loaded)\n")

    while True:
        print_menu()
        choice = input("  Choose option: ").strip()

        try:
            # ── 1. Register ──
            if choice == "1":
                print("\n  — Register New Student —")
                name  = get_input("Full name")
                email = get_input("Email")
                major = get_input("Major / field of study")
                year  = get_input("Year (1-6)", int)
                sms.register_student(name, email, major, year)

            # ── 2. List all ──
            elif choice == "2":
                print(f"\n  — All Students ({len(sms)} total) —")
                sms.print_all()

            # ── 3. Search by name ──
            elif choice == "3":
                q = get_input("Enter name (partial ok)")
                results = sms.search_by_name(q)
                print(f"\n  Found {len(results)} result(s):")
                sms.print_all(results)

            # ── 4. Search by major ──
            elif choice == "4":
                q = get_input("Enter major (partial ok)")
                results = sms.search_by_major(q)
                print(f"\n  Found {len(results)} result(s):")
                sms.print_all(results)

            # ── 5. Add grade ──
            elif choice == "5":
                sid     = get_input("Student ID (number only)", int)
                subject = get_input("Subject name")
                grade   = get_input("Grade (0-100)", float)
                sms.add_grade(sid, subject, grade)

            # ── 6. Sort ──
            elif choice == "6":
                print("  Sort by: [1] Name  [2] GPA  [3] Year")
                sub = input("  Choice: ").strip()
                if sub == "1":
                    sms.print_all(sms.sort_by_name())
                elif sub == "2":
                    sms.print_all(sms.sort_by_gpa())
                elif sub == "3":
                    sms.print_all(sms.sort_by_year())

            # ── 7. Update ──
            elif choice == "7":
                sid = get_input("Student ID (number only)", int)
                print("  Fields you can change: name, email, major, year")
                print("  (Press Enter to skip a field)")
                updates = {}
                for field in ("name", "email", "major"):
                    val = get_input(f"New {field}", optional=True)
                    if val:
                        updates[field] = val
                yr = get_input("New year (1-6)", optional=True)
                if yr:
                    updates["year"] = int(yr)
                if updates:
                    sms.update_student(sid, **updates)
                else:
                    print("  Nothing to update.")

            # ── 8. Delete ──
            elif choice == "8":
                sid = get_input("Student ID to delete (number only)", int)
                confirm = input(f"  Confirm delete STU-{sid}? (y/n): ").strip().lower()
                if confirm == "y":
                    sms.delete_student(sid)

            # ── 9. Statistics ──
            elif choice == "9":
                sms.print_statistics()

            # ── 0. Exit ──
            elif choice == "0":
                print("\n  Goodbye! 👋\n")
                break

            else:
                print("  ⚠️  Unknown option. Try again.")

        except (ValueError, LookupError, KeyError) as e:
            print(f"\n  ⛔  Error: {e}\n")

        input("\n  [Press Enter to continue...]")


if __name__ == "__main__":
    run()