# Library Management System using Python
# Data Structures: Stack (for recent actions), Queue (for waitlists using Linked List), BST (for book search by serial), Hash Table (for title and author lookups)
# If needed, Linked List is used in Queue implementation

class LinkedNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, data):
        node = LinkedNode(data)
        if self.rear is None:
            self.front = self.rear = node
            return
        self.rear.next = node
        self.rear = node

    def dequeue(self):
        if self.front is None:
            return None
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        return temp.data

    def is_empty(self):
        return self.front is None

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def is_empty(self):
        return len(self.items) == 0

    def get_all(self):
        return self.items[::-1]  # Recent first

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if key < node.key:
            if node.left is None:
                node.left = Node(key, value)
            else:
                self._insert(node.left, key, value)
        elif key > node.key:
            if node.right is None:
                node.right = Node(key, value)
            else:
                self._insert(node.right, key, value)
        else:
            node.value = value  # Update if exists

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None or node.key == key:
            return node.value if node else None
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[index].append([key, value])

    def get(self, key):
        index = self.hash_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None

class Book:
    def __init__(self, serial, title, author):
        self.serial = serial
        self.title = title
        self.author = author
        self.available = True
        self.wait_queue = Queue()  # Queue for waitlist (duration management via waitlist)

class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.borrowed = []  # List of borrowed books

class Library:
    def __init__(self):
        self.books_bst = BST()  # BST for books by serial number (quick search)
        self.title_hash = HashTable()  # Hash table for book by title
        self.author_hash = HashTable()  # Hash table for books by author (value is list)
        self.students = {}  # Dictionary for students by ID
        self.action_stack = Stack()  # Stack for general entries/recent actions

    def register_student(self, id, name):
        if id in self.students:
            print("Student already registered.")
            return
        student = Student(id, name)
        self.students[id] = student
        self.action_stack.push(f"Registered student {name} with ID {id}")
        print("Student registered successfully.")

    def add_book(self, serial, title, author):
        if self.books_bst.search(serial):
            print("Book with this serial number already exists.")
            return
        book = Book(serial, title, author)
        self.books_bst.insert(serial, book)
        self.title_hash.insert(title, book)
        author_books = self.author_hash.get(author)
        if author_books is None:
            author_books = []
            self.author_hash.insert(author, author_books)
        author_books.append(book)
        self.action_stack.push(f"Added book '{title}' by {author} with serial {serial}")
        print("Book added successfully.")

    def borrow_book(self, student_id, serial):
        if student_id not in self.students:
            print("Student not registered.")
            return
        student = self.students[student_id]
        book = self.books_bst.search(serial)
        if book is None:
            print("Book not found.")
            return
        if book.available:
            book.available = False
            student.borrowed.append(book)
            self.action_stack.push(f"Student {student.name} borrowed '{book.title}' (serial {serial})")
            print("Book borrowed successfully.")
        else:
            book.wait_queue.enqueue(student)
            self.action_stack.push(f"Student {student.name} added to waitlist for '{book.title}' (serial {serial})")
            print("Book not available. Added to waitlist.")

    def return_book(self, student_id, serial):
        if student_id not in self.students:
            print("Student not registered.")
            return
        student = self.students[student_id]
        book = self.books_bst.search(serial)
        if book is None:
            print("Book not found.")
            return
        if book in student.borrowed:
            book.available = True
            student.borrowed.remove(book)
            self.action_stack.push(f"Student {student.name} returned '{book.title}' (serial {serial})")
            print("Book returned successfully.")
            if not book.wait_queue.is_empty():
                next_student = book.wait_queue.dequeue()
                book.available = False
                next_student.borrowed.append(book)
                self.action_stack.push(f"Auto-borrowed '{book.title}' (serial {serial}) to {next_student.name}")
                print(f"Book auto-borrowed to {next_student.name} from waitlist.")
        else:
            print("This student did not borrow this book.")

    def search_book_by_serial(self, serial):
        book = self.books_bst.search(serial)
        if book:
            availability = "available" if book.available else "not available"
            print(f"Book '{book.title}' by {book.author} (serial {serial}) is {availability}.")
        else:
            print("Book not found.")

    def search_book_by_title(self, title):
        book = self.title_hash.get(title)
        if book:
            availability = "available" if book.available else "not available"
            print(f"Book '{book.title}' by {book.author} (serial {book.serial}) is {availability}.")
        else:
            print("Book not found.")

    def search_books_by_author(self, author):
        books = self.author_hash.get(author)
        if books:
            print(f"Books by {author}:")
            for book in books:
                availability = "available" if book.available else "not available"
                print(f"- '{book.title}' (serial {book.serial}) is {availability}.")
        else:
            print("No books found for this author.")

    def get_sorted_books(self, by='title'):
        books = self._inorder_books()
        if by == 'title':
            books.sort(key=lambda b: b.title)
        
        print("Sorted books:")
        for book in books:
            availability = "available" if book.available else "not available"
            print(f"- '{book.title}' by {book.author} (serial {book.serial}) is {availability}.")

    def _inorder_books(self):
        def inorder(node, lst):
            if node:
                inorder(node.left, lst)
                lst.append(node.value)
                inorder(node.right, lst)
        lst = []
        inorder(self.books_bst.root, lst)
        return lst

    def show_recent_actions(self):
        actions = self.action_stack.get_all()
        if actions:
            print("Recent actions (latest first):")
            for action in actions:
                print(f"- {action}")
        else:
            print("No recent actions.")

def main():
    library = Library()
    while True:
        print("\nLibrary Management System Menu:")
        print("1. Register Student")
        print("2. Add Book")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Search Book by Serial (using BST)")
        print("6. Search Book by Title (using Hash Table)")
        print("7. Search Books by Author (using Hash Table)")
        print("8. List Sorted Books (by title)")
        print("9. Show Recent Actions (using Stack)")
        print("0. Exit")
        choice = input("Enter your choice: ")
        if choice == '0':
            break
        elif choice == '1':
            try:
                student_id = int(input("Enter Student ID: "))
                name = input("Enter Student Name: ")
                library.register_student(student_id, name)
            except ValueError:
                print("Invalid input.")
        elif choice == '2':
            try:
                serial = int(input("Enter Book Serial Number: "))
                title = input("Enter Book Title: ")
                author = input("Enter Book Author: ")
                library.add_book(serial, title, author)
            except ValueError:
                print("Invalid input.")
        elif choice == '3':
            try:
                student_id = int(input("Enter Student ID: "))
                serial = int(input("Enter Book Serial Number: "))
                library.borrow_book(student_id, serial)
            except ValueError:
                print("Invalid input.")
        elif choice == '4':
            try:
                student_id = int(input("Enter Student ID: "))
                serial = int(input("Enter Book Serial Number: "))
                library.return_book(student_id, serial)
            except ValueError:
                print("Invalid input.")
        elif choice == '5':
            try:
                serial = int(input("Enter Book Serial Number: "))
                library.search_book_by_serial(serial)
            except ValueError:
                print("Invalid input.")
        elif choice == '6':
            title = input("Enter Book Title: ")
            library.search_book_by_title(title)
        elif choice == '7':
            author = input("Enter Author Name: ")
            library.search_books_by_author(author)
        elif choice == '8':
            library.get_sorted_books()
        elif choice == '9':
            library.show_recent_actions()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
