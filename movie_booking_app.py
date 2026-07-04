from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import hashlib

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
PRICE_PER_SEAT = 300
ALL_SEATS = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4"]

# Shared data across all pages (replaces session.json)
session = {}


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------
def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


def init_db():
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            movie TEXT NOT NULL,
            theatre TEXT NOT NULL,
            show_time TEXT NOT NULL,
            seat TEXT NOT NULL,
            amount INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_booking():
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO bookings (username, movie, theatre, show_time, seat, amount)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (session["username"], session["movie"], session["theatre"],
          session["show"], session["seat"], session["amount"]))
    conn.commit()
    conn.close()


# ---------------------------------------------------------
# WINDOW SETUP
# ---------------------------------------------------------
root = Tk()
root.title("Movie Ticket Booking")
root.geometry("700x500")
root.configure(bg="#a54b91")

container = Frame(root, bg="#1f2e22")
container.pack(fill=BOTH, expand=True)


def clear_container():
    for widget in container.winfo_children():
        widget.destroy()


# ---------------------------------------------------------
# PAGE 1: LOGIN / REGISTER
# ---------------------------------------------------------
def show_login():
    clear_container()

    Label(container, text="Movie Ticket Booking", font=("Arial", 20, "bold"),
          fg="orange", bg="#1f1f2e").pack(pady=20)

    Label(container, text="Username", bg="#1f1f2e", fg="white").pack()
    username_entry = Entry(container, width=30)
    username_entry.pack(pady=5)

    Label(container, text="Password", bg="#1f1f2e", fg="white").pack()
    password_entry = Entry(container, show="*", width=30)
    password_entry.pack(pady=5)

    def register():
        uname = username_entry.get().strip()
        pwd = password_entry.get().strip()
        if not uname or not pwd:
            messagebox.showwarning("Warning", "Please fill in both fields")
            return

        conn = sqlite3.connect("movie.db")
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users(username, password) VALUES(?, ?)",
                        (uname, hash_password(pwd)))
            conn.commit()
            messagebox.showinfo("Success", "Registration Successful")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()

    def login():
        uname = username_entry.get().strip()
        pwd = password_entry.get().strip()
        if not uname or not pwd:
            messagebox.showwarning("Warning", "Please fill in both fields")
            return

        conn = sqlite3.connect("movie.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                    (uname, hash_password(pwd)))
        user = cur.fetchone()
        conn.close()

        if user:
            session["username"] = uname
            messagebox.showinfo("Success", "Login Successful")
            show_movie_selection()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    Button(container, text="Login", command=login, bg="gold", width=15).pack(pady=10)
    Button(container, text="Register", command=register, bg="gray", fg="white", width=15).pack()


# ---------------------------------------------------------
# PAGE 2: MOVIE / THEATRE / SHOW SELECTION
# ---------------------------------------------------------
def show_movie_selection():
    clear_container()

    Label(container, text="Now Showing", font=("Arial", 20, "bold"),
          fg="orange", bg="#1f1f2e").pack(pady=10)

    Label(container, text=f"Welcome, {session.get('username', 'Guest')}",
          fg="lightgreen", bg="#1f1f2e").pack(pady=(0, 10))

    Label(container, text="Movie", bg="#1f1f2e", fg="white").pack()
    movie_box = ttk.Combobox(container, width=30)
    movie_box["values"] = ("Leo", "Jailer", "GOAT", "Coolie")
    movie_box.pack(pady=5)

    Label(container, text="Theatre", bg="#1f1f2e", fg="white").pack()
    theatre_box = ttk.Combobox(container, width=30)
    theatre_box["values"] = ("PVR Chennai", "INOX", "AGS", "Sathyam Cinemas")
    theatre_box.pack(pady=5)

    Label(container, text="Show Time", bg="#1f1f2e", fg="white").pack()
    show_box = ttk.Combobox(container, width=30)
    show_box["values"] = ("10:00 AM", "02:00 PM", "06:00 PM", "09:00 PM")
    show_box.pack(pady=5)

    def next_page():
        if movie_box.get() == "" or theatre_box.get() == "" or show_box.get() == "":
            messagebox.showerror("Error", "Please select all details")
            return

        session["movie"] = movie_box.get()
        session["theatre"] = theatre_box.get()
        session["show"] = show_box.get()
        show_seat_selection()

    Button(container, text="Next", command=next_page, bg="gold", width=20).pack(pady=30)


# ---------------------------------------------------------
# PAGE 3: SEAT SELECTION
# ---------------------------------------------------------
def show_seat_selection():
    clear_container()

    Label(container, text="Seat Selection", font=("Arial", 20, "bold"),
          fg="orange", bg="#1f1f2e").pack(pady=15)

    summary = f"Movie: {session['movie']}   |   Theatre: {session['theatre']}   |   Show: {session['show']}"
    Label(container, text=summary, fg="lightgreen", bg="#1f1f2e").pack(pady=(0, 15))

    seat_vars = {}
    grid_frame = Frame(container, bg="#1f1f2e")
    grid_frame.pack()

    for i, seat in enumerate(ALL_SEATS):
        var = BooleanVar()
        seat_vars[seat] = var
        Checkbutton(grid_frame, text=seat, variable=var,
                    bg="#1f1f2e", fg="white", selectcolor="#333",
                    activebackground="#1f1f2e", activeforeground="white").grid(
            row=i // 4, column=i % 4, padx=10, pady=10)

    def confirm_seats():
        selected = [seat for seat, var in seat_vars.items() if var.get()]
        if not selected:
            messagebox.showerror("Error", "Please select at least one seat")
            return

        amount = len(selected) * PRICE_PER_SEAT
        session["seat"] = ", ".join(selected)
        session["amount"] = amount
        show_booking_summary()

    Button(container, text="Confirm & Pay", command=confirm_seats, bg="gold", width=20).pack(pady=30)


# ---------------------------------------------------------
# PAGE 4: BOOKING SUMMARY
# ---------------------------------------------------------
def show_booking_summary():
    clear_container()

    Label(container, text="Booking Summary", font=("Arial", 20, "bold"),
          fg="orange", bg="#1f1f2e").pack(pady=20)

    Label(container, text="Username : " + session["username"], bg="#1f1f2e", fg="white", font=("Arial", 12)).pack(pady=5)
    Label(container, text="Movie : " + session["movie"], bg="#1f1f2e", fg="white", font=("Arial", 12)).pack(pady=5)
    Label(container, text="Theatre : " + session["theatre"], bg="#1f1f2e", fg="white", font=("Arial", 12)).pack(pady=5)
    Label(container, text="Show Time : " + session["show"], bg="#1f1f2e", fg="white", font=("Arial", 12)).pack(pady=5)
    Label(container, text="Seats : " + session["seat"], bg="#1f1f2e", fg="white", font=("Arial", 12)).pack(pady=5)

    Label(container, text="Total Amount : \u20b9" + str(session["amount"]),
          bg="#1f1f2e", fg="yellow", font=("Arial", 14, "bold")).pack(pady=15)

    def confirm():
        save_booking()
        show_confirmation()

    Button(container, text="Confirm Booking", command=confirm, bg="gold", width=20).pack(pady=20)


# ---------------------------------------------------------
# PAGE 5: FINAL CONFIRMATION
# ---------------------------------------------------------
def show_confirmation():
    clear_container()

    Label(container, text="Booking Successful!", font=("Arial", 20, "bold"),
          fg="green", bg="#1f1f2e").pack(pady=20)

    Label(container, text="Thank You for Booking", font=("Arial", 14),
          fg="white", bg="#1f1f2e").pack()

    Label(container, text="Movie : " + session["movie"], bg="#1f1f2e", fg="white").pack(pady=5)
    Label(container, text="Theatre : " + session["theatre"], bg="#1f1f2e", fg="white").pack(pady=5)
    Label(container, text="Show Time : " + session["show"], bg="#1f1f2e", fg="white").pack(pady=5)
    Label(container, text="Seat : " + session["seat"], bg="#1f1f2e", fg="white").pack(pady=5)

    Label(container, text="Amount Paid : \u20b9" + str(session["amount"]),
          bg="#1f1f2e", fg="yellow", font=("Arial", 12, "bold")).pack(pady=10)

    Button(container, text="Exit", command=root.destroy, bg="red", fg="white", width=15).pack(pady=20)

    messagebox.showinfo("Success", "Booking Saved Successfully!")


# ---------------------------------------------------------
# START
# ---------------------------------------------------------
init_db()
show_login()
root.mainloop()
