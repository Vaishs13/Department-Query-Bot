#!/usr/bin/env python3

"""
create_department_db.py

This script creates an SQLite3 database for the department syllabus
and populates it with comprehensive data for subjects, faculty,
and infrastructure.
"""

import sqlite3
import os
import argparse

# Create database in the 'database' directory
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'database', 'department.db'))
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# CLI: allow --force to overwrite an existing DB; otherwise keep existing DB
parser = argparse.ArgumentParser(description='Create and populate department SQLite database.')
parser.add_argument('--force', action='store_true', help='Remove existing database and recreate (destructive).')
args = parser.parse_args()

if os.path.exists(db_path):
    if args.force:
        os.remove(db_path)
        print(f"Removed old database '{db_path}' (force enabled).")
    else:
        print(f"Database '{db_path}' already exists. Use --force to recreate it.")
        print("Exiting without changes.")
        raise SystemExit(0)

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign key support (crucial for data integrity)
cursor.execute("PRAGMA foreign_keys = ON;")
print(f"Database '{db_path}' created. Foreign key support enabled.")

try:
    # --- 1. Schema Creation ---
    print("\n--- Creating Tables ---")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS semesters (
        semester_id INTEGER PRIMARY KEY AUTOINCREMENT,
        semester_number INTEGER NOT NULL,
        semester_name TEXT,
        academic_year TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    print("Table 'semesters' created.")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        semester_id INTEGER,
        subject_code TEXT NOT NULL UNIQUE,
        subject_title TEXT NOT NULL,
        credits INTEGER NOT NULL,
        lecture_hours INTEGER,
        tutorial_hours INTEGER,
        practical_hours INTEGER,
        total_contact_hours INTEGER,
        cie_marks INTEGER,
        see_marks INTEGER,
        ltp_structure TEXT,
        FOREIGN KEY (semester_id) REFERENCES semesters(semester_id)
    )
    ''')
    print("Table 'subjects' created.")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS course_objectives (
        objective_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        objective_number INTEGER,
        objective_description TEXT NOT NULL,
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
    )
    ''')
    print("Table 'course_objectives' created.")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS course_outcomes (
        outcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        outcome_number INTEGER,
        outcome_description TEXT NOT NULL,
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
    )
    ''')
    print("Table 'course_outcomes' created.")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS course_units (
        unit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        unit_number INTEGER,
        unit_title TEXT NOT NULL,
        teaching_hours INTEGER,
        tutorial_hours INTEGER,
        unit_content TEXT,
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
    )
    ''')
    print("Table 'course_units' created.")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reference_books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        book_type TEXT CHECK(book_type IN ('text', 'reference')),
        book_number INTEGER,
        book_details TEXT NOT NULL,
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
    )
    ''')
    print("Table 'reference_books' created.")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS co_po_mapping (
        mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        course_outcome TEXT,
        po1 INTEGER, po2 INTEGER, po3 INTEGER, po4 INTEGER, po5 INTEGER, po6 INTEGER, po7 INTEGER, po8 INTEGER, po9 INTEGER, po10 INTEGER, po11 INTEGER, po12 INTEGER,
        pso1 INTEGER, pso2 INTEGER, pso3 INTEGER,
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
    )
    ''')
    print("Table 'co_po_mapping' created.")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Faculty (
        faculty_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        designation TEXT NOT NULL,
        qualification TEXT,
        specialization TEXT,
        email TEXT,
        phone_no TEXT
    )
    ''')
    print("Table 'Faculty' created.")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SupportingStaff (
        staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        designation TEXT NOT NULL,
        phone_no TEXT
    )
    ''')
    print("Table 'SupportingStaff' created.")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS LabInfrastructure (
        lab_id INTEGER PRIMARY KEY AUTOINCREMENT,
        lab_no TEXT NOT NULL,
        lab_name TEXT NOT NULL,
        incharge TEXT NOT NULL
    )
    ''')
    print("Table 'LabInfrastructure' created.")

    print("\nAll tables created successfully.")

    # --- 2. Data Insertion (Using the FULL dataset) ---
    print("\n--- Inserting Data ---")

    # Insert Semester and get its ID
    cursor.execute("""
    INSERT INTO semesters (semester_number, semester_name, academic_year) 
    VALUES (5, 'Fifth Semester', '2024-2025');
    """)
    semester_5_id = cursor.lastrowid
    print(f"Inserted semester 'Fifth Semester' (ID: {semester_5_id})")

    # Insert Subjects and get their IDs
    cursor.execute("""
    INSERT INTO subjects (semester_id, subject_code, subject_title, credits, lecture_hours, tutorial_hours, practical_hours, total_contact_hours, cie_marks, see_marks, ltp_structure) 
    VALUES (?, '22UIS503C', 'Web Programming', 3, 2, 0, 2, 4, 50, 50, '2L-0T-2P');
    """, (semester_5_id,))
    web_programming_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO subjects (semester_id, subject_code, subject_title, credits, lecture_hours, tutorial_hours, practical_hours, total_contact_hours, cie_marks, see_marks, ltp_structure) 
    VALUES (?, '22UIS003E', 'Introduction to Artificial Intelligence', 3, 3, 0, 0, 3, 50, 50, '3L-0T-0P');
    """, (semester_5_id,))
    ai_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO subjects (semester_id, subject_code, subject_title, credits, lecture_hours, tutorial_hours, practical_hours, total_contact_hours, cie_marks, see_marks, ltp_structure) 
    VALUES (?, '22UIS501C', 'Software Engineering', 3, 3, 0, 0, 40, 50, 50, '3L-0T-0P');
    """, (semester_5_id,))
    se_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO subjects (semester_id, subject_code, subject_title, credits, lecture_hours, tutorial_hours, practical_hours, total_contact_hours, cie_marks, see_marks, ltp_structure) 
    VALUES (?, '22UIS502C', 'Computer Networks (Integrated)', 3, 2, 0, 2, 26, 50, 50, '2L-0T-2P');
    """, (semester_5_id,))
    cn_id = cursor.lastrowid
    print(f"Inserted subjects (Web ID: {web_programming_id}, AI ID: {ai_id}, SE ID: {se_id}, CN ID: {cn_id})")

    # --- Web Programming Data ---
    web_objectives = [
        (web_programming_id, 1, 'Understand the principles of World Wide Web and also to create an effective web page.'),
        (web_programming_id, 2, 'Use CSS to implement a variety of presentation effects in XHTML documents.'),
        (web_programming_id, 3, 'Develop basic programming skills using JavaScript'),
        (web_programming_id, 4, 'Implement interactive and dynamic web pages using XHTML, CSS and JavaScript'),
        (web_programming_id, 5, 'Understand how server-side programming works on the web using PHP technology and design responsive web pages using PHP')
    ]
    cursor.executemany("INSERT INTO course_objectives (subject_id, objective_number, objective_description) VALUES (?, ?, ?);", web_objectives)

    web_outcomes = [
        (web_programming_id, 1, 'Develop web pages using technologies like XHTML and CSS.'),
        (web_programming_id, 2, 'Develop JavaScript scripts for event handling.'),
        (web_programming_id, 3, 'Build dynamic documents using JavaScript and XHTML.'),
        (web_programming_id, 4, 'Implement web pages using PHP and MySQL.')
    ]
    cursor.executemany("INSERT INTO course_outcomes (subject_id, outcome_number, outcome_description) VALUES (?, ?, ?);", web_outcomes)

    web_units = [
        (web_programming_id, 1, 'FUNDAMENTALS OF WEB, XHTML', 7, 0, 'Internet, HTTP request and HTTP response phase, MIME, The Web Programmers Toolbox. XHTML: Basic syntax; Standard XHTML document structure; Basic text markup. XHTML : Hypertext Links; Lists; Tables; Forms; Syntactic differences between HTML and XHTML. CSS: Introduction; Levels of style sheets; Style specification formats; Selector forms; Property value forms; CSS: Font properties; List properties; Color; Alignment of text; Background images; The <span> and <div> tags'),
        (web_programming_id, 2, 'Basics of JavaScript', 7, 0, 'General syntactic characteristics; Primitives, Screen output and keyboard input; Control statements; Arrays; Functions. JavaScript & XHTML Documents: The Document Object Model, Element Access in JavaScript, Events & Event Handling, Basic Concepts of Event handling, Events, Attributes & Tags, Handling Events from Body Elements, Handling Events from Button Elements, Handling Events from Textbox & password Elements, The Focus Event'),
        (web_programming_id, 3, 'Dynamic Documents with JavaScript', 6, 0, 'Introduction, Positioning Elements, Absolute Positioning, Relative Positioning, Static Positioning, Moving Elements, Element Visibility, Changing Colors & Fonts, Changing Colors, Changing Fonts, Dynamic Contents, Stacking Elements, Locating the Mouse Cursor, Reacting to the Mouse Click, Slow Movement of Elements, Dragging & Dropping Elements.'),
        (web_programming_id, 4, 'Introduction to PHP', 6, 0, 'Origins and Uses of PHP, Overview of PHP, General Syntactic Characteristics, Primitives, Operations and Expressions, Output, Control statements, Arrays, Functions, Form Handling, Cookies, Database access with PHP and MySQL')
    ]
    cursor.executemany("INSERT INTO course_units (subject_id, unit_number, unit_title, teaching_hours, tutorial_hours, unit_content) VALUES (?, ?, ?, ?, ?, ?);", web_units)

    web_books = [
        (web_programming_id, 'text', 1, 'Programming the World Wide Web - Robert W. Sebesta, 4th Edition, Pearson Education, 2008.'),
        (web_programming_id, 'reference', 1, 'Internet & World Wide Web How to program - M. Deitel, P.J.Deitel, A. B. Goldberg, 3rd Edition, Pearson Education / PHI, 2004.'),
        (web_programming_id, 'reference', 2, 'Web Programming Building Internet Applications - Chris Bates,3rd Edition, Wiley India, 2006.'),
        (web_programming_id, 'reference', 3, 'The Web Warrior Guide to Web Programming - Xue Bai et al,Thomson, 2003.'),
        (web_programming_id, 'reference', 4, 'M.Srinivasan: Web Technology Theory and Practice, Pearson Education, 2012.'),
        (web_programming_id, 'reference', 5, 'Jeffrey.C.Jackson: Web Technologies-A Computer Science Perspective, Pearson Education, Eleventh Impression, 2012')
    ]
    cursor.executemany("INSERT INTO reference_books (subject_id, book_type, book_number, book_details) VALUES (?, ?, ?, ?);", web_books)

    web_mapping = [
        (web_programming_id, 'CO1', 3, 2, 3, None, 1, None, None, None, None, None, None, 1, 1, 2, 1),
        (web_programming_id, 'CO2', 3, 2, 3, None, 1, None, None, None, None, None, None, 1, 1, 2, 1),
        (web_programming_id, 'CO3', 3, 2, 3, None, 1, None, None, None, None, None, None, 1, 1, 2, 1),
        (web_programming_id, 'CO4', 3, 2, 3, None, 1, None, None, None, None, None, None, 1, 1, 2, 1)
    ]
    cursor.executemany("""
    INSERT INTO co_po_mapping (subject_id, course_outcome, po1, po2, po3, po4, po5, po6, po7, po8, po9, po10, po11, po12, pso1, pso2, pso3)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, web_mapping)
    print("Inserted all data for 'Web Programming'.")

    # --- Artificial Intelligence Data ---
    ai_units = [
        (ai_id, 1, 'Introduction to AI', 10, 0, 'What is AI? Domains and use cases of AI, Defining the problem as a state space search, solving problems by searching, Uninformed search strategies: BFS, DFS, informed (Heuristic) search strategies: Hill climbing, Simulated annealing, A* algorithm, AO* algorithm, Constraint satisfaction.'),
        (ai_id, 2, 'Machine Learning', 10, 0, 'What is machine learning? Types of MLs, Supervised ML, Common tasks in Supervised ML, Classification & types, Regression & types, Unsupervised ML, Common tasks in Unsupervised ML, Clustering and types, Semi supervised ML, Supervised ML algorithms, Unsupervised ML algorithms, decision trees, K means algorithm.'),
        (ai_id, 3, 'Deep Learning', 10, 0, 'What is deep learning? Perceptions, multi-layer perceptions, backpropagation, Artificial Neural Networks, Convolution Neural Networks, Recurrent Neural Networks, Gradient descent.'),
        (ai_id, 4, 'Generative AI', 10, 0, 'What is Generative AI? Attention, Contextual embeddings, Self-attention, Transformers, Multi-head self-attention, Positional encodings.')
    ]
    cursor.executemany("INSERT INTO course_units (subject_id, unit_number, unit_title, teaching_hours, tutorial_hours, unit_content) VALUES (?, ?, ?, ?, ?, ?);", ai_units)

    ai_outcomes = [
        (ai_id, 1, 'Solve problems by search applying various search strategies.'),
        (ai_id, 2, 'Demonstrate machine learning concepts.'),
        (ai_id, 3, 'Describe building blocks of deep learning.'),
        (ai_id, 4, 'Explain basic concepts of generative AI.')
    ]
    cursor.executemany("INSERT INTO course_outcomes (subject_id, outcome_number, outcome_description) VALUES (?, ?, ?);", ai_outcomes)

    ai_books = [
        (ai_id, 'reference', 1, 'Joseph Babcock, Raghav Bali, 2021, "Generative AI With Python and Tensorflow2", Packt.'),
        (ai_id, 'reference', 2, 'Aurelien Geron, 2017, "Hands-On Machine Learning with Scikit-Learn & TensorFlow", O''Reilly.'),
        (ai_id, 'reference', 3, 'Elaine Rich, Kevin Knight, Shivashankar B. Nair, "Artificial Intelligence", TMH.'),
        (ai_id, 'reference', 4, 'Chip Huyen, 2024, "AI Engineering", O''Reilly.')
    ]
    cursor.executemany("INSERT INTO reference_books (subject_id, book_type, book_number, book_details) VALUES (?, ?, ?, ?);", ai_books)

    ai_mapping = [
        (ai_id, 'CO1', 1, 1, 2, None, None, None, None, None, None, None, None, None, 1, None, None),
        (ai_id, 'CO2', 1, 1, 2, None, 1, None, None, None, None, None, None, None, 1, 1, None),
        (ai_id, 'CO3', 1, 1, 2, None, None, None, None, None, None, None, None, None, 1, 1, None),
        (ai_id, 'CO4', 1, 1, 2, None, 1, None, None, None, None, None, 1, None, 1, 1, 1)
    ]
    cursor.executemany("""
    INSERT INTO co_po_mapping (subject_id, course_outcome, po1, po2, po3, po4, po5, po6, po7, po8, po9, po10, po11, po12, pso1, pso2, pso3)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, ai_mapping)
    print("Inserted all data for 'Artificial Intelligence'.")
    
    # --- Software Engineering Data ---
    se_units = [
        (se_id, 1, 'INTRODUCTION AND SOFTWARE LIFE CYCLE MODELS', 10, 0, 'INTRODUCTION: Evolution- from an art form to an engineering discipline, software development projects, exploratory style of software development, emergence of software engineering, notable changes in software development practices, computer systems engineering. SOFTWARE LIFE CYCLE MODELS: A few basic concepts, waterfall model and its extensions, rapid application development, agile development models, spiral model, a comparison of different life cycle models.'),
        (se_id, 2, 'REQUIREMENTS ANALYSIS AND SOFTWARE DESIGN', 10, 0, 'REQUIREMENTS ANALYSIS AND SPECIFICATION: Requirements gathering and analysis, software requirements specification (SRS). SOFTWARE DESIGN: Overview of the design process, how to characterize a good software design, cohesion and coupling, layered arrangement of Modules'),
        (se_id, 3, 'FUNCTION-ORIENTED SOFTWARE DESIGN AND TESTING', 10, 0, 'FUNCTION-ORIENTED SOFTWARE DESIGN: Overview of SA/SD methodology, structured analysis, developing the DFD model of the system, structured design, detailed design, design review. CODING AND TESTING: Introduction to program testing, Coding, code review, software documentation, testing, unit testing, black-box testing, White-box testing, debugging, program analysis tools, integration testing.'),
        (se_id, 4, 'SOFTWARE RELIABILITY AND PROJECT MANAGEMENT', 10, 0, 'SOFTWARE RELIABILITY AND QUALITY MANAGEMENT: Software reliability, statistical testing, software quality, software quality management system, ISO 9000, SEI capability maturity model. SOFTWARE PROJECT MANAGEMENT: software project management complexities, responsibilities of a software project manager, project planning and metrics for project size estimation, project estimation techniques, COCOMO - a heuristic estimation technique.')
    ]
    cursor.executemany("INSERT INTO course_units (subject_id, unit_number, unit_title, teaching_hours, tutorial_hours, unit_content) VALUES (?, ?, ?, ?, ?, ?);", se_units)

    se_outcomes = [
        (se_id, 1, 'Understand fundamentals of software engineering and different life cycle models.'),
        (se_id, 2, 'Apply software engineering techniques in the requirements specification, design and development stages of software projects.'),
        (se_id, 3, 'Apply testing and quality management techniques for development of quality software.'),
        (se_id, 4, 'Exhibit a good knowledge of software project management techniques.')
    ]
    cursor.executemany("INSERT INTO course_outcomes (subject_id, outcome_number, outcome_description) VALUES (?, ?, ?);", se_outcomes)

    se_books = [
        (se_id, 'reference', 1, 'Rajib Mall, Fundamentals of software engineering, 4th edition, pHI.'),
        (se_id, 'reference', 2, 'Ian Somerville, Software Engineering, 7th edition, Pearson Education.'),
        (se_id, 'reference', 3, 'Pressman R.S, "Software Engineering- A Practitioners Approach", MGH New Delhi.')
    ]
    cursor.executemany("INSERT INTO reference_books (subject_id, book_type, book_number, book_details) VALUES (?, ?, ?, ?);", se_books)

    se_mapping = [
        (se_id, 'CO1', 1, 1, 1, None, None, None, 1, None, None, None, 1, 2, 1, 3, 1),
        (se_id, 'CO2', 1, 2, 3, None, None, None, 1, None, None, None, 1, 2, 1, 3, 1),
        (se_id, 'CO3', 1, 1, 3, None, None, None, 1, None, None, None, 1, 2, 1, 3, 1),
        (se_id, 'CO4', 1, 1, 3, None, None, None, 1, None, None, None, 3, 2, 1, 3, 1)
    ]
    cursor.executemany("""
    INSERT INTO co_po_mapping (subject_id, course_outcome, po1, po2, po3, po4, po5, po6, po7, po8, po9, po10, po11, po12, pso1, pso2, pso3)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, se_mapping)
    print("Inserted all data for 'Software Engineering'.")

    # --- Computer Networks Data ---
    cn_units = [
        (cn_id, 1, 'INTRODUCTION AND NETWORK MODELS', 7, 0, 'Introduction: Data Communications: Components, Data representations, Data flow, Networks: Network Criteria and Physical structures, Categories of Networks [LAN, WAN, MAN]. Network Models: The OSI Model: layered architecture, Layers in the OSI model: [Brief description of all seven layers], TCP / IP Protocol Suite: physical, data link, network, transport and application layer.'),
        (cn_id, 2, 'PHYSICAL LAYER AND DATA LINK LAYER', 6, 0, 'Physical Layer: Transmission Media: Guided Media: Twisted pair cable, Coaxial cable, Fiber Optic cable, Unguided Media: Radio waves, Microwaves, Infrared. Data Link Layer: Error detection and correction: Cyclic codes: CRC, Checksum.'),
        (cn_id, 3, 'NETWORK LAYER', 7, 0, 'Network Layer: Logical Addressing: IPv4 Addresses: Address Space, Notation, Classfull Addressing, Classless Addressing, IPv6 Addresses: Structure, Address Space. Network Layer: Delivery, Forwarding & Routing: Unicast routing protocols: Distance vector routing, Link state routing.'),
        (cn_id, 4, 'TRANSPORT LAYER AND CONGESTION CONTROL', 6, 0, 'Transport Layer: Process to Process Delivery: UDP: UDP services, UDP features. TCP: TCP services, TCP features, SCTP: SCTP services, SCTP features. Congestion Control and Quality of Service: Congestion control: Open loop congestion control and closed loop congestion control.')
    ]
    cursor.executemany("INSERT INTO course_units (subject_id, unit_number, unit_title, teaching_hours, tutorial_hours, unit_content) VALUES (?, ?, ?, ?, ?, ?);", cn_units)

    cn_outcomes = [
        (cn_id, 1, 'Comprehend fundamentals of data communication system.'),
        (cn_id, 2, 'Identify functions of OSI and TCP/IP models.'),
        (cn_id, 3, 'Apply different error detection and correction technique to solve communication problem.'),
        (cn_id, 4, 'Apply class full and classless addressing with their respective address space in various networks.'),
        (cn_id, 5, 'Use various algorithms to solve routing problems.'),
        (cn_id, 6, 'Analyse various transport and application layer protocols.')
    ]
    cursor.executemany("INSERT INTO course_outcomes (subject_id, outcome_number, outcome_description) VALUES (?, ?, ?);", cn_outcomes)

    cn_books = [
        (cn_id, 'reference', 1, 'Data Communications and Networking Behrouz A. Forouzan, 4th Edition, Tata McGrawHill, 2006. [Unit-I: Chapters 1, 2 ,7 Unit-II: Chapters 8, 10, 11 Unit-III: Chapters 19,20, 21,22 Unit-IV: Chapters 23, 24, 25 and 26]'),
        (cn_id, 'reference', 2, 'Communication Networks --Fundamental Concepts and Key Architectures Alberto LeonGarcia and IndraWidjaja, 2 nd Edition, Tata McGrawHill,2004.')
    ]
    cursor.executemany("INSERT INTO reference_books (subject_id, book_type, book_number, book_details) VALUES (?, ?, ?, ?);", cn_books)
    print("Inserted all data for 'Computer Networks'.")

    # --- Faculty Data (Full List) ---
    faculty_data = [
        ('Dr.S.P.Bangarashetti', 'Professor and Head Of Department', 'Ph.D,M.Tech,BE', 'Image Processing', 'spbis@becbgk.edu', '+91 9448215955'),
        ('Dr.S.R.Patil', 'Professor', 'Ph.D,M.Tech,BE', 'Image Processing', 'srpis@becbgk.edu', '+91 9449534202'),
        ('Prof.P.V.Kulakarni', 'Associate Professor', 'M.Tech,BE', 'Database Systems', 'pvkis@becbgk.edu', '+91 9448939735'),
        ('Smt.P.Puranik', 'Associate Professor', 'M.Tech,BE', 'Web Technology', 'pspis@becbg.edu', '+91 9449724440'),
        ('Dr.L.B.Bhajantri', 'Associate Professor', 'Ph.D,M.Tech,BE', 'Wireless networks and communications', 'lbbis@beckbgk.edu', '+91 8904614106'),
        ('Smt.Roopa Math', 'Assistant Professor', 'M.Tech,BE', 'Quality management', 'rbmis@beckbgk.edu', '+91 9480222544'),
        ('Smt.V.S.Patil', 'Assistant Professor', 'M.Tech,BE', 'Image processing', 'vspis@beckbgk.edu', '+91 9449224311'),
        ('Sri.S.N.Kugali', 'Assistant Professor', 'M.Tech,BE', 'Virtual Adhoc networks', 'snkis@beckbgk.edu', '+91 9686877836'),
        ('Miss.G.M.Patil', 'Assistant Professor', 'M.Tech,BE', 'Networking', 'gmpis@beckbgk.edu', '+91 9972418388'),
        ('Sri.P.K.Deshpande', 'Assistant Professor', 'M.Tech,BE', 'Algorithms and database', 'pkdis@beckbgk.edu', '+91 9945112976'),
        ('Sri.G.B.Shettar', 'Assistant Professor', 'M.Tech,BE', 'Software testing and Computer Networks', 'gbsis@beckbgk.edu', '+91 9620863183'),
        ('Smt.D.I.Kalappanavar', 'Assistant Professor', 'M.Tech,BE', 'Networking', 'dikis@beckbgk.edu', '+91 9481982363'),
        ('Miss.C.R.Shivanagi', 'Assistant Professor', 'M.Tech,BE', 'Image processing', 'crsis@beckbgk.edu', '+91 9916688415'),
        ('Sri.M.R.Patil', 'Assistant Professor', 'M.Tech,BE', 'Web Technology', 'mrpis@beckbgk.edu', '+91 9449481282'),
        ('Sri.S.S.Hiremath', 'Assistant Professor', 'M.Tech,BE', 'Wireless Sensor Networks,Iot', 'sshis@beckbgk.edu', '+91 8867348752'),
        ('Smt.Sheetal.P', 'Assistant Professor', 'M.Tech,BE', 'Computer Networks', 'spis@beckbgk.edu', '+91 8123999572'),
        ('Ms.P.R.Muttannavar', 'Assistant Professor', 'M.Tech,BE', 'Web Technology', 'prmis@beckbgk.edu', '+91 9380649626'),
        ('Smt.Seema.G', 'Assistant Professor', 'M.Tech,BE', 'Computer Science', 'seema.sb@beckbgk.edu', '+91 9945799942')
    ]
    cursor.executemany("""
    INSERT INTO Faculty (name, designation, qualification, specialization, email, phone_no) 
    VALUES (?, ?, ?, ?, ?, ?);
    """, faculty_data)
    print("Inserted Faculty data.")

    # --- Supporting Staff Data (Full List) ---
    staff_data = [
        ('Shri.Kupendrakumar.H.B', 'Foreman', None),
        ('Shri.V.S.Nashi', 'Asst.Instructor', None),
        ('Shri.D.S.Gadad', 'Asst.Instructor', None),
        ('Shri.A.D.Lokare', 'Asst.Instructor', None),
        ('Shri.M.V.Gennur', 'Asst.Instructor', None),
        ('Shri.S.B.Khot', 'Instructor', None),
        ('Shri.S.F.Patil', 'Mechanic', None),
        ('Shri.K.C.Golappanavar', 'Peon', None)
    ]
    cursor.executemany("INSERT INTO SupportingStaff (name, designation, phone_no) VALUES (?, ?, ?);", staff_data)
    print("Inserted SupportingStaff data.")

    # --- Lab Infrastructure Data (Full List) ---
    lab_data = [
        ('ISE LAB NO-01', 'Tim Berners-Lee Lab', 'Shri.M.V.Gennur'),
        ('ISE LAB NO-02', 'Abraham SilberschGatz Lab', 'MR.Patil'),
        ('ISE LAB NO-03', 'Aho and Ullman Lab', 'Shri.V.S.Nashi'),
        ('ISE LAB NO-04', 'A.P.J.Abdul Kalam Lab', 'Shri.S.B.Khot'),
        ('ISE LAB NO-05', 'Quine-McCluskey Lab', 'Shri.V.S.Nashi')
    ]
    cursor.executemany("INSERT INTO LabInfrastructure (lab_no, lab_name, incharge) VALUES (?, ?, ?);", lab_data)
    print("Inserted LabInfrastructure data.")

    # Commit all changes
    conn.commit()
    print("\nDatabase created and populated successfully.")

except sqlite3.Error as e:
    print(f"\nAn error occurred: {e}")
    print("Rolling back changes...")
    conn.rollback()

finally:
    # Close the connection
    conn.close()
    print("Database connection closed.")