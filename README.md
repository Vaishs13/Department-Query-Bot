Department Query Chatbot
=========================

This project provides a small Flask-based chatbot for answering department-related queries (subjects, syllabus, faculty, labs, etc.) using an SQLite database.

Quick start
-----------

1. Create the database (safe by default):

	 - To create the DB only if it doesn't exist:
		 ```powershell
		 python .\create_proper_db.py
		 ```

	 - To force recreation (will delete existing DB):
		 ```powershell
		 python .\create_proper_db.py --force
		 ```

2. Run the Flask app:

	 ```powershell
	 python .\app.py
	 ```

3. Open the web UI at http://localhost:5000 (default).

API
---

POST /get

- Accepts JSON { "message": "your question" }
- Returns JSON { "reply": "bot response" } or { "error": "..." }

Backend notes and safety improvements
------------------------------------

- DB path: `database/department.db` (the helper will complain if missing).
- `create_proper_db.py` no longer overwrites the DB unless `--force` is used.
- `chatbot/db_helper.py` centralizes DB access and logs errors. Missing DB will be reported instead of causing unhelpful crashes.
- `app.py` validates input and returns clear HTTP error codes for malformed requests.

Sample prompts you can ask the chatbot
-------------------------------------

Try these in the web UI or via the API payload:

- "Hi" or "Hello"
- "What can you do?" or "help"
- "Show 5th semester subjects"
- "Show 5th semester syllabus"
- "Web Programming outcomes"
- "AI reference books"
- "Who is the HOD of ISE?"
- "List Assistant Professors"
- "Faculty specialized in Image Processing"
- "Show lab details"
- "List supporting staff"

If you want more polished sample prompts or a JSON-based test harness, tell me which format you prefer and I can add it.
