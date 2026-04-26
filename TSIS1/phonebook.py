import json
from connect import get_connection

# 1. Жаңа контакт қосу
def add_contact(first_name, last_name, email, birthday, phone, phone_type, group_name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Топты алу немесе құру
        cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name=EXCLUDED.name RETURNING id;", (group_name,))
        group_id = cur.fetchone()[0]

        # Контактты қосу
        cur.execute("""
            INSERT INTO contacts (first_name, last_name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """, (first_name, last_name, email, birthday, group_id))
        
        contact_id = cur.fetchone()[0]

        # Телефонды қосу
        cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);", 
                    (contact_id, phone, phone_type))

        conn.commit()
        print("\n✅ Контакт сәтті қосылды!")
    except Exception as e:
        conn.rollback()
        print(f"❌ Қате: {e}")
    finally:
        cur.close()
        conn.close()

# 2. Жетілдірілген іздеу (SQL Function арқылы)
def search_contacts_logic(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s);", (query,))
    results = cur.fetchall()
    
    if not results:
        print("\n🔍 Ештеңе табылмады.")
    else:
        print("\n--- Табылған контактілер ---")
        for row in results:
            print(f"ID: {row[0]} | Аты: {row[1]} {row[2]} | Email: {row[3]} | Тел: {row[4]} | Топ: {row[5]}")
    
    cur.close()
    conn.close()

# 3. Тізімді көру (Пагинация)
def view_paginated(limit=5):
    offset = 0
    conn = get_connection()
    cur = conn.cursor()

    while True:
        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, g.name 
            FROM contacts c 
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id LIMIT %s OFFSET %s
        """, (limit, offset))
        
        rows = cur.fetchall()
        print("\n--- Контактілер тізімі (Пагинация) ---")
        if not rows:
            print("Тізім бос.")
        for r in rows:
            print(f"ID: {r[0]} | {r[1]} {r[2]} | Топ: {r[3]}")

        nav = input("\n[n] Келесі, [p] Алдыңғы, [q] Шығу: ").lower()
        if nav == 'n' and len(rows) == limit: offset += limit
        elif nav == 'p': offset = max(0, offset - limit)
        elif nav == 'q': break
            
    cur.close()
    conn.close()

# 4. JSON-ға Экспорт
def export_to_json(filename="contacts.json"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.first_name, c.last_name, c.email, c.birthday, g.name, 
               array_agg(p.phone || ' (' || p.type || ')') as phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, g.name;
    """)
    
    rows = cur.fetchall()
    data = []
    for r in rows:
        data.append({
            "first_name": r[0], "last_name": r[1], "email": r[2],
            "birthday": str(r[3]), "group": r[4], "phones": r[5]
        })
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"\n💾 Деректер {filename} файлына сақталды!")
    cur.close()
    conn.close()

# 5. JSON-нан Импорт (Дубликаттарды өңдеумен)
def import_from_json(filename="contacts.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Файл табылмады!")
        return

    conn = get_connection()
    cur = conn.cursor()

    for item in data:
        cur.execute("SELECT id FROM contacts WHERE first_name = %s AND last_name = %s", 
                    (item['first_name'], item['last_name']))
        row = cur.fetchone()

        if row:
            ans = input(f"❓ '{item['first_name']} {item['last_name']}' базада бар. Аттап кету (s) әлде Үстінен жазу (o)? ")
            if ans.lower() == 's': continue
            cur.execute("DELETE FROM phones WHERE contact_id = %s", (row[0],))
            contact_id = row[0]
        else:
            cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name=EXCLUDED.name RETURNING id", (item['group'],))
            group_id = cur.fetchone()[0]
            cur.execute("INSERT INTO contacts (first_name, last_name, email, birthday, group_id) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                        (item['first_name'], item['last_name'], item['email'], item['birthday'], group_id))
            contact_id = cur.fetchone()[0]

        for p_info in item['phones']:
            p_val = p_info.split(' (')[0]
            p_type = p_info.split(' (')[1].replace(')', '')
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", (contact_id, p_val, p_type))

    conn.commit()
    print("\n📥 Импорт аяқталды!")
    cur.close()
    conn.close()

# 6. Контактіні өшіру (CASCADE арқасында телефондары да бірге өшеді)
def delete_contact(name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM contacts WHERE first_name = %s", (name,))
        if cur.rowcount > 0:
            conn.commit()
            print(f"\n✅ {name} және оның барлық деректері өшірілді!")
        else:
            print("\n❌ Мұндай контакт табылмады.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Қате: {e}")
    finally:
        cur.close()
        conn.close()

# Негізгі Мәзір
def main():
    while True:
        print("\n===== PhoneBook Advanced System =====")
        print("1. Жаңа контакт қосу")
        print("2. Іздеу (Аты, Email, Телефон)")
        print("3. Тізімді көру (Пагинация)")
        print("4. JSON-ға экспорттау")
        print("5. JSON-нан импорттау")
        print("6. Контактіні өшіру")
        print("0. Шығу")
        
        choice = input("\nТаңдауыңыз: ")
        
        if choice == "1":
            add_contact(input("Аты: "), input("Тегі: "), input("Email: "), 
                        input("Туған күні (YYYY-MM-DD): "), input("Телефон: "), 
                        input("Түрі (mobile/work/home): "), input("Топ: "))
        elif choice == "2":
            search_contacts_logic(input("Іздеу сөзі: "))
        elif choice == "3":
            view_paginated()
        elif choice == "4":
            export_to_json()
        elif choice == "5":
            import_from_json()
        elif choice == "6":
            delete_contact(input("Өшіретін адамның аты: "))
        elif choice == "0":
            print("Сау болыңыз!")
            break

if __name__ == "__main__":
    main()