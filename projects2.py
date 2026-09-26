import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ---------------- DATABASE CONNECTION ----------------
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",   # Add your MySQL password if needed
            database="companydb"
        )
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Employee Management System")
root.geometry("1000x600")
root.config(bg="#f8c8dc")

# ---------------- VARIABLES ----------------
emp_id = tk.StringVar()
name = tk.StringVar()
email = tk.StringVar()
phone = tk.StringVar()
department = tk.StringVar()
salary = tk.StringVar()
search_by = tk.StringVar()
search_txt = tk.StringVar()

# ---------------- FUNCTIONS ----------------

def add_employee():
    if name.get() == "" or email.get() == "":
        messagebox.showerror("Error", "Name and Email Required")
        return

    try:
        sal = float(salary.get()) if salary.get() else 0.0
        con = connect_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO employees (name,email,phone,department,salary) VALUES (%s,%s,%s,%s,%s)",
            (name.get(), email.get(), phone.get(), department.get(), sal)
        )
        con.commit()
        con.close()
        fetch_data()
        clear_fields()
        messagebox.showinfo("Success", "Employee Added Successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def fetch_data():
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT id,name,email,phone,department,salary FROM employees")
    rows = cur.fetchall()
    employee_table.delete(*employee_table.get_children())
    for row in rows:
        employee_table.insert("", tk.END, values=row)
    con.close()


def get_cursor(event):
    row = employee_table.focus()
    if row == "":
        return
    data = employee_table.item(row)["values"]
    if not data:
        return
    emp_id.set(data[0])
    name.set(data[1])
    email.set(data[2])
    phone.set(data[3])
    department.set(data[4])
    salary.set(data[5])


def update_employee():
    if emp_id.get() == "":
        messagebox.showerror("Error", "Select Employee First")
        return

    try:
        sal = float(salary.get()) if salary.get() else 0.0
        con = connect_db()
        cur = con.cursor()
        cur.execute("""
            UPDATE employees SET
            name=%s,
            email=%s,
            phone=%s,
            department=%s,
            salary=%s
            WHERE id=%s
        """, (name.get(), email.get(), phone.get(), department.get(), sal, emp_id.get()))
        con.commit()
        con.close()
        fetch_data()
        clear_fields()
        messagebox.showinfo("Success", "Employee Updated Successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def delete_employee():
    if emp_id.get() == "":
        messagebox.showerror("Error", "Select Employee First")
        return

    con = connect_db()
    cur = con.cursor()
    cur.execute("DELETE FROM employees WHERE id=%s", (emp_id.get(),))
    con.commit()
    con.close()
    fetch_data()
    clear_fields()
    messagebox.showinfo("Success", "Employee Deleted Successfully")


def clear_fields():
    emp_id.set("")
    name.set("")
    email.set("")
    phone.set("")
    department.set("")
    salary.set("")


def search_employee():
    con = connect_db()
    cur = con.cursor()
    query = "SELECT id,name,email,phone,department,salary FROM employees WHERE " + search_by.get() + " LIKE %s"
    cur.execute(query, ('%' + search_txt.get() + '%',))
    rows = cur.fetchall()
    employee_table.delete(*employee_table.get_children())
    for row in rows:
        employee_table.insert("", tk.END, values=row)
    con.close()

# ---------------- UI DESIGN ----------------

title = tk.Label(root, text="EMPLOYEE MANAGEMENT SYSTEM",
                 font=("Arial", 22, "bold"),
                 bg="#f8c8dc")
title.pack(pady=10)

# Form Frame
form_frame = tk.Frame(root, bg="#f2a7c2", bd=5, relief=tk.RIDGE)
form_frame.place(x=30, y=70, width=400, height=470)

lbl_font = ("Arial", 12, "bold")

labels = ["Name", "Email", "Phone", "Department", "Salary"]
vars = [name, email, phone, department, salary]

for i in range(5):
    tk.Label(form_frame, text=labels[i], bg="#f2a7c2",
             font=lbl_font).grid(row=i, column=0, padx=10, pady=15, sticky="w")
    tk.Entry(form_frame, textvariable=vars[i], width=22).grid(row=i, column=1)

# Buttons
tk.Button(form_frame, text="ADD", width=15, bg="#ff69b4",
          command=add_employee).grid(row=5, column=0, pady=15)

tk.Button(form_frame, text="UPDATE", width=15, bg="#ff69b4",
          command=update_employee).grid(row=5, column=1)

tk.Button(form_frame, text="DELETE", width=15, bg="#ff69b4",
          command=delete_employee).grid(row=6, column=0)

tk.Button(form_frame, text="CLEAR", width=15, bg="#ff69b4",
          command=clear_fields).grid(row=6, column=1)

# Search Frame
search_frame = tk.Frame(root, bd=4, relief=tk.RIDGE, bg="#f2a7c2")
search_frame.place(x=450, y=70, width=520, height=60)

tk.Label(search_frame, text="Search By",
         bg="#f2a7c2").grid(row=0, column=0, padx=5)

search_combo = ttk.Combobox(search_frame, textvariable=search_by,
                             values=["name", "email", "department"],
                             state="readonly", width=12)
search_combo.grid(row=0, column=1)
search_combo.current(0)

tk.Entry(search_frame, textvariable=search_txt,
         width=20).grid(row=0, column=2, padx=5)

tk.Button(search_frame, text="Search",
          command=search_employee).grid(row=0, column=3, padx=5)

tk.Button(search_frame, text="Show All",
          command=fetch_data).grid(row=0, column=4, padx=5)

# Table Frame
table_frame = tk.Frame(root, bd=4, relief=tk.RIDGE)
table_frame.place(x=450, y=140, width=520, height=400)

scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
employee_table = ttk.Treeview(
    table_frame,
    columns=("ID","Name","Email","Phone","Department","Salary"),
    yscrollcommand=scroll_y.set
)

scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_y.config(command=employee_table.yview)

for col in ("ID","Name","Email","Phone","Department","Salary"):
    employee_table.heading(col, text=col)
    employee_table.column(col, width=80)

employee_table["show"] = "headings"
employee_table.pack(fill=tk.BOTH, expand=1)
employee_table.bind("<ButtonRelease-1>", get_cursor)

fetch_data()
root.mainloop()