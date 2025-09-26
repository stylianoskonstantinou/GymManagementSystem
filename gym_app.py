from datetime import date, timedelta
import psycopg2
import tkinter as tk
from tkinter import messagebox, simpledialog

# --- ΣΥΝΔΕΣΗ ΜΕ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ ---
def connect():
    return psycopg2.connect(
        host="your_host",          # Π.χ. localhost ή η IP της βάσης σου
        port="5432",               # Συνήθης θύρα για PostgreSQL
        dbname="your_database",    # Όνομα της βάσης δεδομένων
        user="your_username",      # Το όνομα χρήστη
        password="your_password"   # Ο κωδικός πρόσβασης
    )


# --- ΠΡΟΣΘΗΚΗ ΜΕΛΟΥΣ ---
def add_member():
    name = simpledialog.askstring("Όνομα", "Δώσε όνομα:")
    surname = simpledialog.askstring("Επώνυμο", "Δώσε επώνυμο:")
    email = simpledialog.askstring("Email", "Δώσε email:")
    phone = simpledialog.askstring("Τηλέφωνο", "Δώσε τηλέφωνο:")

    if not all([name, surname, email, phone]):
        messagebox.showerror("Σφάλμα", "Όλα τα πεδία είναι υποχρεωτικά.")
        return

    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Member (name, surname, email, phone)
            VALUES (%s, %s, %s, %s) RETURNING member_id
        """, (name, surname, email, phone))
        member_id = cur.fetchone()[0]

        cur.execute("SELECT subscription_id, type FROM Subscription")
        subscriptions = cur.fetchall()
        options = "\n".join([f"{s[0]}: {s[1]}" for s in subscriptions])
        sub_id = simpledialog.askstring("Συνδρομή", f"Επίλεξε ID συνδρομής:\n{options}")

        cur.execute("SELECT duration_months FROM Subscription WHERE subscription_id = %s", (sub_id,))
        duration = cur.fetchone()
        if duration is None:
            messagebox.showerror("Σφάλμα", "Μη έγκυρο ID συνδρομής.")
            conn.rollback()
            return

        start_date = date.today()
        end_date = start_date + timedelta(days=duration[0]*30)

        cur.execute("""
            INSERT INTO Member_Subscription (member_id, subscription_id, start_date, end_date)
            VALUES (%s, %s, %s, %s)
        """, (member_id, sub_id, start_date, end_date))

        conn.commit()
        messagebox.showinfo("Επιτυχία", "Το μέλος προστέθηκε.")
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Σφάλμα", str(e))

# --- ΕΜΦΑΝΙΣΗ ΟΛΩΝ ΤΩΝ ΜΕΛΩΝ ---
def show_all_members():
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                m.member_id, m.name, m.surname, s.type, ms.start_date, ms.end_date
            FROM Member m
            LEFT JOIN Member_Subscription ms ON m.member_id = ms.member_id
            LEFT JOIN Subscription s ON ms.subscription_id = s.subscription_id
            ORDER BY m.member_id
        """)
        rows = cur.fetchall()
        output = ""
        for row in rows:
            if row[3]:
                output += f"ID: {row[0]} | {row[1]} {row[2]} | Συνδρομή: {row[3]} ({row[4]} έως {row[5]})\n"
            else:
                output += f"ID: {row[0]} | {row[1]} {row[2]} | Χωρίς συνδρομή\n"
        messagebox.showinfo("Μέλη", output or "Δεν υπάρχουν καταχωρημένα μέλη.")
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Σφάλμα", str(e))

# --- ΠΡΟΒΟΛΗ ΕΝΕΡΓΩΝ ΜΕΛΩΝ ---
def show_active_members():
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT m.member_id, m.name, m.surname, s.type, ms.end_date
            FROM Member m
            JOIN Member_Subscription ms ON m.member_id = ms.member_id
            JOIN Subscription s ON ms.subscription_id = s.subscription_id
            WHERE CURRENT_DATE BETWEEN ms.start_date AND ms.end_date
        """)
        rows = cur.fetchall()
        output = ""
        for row in rows:
            output += f"ID: {row[0]} | {row[1]} {row[2]} | Συνδρομή: {row[3]} | Λήξη: {row[4]}\n"
        messagebox.showinfo("Ενεργά μέλη", output or "Δεν υπάρχουν ενεργές συνδρομές σήμερα.")
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Σφάλμα", str(e))

# --- ΑΝΑΖΗΤΗΣΗ ΜΕ ΒΑΣΗ ΤΥΠΟ ΣΥΝΔΡΟΜΗΣ ---
def search_members_by_subscription():
    sub_type = simpledialog.askstring("Αναζήτηση", "Τύπος συνδρομής (π.χ. Ετήσια):")
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT m.member_id, m.name, m.surname, s.type, ms.start_date, ms.end_date
            FROM Member m
            JOIN Member_Subscription ms ON m.member_id = ms.member_id
            JOIN Subscription s ON ms.subscription_id = s.subscription_id
            WHERE s.type ILIKE %s
        """, (sub_type,))
        rows = cur.fetchall()
        output = ""
        for row in rows:
            output += f"ID: {row[0]} | {row[1]} {row[2]} | Συνδρομή: {row[3]} ({row[4]} έως {row[5]})\n"
        messagebox.showinfo("Αποτελέσματα", output or "Δεν βρέθηκαν μέλη με αυτή τη συνδρομή.")
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Σφάλμα", str(e))

# --- ΑΝΑΖΗΤΗΣΗ ΜΕ ΒΑΣΗ ΕΠΩΝΥΜΟ ---
def search_member_by_surname():
    surname = simpledialog.askstring("Αναζήτηση", "Δώσε επώνυμο μέλους:")
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                m.member_id, 
                m.name, 
                m.surname, 
                m.email, 
                m.phone,
                s.type, 
                ms.start_date, 
                ms.end_date
            FROM Member m
            LEFT JOIN Member_Subscription ms ON m.member_id = ms.member_id
            LEFT JOIN Subscription s ON ms.subscription_id = s.subscription_id
            WHERE m.surname ILIKE %s
        """, (f"%{surname}%",))
        rows = cur.fetchall()
        output = ""
        for row in rows:
            if row[5] is not None:
                output += (f"ID: {row[0]} | {row[1]} {row[2]} | Email: {row[3]} | Τηλ: {row[4]} | "
                           f"Συνδρομή: {row[5]} ({row[6]} έως {row[7]})\n")
            else:
                output += (f"ID: {row[0]} | {row[1]} {row[2]} | Email: {row[3]} | Τηλ: {row[4]} | "
                           "Χωρίς ενεργή συνδρομή\n")
        messagebox.showinfo("Αποτελέσματα", output or "Δεν βρέθηκαν μέλη με αυτό το επώνυμο.")
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Σφάλμα", str(e))

# --- ΥΠΟΛΟΙΠΕΣ ΛΕΙΤΟΥΡΓΙΕΣ ---
def update_member():
    member_id = simpledialog.askstring("Ενημέρωση", "ID μέλους για ενημέρωση:")
    new_email = simpledialog.askstring("Email", "Νέο email:")
    new_phone = simpledialog.askstring("Τηλέφωνο", "Νέο τηλέφωνο:")
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Member SET email = %s, phone = %s WHERE member_id = %s
        """, (new_email, new_phone, member_id))
        conn.commit()
        messagebox.showinfo("Αποτέλεσμα", "Τα στοιχεία ενημερώθηκαν." if cur.rowcount else "Δεν βρέθηκε μέλος.")
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Σφάλμα", str(e))

def delete_member():
    member_id = simpledialog.askstring("Διαγραφή", "ID μέλους για διαγραφή:")
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM Member_Subscription WHERE member_id = %s", (member_id,))
        cur.execute("DELETE FROM Attendance WHERE member_id = %s", (member_id,))
        cur.execute("DELETE FROM Member WHERE member_id = %s", (member_id,))
        conn.commit()
        messagebox.showinfo("Αποτέλεσμα", "Το μέλος διαγράφηκε." if cur.rowcount else "Δεν βρέθηκε μέλος.")
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Σφάλμα", str(e))

def add_attendance():
    member_id = simpledialog.askstring("Παρουσία", "ID μέλους:")
    date_str = simpledialog.askstring("Ημερομηνία", "Ημερομηνία παρουσίας (YYYY-MM-DD, κενό για σήμερα):")
    try:
        attendance_date = date.today() if not date_str else date.fromisoformat(date_str)
        conn = connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO Attendance (member_id, date) VALUES (%s, %s)", (member_id, attendance_date))
        conn.commit()
        messagebox.showinfo("Επιτυχία", "Η παρουσία καταχωρήθηκε.")
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Σφάλμα", str(e))

def show_attendance_summary():
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT m.member_id, m.name, m.surname, COUNT(*) AS total_visits
            FROM Member m
            JOIN Attendance a ON m.member_id = a.member_id
            WHERE DATE_TRUNC('month', a.date) = DATE_TRUNC('month', CURRENT_DATE)
            GROUP BY m.member_id, m.name, m.surname
            ORDER BY total_visits DESC
        """)
        rows = cur.fetchall()
        output = ""
        for row in rows:
            output += f"ID: {row[0]} | {row[1]} {row[2]} | Παρουσίες: {row[3]}\n"
        messagebox.showinfo("Παρουσίες Μήνα", output or "Δεν υπάρχουν παρουσίες αυτό το μήνα.")
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Σφάλμα", str(e))

# --- GUI ---
root = tk.Tk()
root.title("Σύστημα Γυμναστηρίου")
root.geometry("400x600")

buttons = [
    ("➕ Προσθήκη Μέλους", add_member),
    ("📋 Εμφάνιση Μελών", show_all_members),
    ("🟢 Ενεργά Μέλη", show_active_members),
    ("🔍 Αναζήτηση Συνδρομής", search_members_by_subscription),
    ("🧍‍♂️ Αναζήτηση Επώνυμου", search_member_by_surname),
    ("📅 Παρουσίες Μήνα", show_attendance_summary),
    ("➕ Καταγραφή Παρουσίας", add_attendance),
    ("✏️ Ενημέρωση Μέλους", update_member),
    ("❌ Διαγραφή Μέλους", delete_member)
]

for text, command in buttons:
    tk.Button(root, text=text, command=command).pack(pady=5)

root.mainloop()
