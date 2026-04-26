import psycopg2
from config import DB_PARAMS

def get_connection():
    return psycopg2.connect(**DB_PARAMS)

def get_or_create_player(username):
    conn = get_connection()
    cur = conn.cursor()
    
    # Ойыншы базада бар ма, тексереміз
    cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING;", (username,))
    conn.commit()
    
    # Ойыншының ID-ін аламыз
    cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
    player_id = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    return player_id

def save_game_result(player_id, score, level):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s);",
        (player_id, score, level)
    )
    conn.commit()
    cur.close()
    conn.close()