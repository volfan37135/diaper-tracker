import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS brands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            num_boxes INTEGER NOT NULL,
            diapers_per_box INTEGER NOT NULL,
            brand TEXT NOT NULL,
            cost REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS box_openings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER NOT NULL,
            box_number INTEGER NOT NULL,
            date_opened TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (purchase_id) REFERENCES purchases(id)
        );
    ''')
    conn.commit()
    conn.close()


# Brand operations

def get_all_brands():
    conn = get_db()
    brands = conn.execute(
        'SELECT * FROM brands ORDER BY brand_name'
    ).fetchall()
    conn.close()
    return brands


def get_brand_names():
    conn = get_db()
    brands = conn.execute(
        'SELECT brand_name FROM brands ORDER BY brand_name'
    ).fetchall()
    conn.close()
    return [b['brand_name'] for b in brands]


def add_brand(brand_name):
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO brands (brand_name) VALUES (?)',
            (brand_name.strip(),)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Brand already exists
    finally:
        conn.close()


def update_brand(brand_id, new_name):
    conn = get_db()
    conn.execute(
        'UPDATE brands SET brand_name = ? WHERE id = ?',
        (new_name.strip(), brand_id)
    )
    conn.commit()
    conn.close()


def delete_brand(brand_id):
    conn = get_db()
    conn.execute('DELETE FROM brands WHERE id = ?', (brand_id,))
    conn.commit()
    conn.close()


# Purchase operations

def add_purchase(date, num_boxes, diapers_per_box, brand, cost):
    conn = get_db()
    cursor = conn.execute(
        '''INSERT INTO purchases (date, num_boxes, diapers_per_box, brand, cost)
           VALUES (?, ?, ?, ?, ?)''',
        (date, num_boxes, diapers_per_box, brand.strip(), cost)
    )
    purchase_id = cursor.lastrowid
    for box_num in range(1, num_boxes + 1):
        conn.execute(
            'INSERT INTO box_openings (purchase_id, box_number) VALUES (?, ?)',
            (purchase_id, box_num)
        )
    conn.commit()
    conn.close()
    # Auto-add brand if new
    add_brand(brand)
    return purchase_id


def get_all_purchases():
    conn = get_db()
    purchases = conn.execute(
        'SELECT * FROM purchases ORDER BY date DESC, created_at DESC'
    ).fetchall()
    conn.close()
    return purchases


def get_purchase(purchase_id):
    conn = get_db()
    purchase = conn.execute(
        'SELECT * FROM purchases WHERE id = ?', (purchase_id,)
    ).fetchone()
    conn.close()
    return purchase


def delete_purchase(purchase_id):
    conn = get_db()
    conn.execute('DELETE FROM box_openings WHERE purchase_id = ?', (purchase_id,))
    conn.execute('DELETE FROM purchases WHERE id = ?', (purchase_id,))
    conn.commit()
    conn.close()


def get_statistics():
    conn = get_db()
    row = conn.execute('''
        SELECT
            COUNT(*) as total_purchases,
            COALESCE(SUM(num_boxes), 0) as total_boxes,
            COALESCE(SUM(num_boxes * diapers_per_box), 0) as total_diapers,
            COALESCE(SUM(cost), 0) as total_cost
        FROM purchases
    ''').fetchone()
    conn.close()

    stats = dict(row)
    if stats['total_diapers'] > 0:
        stats['avg_cost_per_diaper'] = stats['total_cost'] / stats['total_diapers']
    else:
        stats['avg_cost_per_diaper'] = 0
    return stats


# Box opening operations

def get_box_openings(purchase_id):
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM box_openings WHERE purchase_id = ? ORDER BY box_number',
        (purchase_id,)
    ).fetchall()
    conn.close()
    return rows


def get_all_box_openings():
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM box_openings ORDER BY purchase_id, box_number'
    ).fetchall()
    conn.close()
    openings = {}
    for row in rows:
        pid = row['purchase_id']
        if pid not in openings:
            openings[pid] = []
        openings[pid].append(row)
    return openings


def update_box_opening(opening_id, date_opened):
    conn = get_db()
    conn.execute(
        'UPDATE box_openings SET date_opened = ? WHERE id = ?',
        (date_opened, opening_id)
    )
    conn.commit()
    conn.close()


def migrate_box_openings():
    conn = get_db()
    purchases = conn.execute(
        '''SELECT p.id, p.num_boxes FROM purchases p
           WHERE p.id NOT IN (SELECT DISTINCT purchase_id FROM box_openings)'''
    ).fetchall()
    for p in purchases:
        for box_num in range(1, p['num_boxes'] + 1):
            conn.execute(
                'INSERT INTO box_openings (purchase_id, box_number) VALUES (?, ?)',
                (p['id'], box_num)
            )
    conn.commit()
    conn.close()
