import sqlite3
import os
import sys

# Path to the actual SQLite database created by create_db.py / create_proper_db.py
db_path = os.path.join('database', 'department.db')

if not os.path.exists(db_path):
	print(f"Database file not found at '{db_path}'.")
	print("Create it by running 'create_proper_db.py' or 'create_db.py'.")
	sys.exit(1)

try:
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
	rows = cursor.fetchall()
	tables = [r[0] for r in rows]

	if not tables:
		print(f"No tables found in database '{db_path}'.")
	else:
		print(f"Tables in database '{db_path}':")
		for t in tables:
			print(f" - {t}")

except sqlite3.Error as e:
	print(f"SQLite error: {e}")
finally:
	if 'conn' in locals():
		conn.close()
