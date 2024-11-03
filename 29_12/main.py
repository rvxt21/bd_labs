"""
T29.12 Скласти програму з графічним інтерфейсом для розв’язання задачі.

Дано базу даних, яка містить відомості про книги. Відомості про кожну
книгу - це прізвище автора, назва та рік видання. Підібрати усі книги за
заданою назвою та/або автором та/або періодом видання.
Вводити відомості про книги треба у окремому вікні. У іншому вікні вводити
обмеження та показувати відібрані книги.
Структуру бази даних визначити самостійно.
"""


import tkinter as tk
from tkinter import ttk, messagebox
from database_manager import DatabaseManager
from book import Book

class BookApp:
    def __init__(self, root):
        self.db = DatabaseManager()
        self.root = root
        self.root.title("Book Database")

        self.frame_main = tk.Frame(root)
        self.frame_main.pack(pady=10)

        self.tree = ttk.Treeview(self.frame_main, columns=("title", "author", "year"), show="headings")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("year", text="Year")
        self.tree.pack()

        self.button_add = tk.Button(root, text="Add New Book", command=self.open_add_book_window)
        self.button_add.pack(pady=5)

        self.button_search = tk.Button(root, text="Search Books", command=self.open_search_window)
        self.button_search.pack(pady=5)
        self.load_books()

    def load_books(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        books = self.db.find_books()  
        for book in books:
            self.tree.insert("", "end", values=book)

    def open_add_book_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Book")

        tk.Label(add_window, text="Author:").grid(row=0, column=0)
        entry_author = tk.Entry(add_window)
        entry_author.grid(row=0, column=1)

        tk.Label(add_window, text="Title:").grid(row=1, column=0)
        entry_title = tk.Entry(add_window)
        entry_title.grid(row=1, column=1)

        tk.Label(add_window, text="Year:").grid(row=2, column=0)
        entry_year = tk.Entry(add_window)
        entry_year.grid(row=2, column=1)

        def add_book():
            author = entry_author.get()
            title = entry_title.get()
            year = entry_year.get()

            if not author or not title or not year.isdigit():
                messagebox.showerror("Error", "Please fill in all fields with valid data.")
                return

            book = Book(author, title, int(year))
            self.db.add_book(book.author, book.title, book.year)
            messagebox.showinfo("Success", "Book added successfully!")
            self.load_books()  
            add_window.destroy()

        tk.Button(add_window, text="Add Book", command=add_book).grid(row=3, columnspan=2, pady=10)

    def open_search_window(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Books")

        tk.Label(search_window, text="Author:").grid(row=0, column=0)
        entry_author = tk.Entry(search_window)
        entry_author.grid(row=0, column=1)

        tk.Label(search_window, text="Title:").grid(row=1, column=0)
        entry_title = tk.Entry(search_window)
        entry_title.grid(row=1, column=1)

        tk.Label(search_window, text="Start Year:").grid(row=2, column=0)
        entry_start_year = tk.Entry(search_window)
        entry_start_year.grid(row=2, column=1)

        tk.Label(search_window, text="End Year:").grid(row=3, column=0)
        entry_end_year = tk.Entry(search_window)
        entry_end_year.grid(row=3, column=1)

        results_listbox = tk.Listbox(search_window, width=50, height=10)
        results_listbox.grid(row=5, columnspan=2, pady=10)

        def search_books():
            author = entry_author.get()
            title = entry_title.get()
            start_year = entry_start_year.get()
            end_year = entry_end_year.get()

            start_year = int(start_year) if start_year.isdigit() else None
            end_year = int(end_year) if end_year.isdigit() else None

            results = self.db.find_books(author, title, start_year, end_year)
            results_listbox.delete(0, tk.END)
            for book in results:
                results_listbox.insert(tk.END, f"{book[0]} - {book[1]} ({book[2]})")

        tk.Button(search_window, text="Search", command=search_books).grid(row=4, columnspan=2, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookApp(root)
    root.mainloop()
