#include <iostream>
#include <string>
#include <stdexcept>
#include <windows.h>
#include <wininet.h>

#pragma comment(lib, "wininet.lib")

using namespace std;

string globalDataResult = "";

// Handles HTTP POST request to the local PHP bridge
void runXAMPPQuery(string sqlQuery) {
    HINTERNET hInternet = InternetOpenA("LMS_App", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (!hInternet) return;

    HINTERNET hConnect = InternetConnectA(hInternet, "127.0.0.1", INTERNET_DEFAULT_HTTP_PORT, NULL, NULL, INTERNET_SERVICE_HTTP, 0, 0);
    if (!hConnect) {
        InternetCloseHandle(hInternet);
        return;
    }

    HINTERNET hRequest = HttpOpenRequestA(hConnect, "POST", "/query_bridge.php", NULL, NULL, NULL, INTERNET_FLAG_RELOAD, 0);
    if (!hRequest) {
        InternetCloseHandle(hConnect);
        InternetCloseHandle(hInternet);
        return;
    }

    string jsonPayload = "{\"query\":\"" + sqlQuery + "\"}";
    string headers = "Content-Type: application/json\r\n";

    BOOL sendReq = HttpSendRequestA(hRequest, headers.c_str(), headers.length(), (LPVOID)jsonPayload.c_str(), jsonPayload.length());
    
    globalDataResult = ""; 
    if (sendReq) {
        char buffer[2048];
        DWORD bytesRead;
        while (InternetReadFile(hRequest, buffer, sizeof(buffer) - 1, &bytesRead) && bytesRead > 0) {
            buffer[bytesRead] = '\0';
            globalDataResult += buffer;
        }
    } else {
        cout << "Database connection stream failed." << endl;
    }

    InternetCloseHandle(hRequest);
    InternetCloseHandle(hConnect);
    InternetCloseHandle(hInternet);
}

// Parses tab-separated fields from the database response string
string getFieldFromRecord(string record, int fieldIndex) {
    size_t start = 0;
    size_t end = record.find("\t| ");
    int currentIdx = 0;
    
    while (end != string::npos) {
        if (currentIdx == fieldIndex) {
            return record.substr(start, end - start);
        }
        start = end + 3; 
        end = record.find("\t| ", start);
        currentIdx++;
    }
    if (currentIdx == fieldIndex) {
        string last = record.substr(start);
        if(!last.empty() && last.back() == '\n') last.pop_back();
        return last;
    }
    return "";
}

class Person {
protected:
    string name;
    int ID;
public:
    Person() { name="Unknown"; ID=0; }
    Person(string n, int id) { name = n; ID = id; }
    virtual void display() {
        cout << "Name: " << name << endl;
        cout << "ID: " << ID << endl;
    }
    virtual ~Person() { cout << "Destroying..." << endl; }
};

class Book {
private:
    string ISBN; 
    string title;
    string author;
    int TotalCopies;
    bool IsIssued;
public:
    Book() { ISBN = "000"; title = "Unknown"; author = "Unknown"; TotalCopies = 0; IsIssued = false; }
    Book(string isbn, string t, string a, int copies) {
        ISBN = isbn; title = t; author = a; TotalCopies = copies; IsIssued = false;
    }
    void Issuebook() {
        if (TotalCopies <= 0) throw runtime_error("No available physical stock left in database inventory!");    
        IsIssued = true;
        TotalCopies--; 
        cout << "Book issued successfully!!" << endl;
    }
    void returnbook() {
        IsIssued = false;
        TotalCopies++; 
        cout << "Book has successfully returned!!" << endl;
    }
    friend ostream& operator << (ostream & out, const Book & b) {
        out << "ISBN: " << b.ISBN << "\nBook Title: " << b.title << "\nBook Author: " << b.author
            << "\nStock Count: " << b.TotalCopies << endl;
        return out;
    }
    string Get_Isbn() { return ISBN; }
};

class User : public Person {
public:
    User() : Person() {}
    User(string n, int id) : Person(n, id) {}
    virtual void display() { cout << "User's details..." << endl; Person::display(); }
};

class Student : public User {
public:
    Student() : User() {}
    Student(string n, int id) : User(n, id) {}
    void display() { cout << "Student's details..." << endl; Person::display(); }
};

class Librarian : public User {
public:
    Librarian() : User() {}
    Librarian(string n, int id) : User(n, id) {}
    void display() { cout << "Librarian's details..." << endl; Person::display(); }
};

class Library {
public:
    void issue (Book & b) {
        try { 
            b.Issuebook(); 
            runXAMPPQuery("UPDATE BOOK SET TOTAL_COPIES = TOTAL_COPIES - 1 WHERE ISBN = '" + b.Get_Isbn() + "';");
            
            cout << "\n[ Issued Book Details (Updated Live) ]\n" << b;
            cout << "Book issued from library." << endl; 
        }  
        catch (const runtime_error & e) { cout << "Error: " << e.what() << endl; }
    }
    void returnbook (Book & b) {
        try { 
            b.returnbook(); 
            runXAMPPQuery("UPDATE BOOK SET TOTAL_COPIES = TOTAL_COPIES + 1 WHERE ISBN = '" + b.Get_Isbn() + "';");
            
            cout << "\n[ Returned Book Details (Updated Live) ]\n" << b;
            cout << "Book successfully returned to library." << endl; 
        }  
        catch (const runtime_error& e) { cout << "Error: " << e.what() << endl; }
    }
};

int main() {
    Library lib;
    Student s1("Sania", 156);
    Librarian L1("Amna", 160);

    int choice;
    do {
        cout << "===================LIBRARY MANAGEMENT SYSTEM=====================\n";
        cout << "1. Display Student\n";
        cout << "2. Display Librarian\n";
        cout << "3. Issue Book (LIVE DATA MODIFICATION)\n";
        cout << "4. Return Book (LIVE DATA MODIFICATION)\n";
        cout << "5. Show All Book Table Catalog (From XAMPP)\n";
        cout << "6. Dynamic Book Search (Search by Title)\n";
        cout << "0. Exit\n";
        cout << "Enter Choice: ";
        cin >> choice;
        
        string inputIsbn;

        switch (choice) {
            case 1: {
                Person* p1 = &s1; p1->display(); break;
            }
            case 2: {
                Person* p2 = &L1; p2->display(); break;
            }
            case 3: {
                cout << "Enter Book ISBN to issue: "; 
                cin >> inputIsbn;
                
                runXAMPPQuery("SELECT ISBN, TITLE, AUTHOR_NAME, TOTAL_COPIES FROM BOOK WHERE ISBN = '" + inputIsbn + "';");
                
                if (globalDataResult.empty() || globalDataResult.find("Error") != string::npos || globalDataResult == "\n") {
                    cout << "Error: This book ISBN record does not exist in the live database archive!" << endl;
                } else {
                    string t = getFieldFromRecord(globalDataResult, 1);
                    string a = getFieldFromRecord(globalDataResult, 2);
                    int copies = stoi(getFieldFromRecord(globalDataResult, 3));
                    
                    Book b(inputIsbn, t, a, copies);
                    lib.issue(b);
                }
                break;
            }
            case 4: {
                cout << "Enter Book ISBN to return: "; 
                cin >> inputIsbn;
                
                runXAMPPQuery("SELECT ISBN, TITLE, AUTHOR_NAME, TOTAL_COPIES FROM BOOK WHERE ISBN = '" + inputIsbn + "';");
                
                if (globalDataResult.empty() || globalDataResult.find("Error") != string::npos || globalDataResult == "\n") {
                    cout << "Error: Impossible transactional rollback. This catalog item does not belong to this library!" << endl;
                } else {
                    string t = getFieldFromRecord(globalDataResult, 1);
                    string a = getFieldFromRecord(globalDataResult, 2);
                    int copies = stoi(getFieldFromRecord(globalDataResult, 3));
                    
                    Book b(inputIsbn, t, a, copies);
                    lib.returnbook(b);
                }
                break;
            }
            case 5: {
                cout << "\n================= LIVE XAMPP BOOK CATALOG =================\n";
                runXAMPPQuery("SELECT ISBN, TITLE, AUTHOR_NAME, TOTAL_COPIES FROM BOOK;");
                cout << globalDataResult;
                cout << "===========================================================\n\n";
                break;
            }
            case 6: {
                string searchTitle;
                cout << "\n--- Dynamic Search Dashboard ---\n";
                cout << "Enter exact book title to search for: ";
                cin.ignore(); 
                getline(cin, searchTitle); 
                
                cout << "\n--- SEARCH RESULTS FOR: \"" << searchTitle << "\" ---\n";
                runXAMPPQuery("SELECT ISBN, TITLE, AUTHOR_NAME, TOTAL_COPIES FROM BOOK WHERE TITLE = '" + searchTitle + "';");
                
                if (globalDataResult.empty() || globalDataResult == "\n") {
                    cout << "No matching records found for that title.\n";
                } else {
                    cout << globalDataResult;
                }
                cout << "--------------------------------------------\n\n";
                break;
            }
            case 0:
                cout << "Exiting Program...\n"; break;
            default:
                cout << "Invalid Choice!\n";
        }
    } while (choice != 0);

    return 0;
}