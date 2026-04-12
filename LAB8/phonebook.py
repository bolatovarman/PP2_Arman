import psycopg2
from config import load_config

def run_app():
    config = load_config()
    try:
        # Базаға қосылу
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                
                
                print("Adding contacts...")
                cur.execute("CALL upsert_contact(%s, %s)", ("Alibi", "87071112233"))
                cur.execute("CALL upsert_contact(%s, %s)", ("Aisulu", "87019998877"))

                
                print("\nSearching for 'Ali':")
                cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", ("Ali",))
                results = cur.fetchall()
                for row in results:
                    print(row)

                
                print("\nShowing first page (limit 1):")
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (1, 0))
                print(cur.fetchone())

                
                conn.commit()
                print("\nAll operations completed successfully!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_app()