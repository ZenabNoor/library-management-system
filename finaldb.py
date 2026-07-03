import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector

# ==============================================================================
# --- CUTESY AESTHETIC CONFIGURATION ---
# ==============================================================================
ctk.set_appearance_mode("Dark")
BG_COLOR = "#1a1a1a"
SIDEBAR_COLOR = "#252525"
CARD_COLOR = "#2d2d2d"
TEXT_COLOR = "#f4f1ea"
ACCENT_COLOR = "#d4a373"

COLOR_CAT = "#6B8E72"
COLOR_ADD_B = "#D4A373"
COLOR_ADD_M = "#A39171"
COLOR_VIEW_M = "#7395AE"
COLOR_ISSUE = "#B07D62"
COLOR_RETURN = "#9B72AA"
COLOR_TRANS = "#D78E8E"
COLOR_DANGER = "#bf4e4e"

# ==============================================================================
# --- MAIN APPLICATION CLASS ---
# ==============================================================================
class LMS(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("✨ Library Management System ✨")
        self.geometry("1150x750")
        self.configure(fg_color=BG_COLOR)
        
        self.db_connection = None
        self.db_cursor = None
        
        self.init_database()
        self.sidebar = self.setup_sidebar()
        self.main_area = self.setup_main_area()
        self.catalog()

    def init_database(self):
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost", user="root", password="", database="projectdb"
            )
            self.db_cursor = self.db_connection.cursor()
        except Exception as err:
            messagebox.showerror("Connection Error", f"Could not connect: {err}")

    def setup_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=260, fg_color=SIDEBAR_COLOR, corner_radius=25)
        sidebar.pack(side="left", fill="y", padx=20, pady=20)
        sidebar.pack_propagate(False)

        ctk.CTkLabel(sidebar, text="🌿 My Library 🌿",
                     font=ctk.CTkFont(family="Georgia", size=24, weight="bold"),
                     text_color=ACCENT_COLOR).pack(pady=30)

        self.create_nav_button(sidebar, "📖 Catalog", self.catalog, COLOR_CAT)
        self.create_nav_button(sidebar, "🔍 Search Book", self.search_book_ui, COLOR_VIEW_M)
        self.create_nav_button(sidebar, "➕ Add Book", self.add_book_ui, COLOR_ADD_B)
        self.create_nav_button(sidebar, "📈 Update Stock", self.update_stock_ui, COLOR_CAT)
        self.create_nav_button(sidebar, "🗑️ Remove Book", self.remove_book_ui, COLOR_DANGER)
        self.create_nav_button(sidebar, "👤 Add Member", self.add_member_ui, COLOR_ADD_M)
        self.create_nav_button(sidebar, "👥 View Members", self.view_members, COLOR_VIEW_M)
        self.create_nav_button(sidebar, "📤 Issue Book", self.issue_ui, COLOR_ISSUE)
        self.create_nav_button(sidebar, "📥 Return Book", self.return_ui, COLOR_RETURN)
        self.create_nav_button(sidebar, "📋 Transactions", self.transactions_ui, COLOR_TRANS)
        self.create_nav_button(sidebar, "📊 Stats", self.show_stats, ACCENT_COLOR)
        
        ctk.CTkLabel(sidebar, text="🦉✨", font=ctk.CTkFont(size=25)).pack(side="bottom", pady=20)
        return sidebar

    def setup_main_area(self):
        main = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=25)
        main.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)
        return main

    def create_nav_button(self, parent, text, command, color):
        ctk.CTkButton(parent, text=text, command=command, fg_color=color, 
                      hover_color="#404040", text_color="white", height=38, 
                      corner_radius=12, font=ctk.CTkFont(size=14, weight="bold")
                      ).pack(fill="x", padx=30, pady=4)

    def create_input_field(self, placeholder):
        entry = ctk.CTkEntry(self.main_area, placeholder_text=placeholder, width=380, height=45, corner_radius=15)
        entry.pack(pady=10)
        return entry

    def render_footer(self):
        self.footer_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.footer_frame.pack(side="bottom", fill="x", pady=10, padx=20)
        ctk.CTkLabel(self.footer_frame, text="“A reader lives a thousand lives before he dies.” — George R.R. Martin 📚✨", 
                     font=ctk.CTkFont(family="Georgia", size=13, slant="italic"), text_color="#888888").pack(side="left")
        ctk.CTkLabel(self.footer_frame, text="🐈💤📚", font=ctk.CTkFont(size=24)).pack(side="right", padx=10)

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()
        self.render_footer()

    # --- CORE BUSINESS LOGIC ---
    def catalog(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="BOOK CATALOG", font=ctk.CTkFont(size=30, weight="bold"), text_color=ACCENT_COLOR).pack(pady=30)
        container = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=40, pady=20)
        headers = ["ISBN", "TITLE", "AUTHOR", "STOCK"]
        for idx, header in enumerate(headers):
            ctk.CTkLabel(container, text=header, font=ctk.CTkFont(weight="bold", size=15), text_color=ACCENT_COLOR).grid(row=0, column=idx, padx=40, pady=15)
        self.db_cursor.execute("SELECT * FROM BOOK")
        for r, row in enumerate(self.db_cursor.fetchall(), start=1):
            for c, val in enumerate(row):
                ctk.CTkLabel(container, text=str(val)).grid(row=r, column=c, padx=40, pady=10)

    def issue_ui(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Time to Borrow 📤✨", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=40)
        self.f_isbn = self.create_input_field("ISBN")
        self.f_mid = self.create_input_field("Member ID")
        self.f_mname = self.create_input_field("Member Name")
        ctk.CTkButton(self.main_area, text="Issue Book 📖", command=self.issue_exec, fg_color=COLOR_ISSUE, height=45, corner_radius=15).pack(pady=30)

    def issue_exec(self):
        try:
            # Check book stock
            self.db_cursor.execute("SELECT STOCK FROM BOOK WHERE ISBN=%s", (self.f_isbn.get(),))
            book = self.db_cursor.fetchone()
            
            # Check member existence
            self.db_cursor.execute("SELECT MEMBER_NAME FROM MEMBER WHERE MEMBER_ID=%s", (self.f_mid.get(),))
            member = self.db_cursor.fetchone()

            if not book: 
                messagebox.showerror("Error", "ISBN not found.")
            elif book[0] <= 0: 
                messagebox.showerror("Error", "Out of stock.")
            elif not member: 
                messagebox.showerror("Error", "Member ID not found.")
            elif member[0].strip().lower() != self.f_mname.get().strip().lower():
                messagebox.showerror("Error", f"Mismatch: ID belongs to {member[0]}.")
            else:
                # Calculate next copy ID
                self.db_cursor.execute("SELECT MAX(COPY_ID) FROM TRANSACTIONS WHERE ISBN=%s", (self.f_isbn.get(),))
                res = self.db_cursor.fetchone()
                new_copy_id = (res[0] + 1) if res[0] else 1
                
                # FIXED: Ensure column names match your DB schema (use MEMBER_NAME instead of NAME)
                sql = "INSERT INTO TRANSACTIONS (ISBN, COPY_ID, MEMBER_ID, MEMBER_NAME, ISSUE_DATE, TRANSACTION_TYPE) VALUES (%s, %s, %s, %s, CURDATE(), 'ISSUE')"
                self.db_cursor.execute(sql, (self.f_isbn.get(), new_copy_id, self.f_mid.get(), self.f_mname.get()))
                
                self.db_cursor.execute("UPDATE BOOK SET STOCK = STOCK - 1 WHERE ISBN=%s", (self.f_isbn.get(),))
                self.db_connection.commit()
                messagebox.showinfo("Success", f"Issued! Copy ID: {new_copy_id}")
        except Exception as e: 
            messagebox.showerror("Database Error", str(e))

    def view_members(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="THE LIBRARY FAMILY", font=ctk.CTkFont(size=26, weight="bold"), text_color=ACCENT_COLOR).pack(pady=30)
        box = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        box.pack(fill="both", expand=True, padx=40, pady=20)
        headers = ["ID", "NAME"]
        for idx, h in enumerate(headers): ctk.CTkLabel(box, text=h, font=ctk.CTkFont(weight="bold")).grid(row=0, column=idx, padx=80, pady=10)
        self.db_cursor.execute("SELECT * FROM MEMBER")
        for r, row in enumerate(self.db_cursor.fetchall(), start=1):
            for c, val in enumerate(row): ctk.CTkLabel(box, text=str(val)).grid(row=r, column=c, padx=80, pady=10)

    def transactions_ui(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="TRANSACTION HISTORY", font=ctk.CTkFont(size=26, weight="bold"), text_color=ACCENT_COLOR).pack(pady=30)
        box = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        box.pack(fill="both", expand=True, padx=40, pady=20)
        
        # 1. Definitive header list
        headers = ["T_ID", "ISBN", "COPY_ID", "M_ID", "NAME", "DATE", "TYPE"]
        for idx, h in enumerate(headers):
            ctk.CTkLabel(box, text=h, font=ctk.CTkFont(weight="bold", size=13), text_color=ACCENT_COLOR).grid(row=0, column=idx, padx=15, pady=10)
        
        # 2. Explicitly select columns in the exact order above
        query = "SELECT ISSUE_ID, ISBN, COPY_ID, MEMBER_ID, MEMBER_NAME, ISSUE_DATE, TRANSACTION_TYPE FROM TRANSACTIONS"
        self.db_cursor.execute(query)
        
        # 3. Render data rows
        for r, row in enumerate(self.db_cursor.fetchall(), start=1):
            for c, val in enumerate(row):
                ctk.CTkLabel(box, text=str(val), font=ctk.CTkFont(size=12)).grid(row=r, column=c, padx=15, pady=10)
    # --- OTHER UI METHODS (RETAINED) ---
    def return_ui(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Return a Book 📥♻️", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=40)
        self.r_isbn = self.create_input_field("ISBN")
        self.r_mid = self.create_input_field("Member ID")
        self.r_mname = self.create_input_field("Member Name")
        self.r_copy = self.create_input_field("Copy ID")
        ctk.CTkButton(self.main_area, text="Return Book 🌷", command=self.return_exec, fg_color=COLOR_RETURN, height=45, corner_radius=15).pack(pady=30)

    def return_exec(self):
        try:
            query = "SELECT ISSUE_ID FROM TRANSACTIONS WHERE ISBN=%s AND COPY_ID=%s AND MEMBER_ID=%s AND MEMBER_NAME=%s AND TRANSACTION_TYPE='ISSUE'"
            self.db_cursor.execute(query, (self.r_isbn.get(), self.r_copy.get(), self.r_mid.get(), self.r_mname.get()))
            if not self.db_cursor.fetchone():
                messagebox.showerror("Error", "Invalid Return: Record not found.")
                return
            self.db_cursor.execute("INSERT INTO TRANSACTIONS (ISBN, COPY_ID, MEMBER_ID, MEMBER_NAME, ISSUE_DATE, TRANSACTION_TYPE) VALUES (%s,%s,%s,%s,CURDATE(),'RETURN')", 
                                   (self.r_isbn.get(), self.r_copy.get(), self.r_mid.get(), self.r_mname.get()))
            self.db_cursor.execute("UPDATE BOOK SET STOCK = STOCK + 1 WHERE ISBN=%s", (self.r_isbn.get(),))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Returned!")
        except Exception as e: messagebox.showerror("Database Error", str(e))

    def add_book_ui(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="New Story Arrival ✨📚", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=40)
        self.i1 = self.create_input_field("ISBN")
        self.i2 = self.create_input_field("Title")
        self.i3 = self.create_input_field("Author")
        self.i4 = self.create_input_field("Stock")
        ctk.CTkButton(self.main_area, text="Add to Shelf 🚀", command=self.add_book_exec, fg_color=COLOR_ADD_B, height=45, corner_radius=15).pack(pady=30)

    def add_book_exec(self):
        try:
            self.db_cursor.execute("INSERT INTO BOOK VALUES (%s,%s,%s,%s)", (self.i1.get(), self.i2.get(), self.i3.get(), int(self.i4.get())))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Added!")
        except Exception as e: messagebox.showerror("Error", str(e))

    def add_member_ui(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="New Reader 👤💖", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=40)
        self.m1 = self.create_input_field("Member ID")
        self.m2 = self.create_input_field("Member Name")
        ctk.CTkButton(self.main_area, text="Register 🌸", command=self.add_member_exec, fg_color=COLOR_ADD_M, height=45, corner_radius=15).pack(pady=30)

    def add_member_exec(self):
        try:
            self.db_cursor.execute("INSERT INTO MEMBER VALUES (%s,%s)", (int(self.m1.get()), self.m2.get()))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Registered!")
        except Exception as e: messagebox.showerror("Error", str(e))

    def search_book_ui(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Find a Story 🔍", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=40)
        self.s_entry = self.create_input_field("Enter Book Title...")
        ctk.CTkButton(self.main_area, text="Search 🔎", command=self.search_book_exec, fg_color=COLOR_VIEW_M, height=45, corner_radius=15).pack(pady=20)
        self.res_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.res_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def search_book_exec(self):
        for w in self.res_frame.winfo_children(): w.destroy()
        self.db_cursor.execute("SELECT * FROM BOOK WHERE TITLE LIKE %s", (f"%{self.s_entry.get()}%",))
        for row in self.db_cursor.fetchall(): ctk.CTkLabel(self.res_frame, text=str(row)).pack(pady=5)

    def remove_book_ui(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Remove from Shelf 🗑️", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=40)
        self.rem_isbn = self.create_input_field("Enter ISBN to Remove")
        ctk.CTkButton(self.main_area, text="Confirm Delete ⚠️", command=self.remove_book_exec, fg_color=COLOR_DANGER, height=45, corner_radius=15).pack(pady=30)

    def remove_book_exec(self):
        try:
            isbn = self.rem_isbn.get()
            # Validation: Check if book exists
            self.db_cursor.execute("SELECT ISBN FROM BOOK WHERE ISBN=%s", (isbn,))
            if not self.db_cursor.fetchone():
                messagebox.showerror("Error", f"ISBN '{isbn}' does not exist in catalog.")
                return
            
            # Delete
            self.db_cursor.execute("DELETE FROM BOOK WHERE ISBN=%s", (isbn,))
            self.db_connection.commit()
            messagebox.showinfo("Done", "Book removed successfully.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            
    def update_stock_ui(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Update Stock 📉📈", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=40)
        self.up_isbn = self.create_input_field("ISBN")
        self.up_val = self.create_input_field("New Quantity")
        ctk.CTkButton(self.main_area, text="Update 🔄", command=self.update_stock_exec, fg_color=COLOR_CAT, height=45, corner_radius=15).pack(pady=30)

    def update_stock_exec(self):
        try:
            isbn = self.up_isbn.get()
            # Validation: Check if book exists
            self.db_cursor.execute("SELECT STOCK FROM BOOK WHERE ISBN=%s", (isbn,))
            result = self.db_cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error", f"ISBN '{isbn}' does not exist.")
                return
            
            # Execute update
            self.db_cursor.execute("UPDATE BOOK SET STOCK=%s WHERE ISBN=%s", (self.up_val.get(), isbn))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Stock updated.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def show_stats(self):
        self.clear_main_area()
        self.db_cursor.execute("SELECT COUNT(*) FROM BOOK")
        b = self.db_cursor.fetchone()[0]
        self.db_cursor.execute("SELECT COUNT(*) FROM MEMBER")
        m = self.db_cursor.fetchone()[0]
        ctk.CTkLabel(self.main_area, text=f"Total Books: {b}\nTotal Members: {m}", font=ctk.CTkFont(size=20)).pack(pady=40)

if __name__ == "__main__":
    app = LMS()
    app.mainloop()