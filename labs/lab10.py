import psycopg2
import argparse
import re
import csv

CONFIG: dict = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "postgres"
}

conn = psycopg2.connect(**CONFIG)
cursor = conn.cursor()

def create_phonebook_table():
    query = """
        CREATE TABLE phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(128) NOT NULL,
            surname VARCHAR (128) NOT NULL,
            phone VARCHAR(16) NOT NULL UNIQUE,
            UNIQUE (name, surname)
        )
    """


    try:
        cursor.execute(query)
        conn.commit()
    except (psycopg2.DatabaseError, Exception) as e:
        print(e)


def insert_from_csv(file_path: str):
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                name = row['name'].strip()
                surname = row['surname'].strip()
                phone = row['phone'].strip()

                if not is_phone_valid(phone):
                    print(f"Invalid phone for {name} {surname}: {phone}")
                    continue

                try:
                    cursor.execute("""
                        INSERT INTO phonebook (name, surname, phone)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (name, surname)
                        DO UPDATE SET phone = EXCLUDED.phone;
                    """, (name, surname, phone))
                    print(f"Inserted/Updated: {name} {surname} - {phone}")
                except (psycopg2.DatabaseError, Exception) as e:
                    print(e)
                    conn.rollback()

            conn.commit()
            print("CSV import finished.")

    except FileNotFoundError:
        print("CSV file not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")


def insert_from_console():
    print("Insert multiple entries. Type 'stop' at any time to finish.\n")

    while True:
        name = input("Enter name: ").strip()
        if not name:
            print("Ha-ha, try one more time)\n")
            continue
        if name.lower() == "stop":
            break

        surname = input("Enter surname: ").strip()
        if not surname:
            print("Ha-ha, try one more time)\n")
            continue
        if surname.lower() == "stop":
            break

        phone = input("Enter phone number: ").strip()
        if phone.lower() == "stop":
            break

        if not is_phone_valid(phone):
            print("Invalid phone format. Try again.\n")
            continue

        try:
            # Попробуем вставить запись
            cursor.execute("""
                INSERT INTO phonebook (name, surname, phone)
                VALUES (%s, %s, %s)
                ON CONFLICT (name, surname)
                DO UPDATE SET phone = EXCLUDED.phone;
            """, (name, surname, phone))

            conn.commit()
            print(f"Saved: {name} {surname} - {phone}\n")
        
        except (psycopg2.DatabaseError, Exception) as e:
            print(e)
            conn.rollback()



def update_data():
    print("UPDATE DATA BY:")
    print("1. NAME")
    print("2. PHONE NUMBER\n")
    func = int(input())

    name = input("Input name:\n")
    phone = input("Input phone number:\n")

    if func == 1:
        query = f"UPDATE phonebook SET phone = {phone} WHERE name = {name}"

    elif func == 2:
        query = f"UPDATE phonebook SET name = {name} WHERE phone = {phone}"

    try:
        cursor.execute(f"UPDATE phonebook SET phone = {phone} WHERE name = {name}")
    except (psycopg2.DatabaseError, Exception) as e:
        print(e)


def select_data(name: str = None, surname: str = None, phone: str = None, limit: int = None, offset: int = None):
    query = "SELECT * FROM phonebook"
    conditions = []
    params = []

    if name:
        conditions.append("name ILIKE %s")
        params.append(f"%{name}%")
    if surname:
        conditions.append("surname ILIKE %s")
        params.append(f"%{surname}%")
    if phone:
        conditions.append("phone ILIKE %s")
        params.append(f"%{phone}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    if limit is not None:
        query += " LIMIT %s"
        params.append(limit)

    if offset is not None:
        query += " OFFSET %s"
        params.append(offset)

    try:
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        if not rows:
            print("No matches")
        else:
            for row in rows:
                print(row)
    except Exception as e:
        print("Ошибка при выполнении запроса:", e)


def delete_data(name: str = None, surname: str = None, phone: str = None):
    query = "DELETE FROM phonebook"
    conditions = []
    params = []

    if name:
        conditions.append("name ILIKE %s")
        params.append(f"%{name}%")
    if surname:
        conditions.append("surname ILIKE %s")
        params.append(f"%{surname}%")
    if phone:
        conditions.append("phone ILIKE %s")
        params.append(f"%{phone}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    else:
        confirmation = input("⚠️ ARE YOU SURE YOU WANT TO DELETE **ALL** DATA? [y/N]: ").lower()
        if confirmation != 'y':
            print("Deletion cancelled.")
            return

    try:
        cursor.execute(query, tuple(params))
        conn.commit()
        print("✅ Data deleted.")
    except Exception as e:
        print("❌ Error during deletion:", e)
        conn.rollback()


def update_data(search_name: str = None, search_surname: str = None, search_phone: str = None,
                new_name: str = None, new_surname: str = None, new_phone: str = None):
    conditions = []
    params = []

    if search_name:
        conditions.append("name ILIKE %s")
        params.append(f"%{search_name}%")
    if search_surname:
        conditions.append("surname ILIKE %s")
        params.append(f"%{search_surname}%")
    if search_phone:
        conditions.append("phone ILIKE %s")
        params.append(f"%{search_phone}%")

    if not conditions:
        print("❌ Set at least one search condition (search_name, search_surname или search_phone)")
        return

    where_clause = " AND ".join(conditions)

    updates = []
    update_values = []

    if new_name:
        updates.append("name = %s")
        update_values.append(new_name)
    if new_surname:
        updates.append("surname = %s")
        update_values.append(new_surname)
    if new_phone:
        updates.append("phone = %s")
        update_values.append(new_phone)

    if not updates:
        print("❌ Set at least one new value (new_name, new_surname, new_phone)")
        return

    query = f"UPDATE phonebook SET {', '.join(updates)} WHERE {where_clause}"

    try:
        cursor.execute(query, tuple(update_values + params))
        conn.commit()

        if cursor.rowcount == 0:
            print("❗ Np matches.")
        else:
            print(f"✅ Data updated: {cursor.rowcount}")
    except Exception as e:
        print("❌ Error while update:", e)
        conn.rollback()


def is_phone_valid(number: str) -> bool:
    pattern = r'^(\+7|8)\d{10}$'
    return re.fullmatch(pattern, number) is not None


def run_cli():
    parser = argparse.ArgumentParser(description="PhoneBook Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # CREATE
    create_parser = subparsers.add_parser("create", help="Create table 'phonebook'")

    # INSERT
    insert_parser = subparsers.add_parser("insert", help="Insert data")
    insert_parser.add_argument("--csv")

    # SELECT
    select_parser = subparsers.add_parser("select", help="Select data from table")
    select_parser.add_argument("--name", help="Select by name")
    select_parser.add_argument("--surname", help="Select by surname")
    select_parser.add_argument("--phone", help="Select by phone number")
    select_parser.add_argument("--limit", help="Limit for selection")
    select_parser.add_argument("--offset", help="Offset for selection")


    # DELETE
    delete_parser = subparsers.add_parser("delete", help="Delete data from table")
    delete_parser.add_argument("--name", help="Delete data by name")
    delete_parser.add_argument("--surname", help="Delete data by surname")
    delete_parser.add_argument("--phone", help="Delete data by phone number")

    # UPDATE
    update_parser = subparsers.add_parser("update", help="Update data")
    update_parser.add_argument("--search-name", help="Search by name for updating")
    update_parser.add_argument("--search-surname", help="Search by surname for updating")
    update_parser.add_argument("--search-phone", help="Search by phone number for updating")
    update_parser.add_argument("--new-name", help="New name to set")
    update_parser.add_argument("--new-surname", help="New surname to set")
    update_parser.add_argument("--new-phone", help="New phone to set")



    args = parser.parse_args()

    match args.command:
        case "create":
            create_phonebook_table()

        case "insert":
            if args.csv:
                insert_from_csv(args.csv)
            else:
                insert_from_console()
        case "select":
            select_data(name=args.name, surname=args.surname, phone=args.phone, limit=args.limit, offset=args.offset)
        case "delete":
            delete_data(name=args.name, surname=args.surname, phone=args.phone)
        case "update":
            update_data(search_name=args.search_name, search_surname=args.search_surname, search_phone=args.search_phone,
            new_name=args.new_name, new_surname=args.new_surname, new_phone=args.new_phone)
        case _:
            print("Unknown command")
            


if __name__=="__main__":
    run_cli()