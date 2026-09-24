
import sqlite3

# Connecting to database
conn = sqlite3.connect("placement.db")
cursor = conn.cursor()


# Creating tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    branch TEXT,
    cgpa REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    role TEXT,
    package REAL,
    min_cgpa REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    company_id INTEGER,
    status TEXT
)
""")

conn.commit()


# Function to register a student
def register_student():

    print("\n--- Student Registration ---")

    name = input("Enter student name: ")
    email = input("Enter email: ")
    branch = input("Enter branch: ")
    cgpa = float(input("Enter CGPA: "))

    cursor.execute("""
    INSERT INTO students (name, email, branch, cgpa)
    VALUES (?, ?, ?, ?)
    """, (name, email, branch, cgpa))

    conn.commit()
    student_id = cursor.lastrowid

    print("Student registered successfully!")
    print("Your Student ID is :", student_id)


# Function to add a company
def add_company():

    print("\n--- Add Company ---")

    name = input("Enter company name: ")
    role = input("Enter job role: ")
    package = float(input("Enter package (in LPA): "))
    min_cgpa = float(input("Enter minimum CGPA required: "))

    cursor.execute("""
    INSERT INTO companies
    (name, role, package, min_cgpa)
    VALUES (?, ?, ?, ?)
    """, (name, role, package, min_cgpa))

    conn.commit()

    print("Company added successfully!")


# Function to display companies
def view_companies():

    print("\n--- Available Companies ---")

    cursor.execute("SELECT * FROM companies")

    companies = cursor.fetchall()

    if len(companies) == 0:
        print("No companies available.")

    else:
        for company in companies:
            print("\nCompany ID:", company[0])
            print("Company Name:", company[1])
            print("Job Role:", company[2])
            print("Package:", company[3], "LPA")
            print("Minimum CGPA:", company[4])


# Function to check eligibility
def check_eligibility():

    print("\n--- Check Eligibility ---")

    student_id = int(input("Enter your student ID: "))

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student is None:
        print("Student not found.")
        return

    cgpa = student[4]

    print("Your CGPA:", cgpa)
    print("\nCompanies you are eligible for:")

    cursor.execute(
        "SELECT * FROM companies WHERE min_cgpa <= ?",
        (cgpa,)
    )

    companies = cursor.fetchall()

    if len(companies) == 0:
        print("No eligible companies found.")

    else:
        for company in companies:
            print(
                company[0],
                "-",
                company[1],
                "-",
                company[2],
                "-",
                company[3],
                "LPA"
            )


# Function to apply for a job
def apply_for_job():

    print("\n--- Apply for Job ---")

    student_id = int(input("Enter student ID: "))
    company_id = int(input("Enter company ID: "))

    # Check student
    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student is None:
        print("Student not found.")
        return

    # Check company
    cursor.execute(
        "SELECT * FROM companies WHERE id = ?",
        (company_id,)
    )

    company = cursor.fetchone()

    if company is None:
        print("Company not found.")
        return

    # Check CGPA eligibility
    if student[4] < company[4]:
        print("You are not eligible for this company.")
        return

    # Check whether already applied
    cursor.execute("""
    SELECT * FROM applications
    WHERE student_id = ? AND company_id = ?
    """, (student_id, company_id))

    application = cursor.fetchone()

    if application is not None:
        print("You have already applied for this company.")
        return

    # Insert application
    cursor.execute("""
    INSERT INTO applications
    (student_id, company_id, status)
    VALUES (?, ?, ?)
    """, (student_id, company_id, "Applied"))

    conn.commit()

    print("Application submitted successfully!")


# Function to view application status
def view_application_status():

    print("\n--- Application Status ---")

    student_id = int(input("Enter student ID: "))

    cursor.execute("""
    SELECT applications.id,
           companies.name,
           companies.role,
           applications.status
    FROM applications
    JOIN companies
    ON applications.company_id = companies.id
    WHERE applications.student_id = ?
    """, (student_id,))

    applications = cursor.fetchall()

    if len(applications) == 0:
        print("No applications found.")

    else:
        for application in applications:
            print("\nApplication ID:", application[0])
            print("Company:", application[1])
            print("Job Role:", application[2])
            print("Status:", application[3])


# Main menu
while True:

    print("\n===================================")
    print("       STUDENT PLACEMENT PORTAL")
    print("===================================")

    print("1. Register Student")
    print("2. Add Company")
    print("3. View Companies")
    print("4. Check Eligibility")
    print("5. Apply for Job")
    print("6. View Application Status")
    print("7. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        register_student()

    elif choice == "2":
        add_company()

    elif choice == "3":
        view_companies()

    elif choice == "4":
        check_eligibility()

    elif choice == "5":
        apply_for_job()

    elif choice == "6":
        view_application_status()

    elif choice == "7":
        print("\nThank you for using Student Placement Portal!")
        break

    else:
        print("Invalid choice. Please try again.")


# Closing database
conn.close()

