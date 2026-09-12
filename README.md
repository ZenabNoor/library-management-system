
# 📚 Library Management System

A desktop-based Library Management System developed in Python using CustomTkinter for the graphical user interface and MySQL as the backend database. The system allows librarians to efficiently manage books, members, book issuing/returning, and transaction records through an intuitive interface.

---

## ✨ Features

* 📖 **View Book Catalog:** Browse complete book collection with stock levels.
* 🔍 **Search Functionality:** Quickly search books by title.
* ➕ **Book Management:** Add new books, update stock counts, or remove records.
* 👤 **Member Tracking:** Register new library members and view all members.
* 📤 **Issue & Return System:** Process book issuance and track returns dynamically.
* 📋 **Transaction History:** View complete transaction logs and history.
* 📊 **Library Statistics:** Display real-time library usage statistics.

---

## 🛠️ Technologies Used

* **Python 3**
* **CustomTkinter** (Modern GUI toolkit)
* **Tkinter**
* **MySQL** & **MySQL Connector for Python**

---

## 📂 Database Structure

The project connects to a MySQL database named `projectdb` featuring three main tables:

### `BOOK`

| Column | Description |
| --- | --- |
| **`ISBN`** | Primary Key |
| **`TITLE`** | Book Title |
| **`AUTHOR`** | Author Name |
| **`STOCK`** | Available Copies |

### `MEMBER`

| Column | Description |
| --- | --- |
| **`MEMBER_ID`** | Primary Key |
| **`MEMBER_NAME`** | Member Name |

### `TRANSACTIONS`

| Column | Description |
| --- | --- |
| **`ISSUE_ID`** | Auto Increment Primary Key |
| **`ISBN`** | Book ISBN (Foreign Key) |
| **`COPY_ID`** | Copy Number |
| **`MEMBER_ID`** | Member ID (Foreign Key) |
| **`MEMBER_NAME`** | Member Name |
| **`ISSUE_DATE`** | Date of Issue/Return |
| **`TRANSACTION_TYPE`** | `ISSUE` or `RETURN` |

---

## 📦 Installation & Setup

1. **Clone the repository:**
git clone [https://github.com/ZenabNoor/library-management-system.git](https://www.google.com/search?q=https://github.com/ZenabNoor/library-management-system.git)
cd library-management-system
2. **Install required packages:**
pip install customtkinter mysql-connector-python
3. **Database Configuration:**
* Create a MySQL database named `projectdb`:
CREATE DATABASE projectdb;
* Execute the SQL schema script located in the `/docs` or `/src` directory to set up the required tables.
* Update your local MySQL credentials in `src/finaldb.py`:
host = "localhost"
user = "root"
password = "YOUR_MYSQL_PASSWORD"
database = "projectdb"


4. **Run the Application:**
python src/finaldb.py

---

## 📄 Project Documentation & Assets

All architecture diagrams and specifications can be found in their designated folders:

* 📁 **`docs/`** – Contains SRS, SDS, Test Plan, and Project Proposal documents.
* 📁 **`diagrams/`** – Contains ER Diagrams, Data Flow Diagrams, and Use Case Diagrams.
* 📁 **`media/`** – Contains the application demonstration video.
* 📁 **`src/`** – Contains the core Python source code (`finaldb.py`).

---

## 📌 Future Improvements

* [ ] User authentication (Admin Login system)
* [ ] Fine calculation for overdue books
* [ ] Book cover images support
* [ ] Export reports to PDF/Excel
* [ ] Search by ISBN or Author
* [ ] Due date email reminders
* [ ] Barcode reader integration

---

## 👩‍💻 Author

**Zenab Noor**

Department of Artificial Intelligence

University of Sargodha

---

## 📜 License

This project was developed for educational purposes and academic learning.

