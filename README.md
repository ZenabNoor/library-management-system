# 📚 Library Management System

A desktop-based **Library Management System** developed in **Python** using **CustomTkinter** for the graphical user interface and **MySQL** as the backend database. The system allows librarians to efficiently manage books, members, book issuing/returning, and transaction records through an intuitive interface.

---

## ✨ Features

- 📖 View complete book catalog
- 🔍 Search books by title
- ➕ Add new books
- 📈 Update book stock
- 🗑️ Remove books
- 👤 Register new library members
- 👥 View all members
- 📤 Issue books to members
- 📥 Return issued books
- 📋 View transaction history
- 📊 Display library statistics

---

## 🛠️ Technologies Used

- Python 3
- CustomTkinter
- Tkinter
- MySQL
- MySQL Connector for Python

---

## 📂 Database Structure

The project uses a MySQL database named **projectdb** with the following tables:

### BOOK
| Column | Description |
|---------|-------------|
| ISBN | Primary Key |
| TITLE | Book Title |
| AUTHOR | Author Name |
| STOCK | Available Copies |

### MEMBER
| Column | Description |
|---------|-------------|
| MEMBER_ID | Primary Key |
| MEMBER_NAME | Member Name |

### TRANSACTIONS
| Column | Description |
|---------|-------------|
| ISSUE_ID | Auto Increment Primary Key |
| ISBN | Book ISBN |
| COPY_ID | Copy Number |
| MEMBER_ID | Member ID |
| MEMBER_NAME | Member Name |
| ISSUE_DATE | Date of Issue/Return |
| TRANSACTION_TYPE | ISSUE or RETURN |

---

## 📦 Installation

1. Clone the repository.

```bash
git clone https://github.com/yourusername/library-management-system.git
```

2. Install the required package.

```bash
pip install customtkinter mysql-connector-python
```

3. Create the MySQL database.

```sql
CREATE DATABASE projectdb;
```

4. Import or execute the SQL script to create the required tables.

5. Update the MySQL credentials in the Python file if necessary.

```python
host="localhost"
user="root"
password=""
database="projectdb"
```

6. Run the application.

```bash
python main.py
```

---

## 📸 User Interface

The application provides a modern dark-themed graphical interface with:

- Sidebar navigation
- Book catalog
- Member management
- Issue/Return system
- Transaction history
- Library statistics

---

## 📌 Future Improvements

- User authentication (Admin Login)
- Fine calculation for overdue books
- Book cover images
- Export reports to PDF/Excel
- Search by ISBN or Author
- Due date reminders
- Barcode support

---

## 👩‍💻 Author

**Zenab Noor**

Department of Artificial Intelligence

University of Sargodha

---

## 📄 License

This project was developed for educational purposes and academic learning.
