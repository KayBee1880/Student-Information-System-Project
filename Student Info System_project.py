import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os
import logging
import re
import traceback

# Configure logging
logging.basicConfig(
    filename='student_system.log', 
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_error(error_message, exception=None):
    """
    Log errors with optional exception details
    """
    if exception:
        logging.error(f"{error_message}\n{traceback.format_exc()}")
    else:
        logging.error(error_message)

def validate_student_id(student_id):
    """
    Validate student ID format
    - Must be a non-empty string
    - Can be alphanumeric
    - Minimum and maximum length constraints
    """
    if not student_id:
        return False, "Student ID cannot be empty"
    
    if len(student_id) < 5 or len(student_id) > 10:
        return False, "Student ID must be between 5 and 10 characters"
    
    if not student_id.isalnum():
        return False, "Student ID must be alphanumeric"
    
    return True, None

def validate_name(first_name, last_name):
    """
    Validate student names
    - Must contain only alphabetic characters and spaces
    - Minimum length
    - No numbers or special characters
    """
    if not first_name or not last_name:
        return False, "First and last names are required"
    
    if len(first_name) < 2 or len(last_name) < 2:
        return False, "Names must be at least 2 characters long"
    
    if not (first_name.replace(' ', '').isalpha() and 
            last_name.replace(' ', '').isalpha()):
        return False, "Names can only contain letters and spaces"
    
    return True, None

def validate_password(password):
    """
    Check password strength
    - Minimum length
    - Contains uppercase, lowercase, number, special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, None

class Student:
    total_students = 0

    def __init__(self, student_id, name, age, grade):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        Student.total_students += 1

    def display_info(self):
        return f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}, Grade: {self.grade}"

class ComputerScienceStudent(Student):
    major = "Computer Science"
    cs_students = 0

    def __init__(self, student_id, name, age, grade):
        super().__init__(student_id, name, age, grade)
        ComputerScienceStudent.cs_students += 1

    def coding_skill(self):
        return f"{self.name} is skilled in Python programming."

class BusinessStudent(Student):
    major = "Business"
    bus_students = 0

    def __init__(self, student_id, name, age, grade):
        super().__init__(student_id, name, age, grade)
        BusinessStudent.bus_students += 1

    def business_deals(self):
        return f"{self.name} excels in negotiations."

class ArtStudent(Student):
    major = "Arts"
    arts_students = 0

    def __init__(self, student_id, name, age, grade):
        super().__init__(student_id, name, age, grade)
        ArtStudent.arts_students += 1

    def creativity(self):
        return f"{self.name} is great at creativity."

class EngineeringStudent(Student):
    major = "Engineering"
    eng_students = 0

    def __init__(self, student_id, name, age, grade):
        super().__init__(student_id, name, age, grade)
        EngineeringStudent.eng_students += 1

    def specialization(self):
        return f"{self.name} has excellent thinking ability."

class LoginSystem:
    def __init__(self, master):
        self.master = master
        master.title("Student Information System")
        master.geometry("400x300")
        master.configure(bg='#F0F4F8')  # Light blue-gray background
        
       
        # Ensure data directory exists
        if not os.path.exists('data'):
            os.mkdir('data')
        
        self.users_file = 'data/users.txt'
        self.students_file = 'data/students.txt'
        
        # Load users and students from text files
        self.users = self.load_users()
        self.students = self.load_students()
        
        # Login attempt tracking
        self.login_attempts = 0
        self.max_attempts = 5
        
        # Students storage lists
        self.cs_students = []
        self.bus_students = []
        self.arts_students = []
        self.eng_students = []
        self.all_students = [self.cs_students, self.bus_students, self.arts_students, self.eng_students]
        
        # Set a default font for the entire application
        default_font = ("Segoe UI", 10)
        master.option_add("*Font", default_font)

        self.create_login_screen()
    
    def load_users(self):
        """Load existing user credentials from text file"""
        users = {}
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as file:
                    for line in file:
                        username, password = line.strip().split(':', 1)
                        users[username] = password
        except Exception as e:
            print(f"Error loading users: {e}")
        return users
    
    def save_users(self):
        """Save user credentials to text file"""
        try:
            with open(self.users_file, 'w') as file:
                for username, password in self.users.items():
                    file.write(f"{username}:{password}\n")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save users: {e}")
    
    def load_students(self):
        """Load existing student data from text file"""
        students = {}
        try:
            if os.path.exists(self.students_file):
                with open(self.students_file, 'r') as file:
                    for line in file:
                        # Parsing student data from text line
                        parts = line.strip().split('|')
                        if len(parts) >= 6:
                            student_id, name, age, classification, major, grade = parts
                            students[student_id] = {
                                'id': student_id,
                                'name': name,
                                'age': age,
                                'classification': classification,
                                'major': major,
                                'grade': grade
                            }
        except Exception as e:
            print(f"Error loading students: {e}")
        return students
    
    def save_students(self):
        """Save student data to text file"""
        try:
            with open(self.students_file, 'w') as file:
                for student_id, student_data in self.students.items():
                    # Create a text line with all student details
                    line = f"{student_data['id']}|{student_data['name']}|{student_data['age']}|{student_data['classification']}|{student_data['major']}|{student_data.get('grade', 'N/A')}\n"
                    file.write(line)
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save students: {e}")

    # The rest of the methods remain the same as in the previous implementation
    # (login, create_login_screen, create_dashboard_screen, add_student, 
    #  search_student_info, remove_student, display_student_count, 
    #  logout, create_new_user)

    # Note: The code for these methods remains unchanged from the previous 
    # implementation, so I'm not repeating them here.

    def create_login_screen(self):
        """Create the login screen with improved colors"""
        # Clear any existing widgets
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Main frame with background color
        main_frame = tk.Frame(self.master, bg='#F0F4F8')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Student Information System", 
                 font=("Segoe UI", 16, "bold"), 
                 fg='#2C3E50',  # Dark slate gray
                 bg='#F0F4F8')  # Match main background
        title_label.pack(pady=(20,20))
        
        # Username Label and Entry
        username_frame = tk.Frame(main_frame, bg='#F0F4F8')
        username_frame.pack()
        
        username_label = tk.Label(username_frame, text="Username:", 
                                  font=("Segoe UI", 12), 
                                  fg='#34495E',  # Dark blue-gray
                                  bg='#F0F4F8')
        username_label.pack()
        
        self.username_entry = tk.Entry(username_frame, 
                                       font=("Segoe UI", 12), 
                                       width=30,
                                       bg='#FFFFFF',  # White background
                                       highlightthickness=1, 
                                       highlightcolor='#3498DB',  # Blue highlight
                                       relief=tk.FLAT)
        self.username_entry.pack(pady=(0,10))
        
        # Password Label and Entry
        password_frame = tk.Frame(main_frame, bg='#F0F4F8')
        password_frame.pack()
        
        password_label = tk.Label(password_frame, text="Password:", 
                                  font=("Segoe UI", 12), 
                                  fg='#34495E',  # Dark blue-gray
                                  bg='#F0F4F8')
        password_label.pack()
        
        self.password_entry = tk.Entry(password_frame, show="*", 
                                       font=("Segoe UI", 12), 
                                       width=30,
                                       bg='#FFFFFF',  # White background
                                       highlightthickness=1, 
                                       highlightcolor='#3498DB',  # Blue highlight
                                       relief=tk.FLAT)
        self.password_entry.pack(pady=(0,20))
        
        # Button Frame
        button_frame = tk.Frame(main_frame, bg='#F0F4F8')
        button_frame.pack(pady=(0,20))
        
        # Login Button
        login_button = tk.Button(button_frame, text="Login", 
                                 command=self.login, 
                                 font=("Segoe UI", 12, "bold"), 
                                 width=15,
                                 bg='#3498DB',  # Bright blue
                                 fg='white',
                                 activebackground='#2980B9',
                                 relief=tk.FLAT)
        login_button.pack(side=tk.LEFT, padx=10)
        
        # Sign Up Button
        signup_button = tk.Button(button_frame, text="Sign Up", 
                                  command=self.create_new_user, 
                                  font=("Segoe UI", 12, "bold"), 
                                  width=15,
                                  bg='#2ECC71',  # Bright green
                                  fg='white',
                                  activebackground='#27AE60',
                                  relief=tk.FLAT)
        signup_button.pack(side=tk.LEFT, padx=10)
        
        # Bind Enter key to login
        self.master.bind('<Return>', lambda event: self.login())

    
    def login(self):
        """Validate login credentials"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if username is empty
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        # Check if password is empty
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
        
        if username in self.users and self.users[username] == password:
            # Successful login
            self.create_dashboard_screen(username)
            return
        
        # Increment login attempts
        self.login_attempts += 1

        # Clear input fields
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        
        # Check if max attempts reached
        if self.login_attempts >= self.max_attempts:
            # Ask if user wants to sign up
            response = messagebox.askyesno(
                "Maximum Login Attempts Reached", 
                "You've reached the maximum number of login attempts. Would you like to sign up?"
            )
            
            if response:
                # Open sign up dialog
                self.create_new_user()
            
            # Reset login attempts
            self.login_attempts = 0
            return
        
        # Show login failure message
        messagebox.showerror(
            "Login Failed", 
            f"Invalid username or password. Attempt {self.login_attempts} of {self.max_attempts}"
        )
    
    def create_dashboard_screen(self, username):
        """Create the dashboard screen with colorful buttons"""
        # Clear existing widgets
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Resize window for dashboard
        self.master.geometry("400x450")
        self.master.configure(bg='#F0F4F8')
        
        # Title
        title_label = tk.Label(self.master, text=f"Welcome, {username}\n\nMAIN MENU", 
                 font=("Segoe UI", 16, "bold"),
                 fg='#2C3E50',
                 bg='#F0F4F8')
        title_label.pack(pady=(20,30))
        
        # Button Frame
        button_frame = tk.Frame(self.master, bg='#F0F4F8')
        button_frame.pack(pady=(0,20))
        
        # Button configurations
        button_configs = [
            ("Print Student Information", self.search_student_info, '#3498DB'),  # Blue
            ("Add Student", self.add_student, '#2ECC71'),  # Green
            ("Remove Student", self.remove_student, '#E74C3C'),  # Red
            ("Display Number of Students", self.display_student_count, '#F39C12'),  # Orange
            ("Logout", self.logout, '#95A5A6')  # Gray
        ]
        
        # Create buttons
        for text, command, color in button_configs:
            btn = tk.Button(button_frame, text=text, 
                            command=command, 
                            font=("Segoe UI", 12), 
                            width=25,
                            bg=color,
                            fg='white',
                            activebackground=self._darken_color(color),
                            relief=tk.FLAT)
            btn.pack(pady=(0,10))

    def _darken_color(self, hex_color):
        """Helper method to darken a hex color"""
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Darken by reducing each color component
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        
        # Convert back to hex
        return '#{:02x}{:02x}{:02x}'.format(*darkened)


        
    def remove_student(self):
        """Remove a student from the system"""
        # If no students exist
        if not self.students:
            messagebox.showinfo("Remove Student", "No students have been added yet.")
            return

        # Create remove student window
        remove_window = tk.Toplevel(self.master)
        remove_window.title("Remove Student")
        remove_window.geometry("400x300")

        # Full Name Input
        tk.Label(remove_window, text="Student Full Name:", font=("Helvetica", 12)).pack(pady=(20, 0))
        full_name_entry = tk.Entry(remove_window, font=("Helvetica", 12), width=30)
        full_name_entry.pack(pady=(0, 10))

        # Student ID Input
        tk.Label(remove_window, text="Student ID:", font=("Helvetica", 12)).pack(pady=(10, 0))
        student_id_entry = tk.Entry(remove_window, font=("Helvetica", 12), width=30)
        student_id_entry.pack(pady=(0, 20))

        def confirm_remove():
            full_name = full_name_entry.get().strip()
            student_id = student_id_entry.get().strip()

            # Check if student ID and name match
            if student_id in self.students and self.students[student_id]['name'] == full_name:
                # Confirm removal
                confirm = messagebox.askyesno("Confirm Removal",
                                              f"Are you sure you want to remove {full_name} (ID: {student_id})?")
                if confirm:
                    # Remove student
                    del self.students[student_id]
                    # Save updated students
                    self.save_students()
                    messagebox.showinfo("Success", f"Student {full_name} (ID: {student_id}) has been removed.")
                    remove_window.destroy()
            else:
                messagebox.showerror("Error", "No student found with the given name and ID.")

        # Remove Button
        remove_button = tk.Button(remove_window, text="Remove",
                                  command=confirm_remove,
                                  font=("Helvetica", 12))
        remove_button.pack(pady=(0, 10))


    def display_student_count(self):
        """Display the total number of students and students by major"""
        # If no students exist
        if not self.students:
            messagebox.showinfo("Student Count", "No students have been added yet.")
            return
        
        
        # Count students by major
        major_counts = {
            "Computer Science": 0,
            "Business": 0,
            "Arts": 0,
            "Engineering": 0
        }
        
        # Count students in each major
        for student in self.students.values():
            major = student.get('major', 'Unknown')
            if major in major_counts:
                major_counts[major] += 1

        # Use len(self.students) instead of any class variables
        total_students = sum(major_counts.values())
        
        # Create student count window
        count_window = tk.Toplevel(self.master)
        count_window.title("Student Count")
        count_window.geometry("300x300")
        
        # Create frame for counts
        count_frame = tk.Frame(count_window)
        count_frame.pack(padx=20, pady=20)
        
        # Total Students Label
        tk.Label(count_frame, text=f"Total Students: {total_students}", 
                 font=("Helvetica", 14, "bold")).pack(anchor='w', pady=(0,10))
        
        # Major-specific counts
        for major, count in major_counts.items():
            tk.Label(count_frame, text=f"{major} Students: {count}", 
                     font=("Helvetica", 12)).pack(anchor='w', pady=(0,5))
    def logout(self):
        """Logout and return to login screen"""
        # Confirm logout
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
                
        if confirm:
            # Reset login attempts
            self.login_attempts = 0
                    
            # Recreate login screen
            self.create_login_screen()
            
    
    def search_student_info(self):
        """Search for student by name and display results"""
        # If no students exist
        if not self.students:
            messagebox.showinfo("Student Information", "No students have been added yet.")
            return
        
        # Create search window
        search_window = tk.Toplevel(self.master)
        search_window.title("Search Student")
        search_window.geometry("400x200")
        
        # First Name Input
        tk.Label(search_window, text="First Name:", font=("Helvetica", 12)).pack(pady=(20,0))
        first_name_entry = tk.Entry(search_window, font=("Helvetica", 12), width=30)
        first_name_entry.pack(pady=(0,10))
        
        # Last Name Input
        tk.Label(search_window, text="Last Name:", font=("Helvetica", 12)).pack()
        last_name_entry = tk.Entry(search_window, font=("Helvetica", 12), width=30)
        last_name_entry.pack(pady=(0,20))
        
        def search_students():
            """Search for students based on entered name"""
            first_name = first_name_entry.get().strip().lower()
            last_name = last_name_entry.get().strip().lower()
            
            # Find matching students
            matches = []
            for student_id, student_data in self.students.items():
                full_name = student_data.get('name', '').lower()
                
                # Check if both first and last names match
                if first_name and last_name:
                    if first_name in full_name and last_name in full_name:
                        matches.append((student_id, student_data))
                # Check if either first or last name matches
                elif first_name:
                    if first_name in full_name:
                        matches.append((student_id, student_data))
                elif last_name:
                    if last_name in full_name:
                        matches.append((student_id, student_data))
            
            # If no matches found
            if not matches:
                messagebox.showinfo("Search Results", "Student not found.")
                return
            
            # If only one match, show details directly
            if len(matches) == 1:
                student_id, student_data = matches[0]
                show_student_details(student_id, student_data)
                return
            
            # Multiple matches - create selection dialog
            select_student_window = tk.Toplevel(search_window)
            select_student_window.title("Select Student")
            select_student_window.geometry("400x300")
            
            # Label
            tk.Label(select_student_window, 
                     text="Multiple Students Found. Please Select:", 
                     font=("Helvetica", 12, "bold")).pack(pady=(10,10))
            
            # Listbox to display matching students
            student_listbox = tk.Listbox(select_student_window, 
                                         font=("Helvetica", 12), 
                                         width=50)
            student_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
            # Populate listbox
            for student_id, student_data in matches:
                student_listbox.insert(tk.END, 
                    f"ID: {student_id} - Name: {student_data.get('name', 'N/A')}")
            
            def on_select():
                """Handle student selection"""
                # Get selected index
                selected_indices = student_listbox.curselection()
                
                # Check if a student is selected
                if not selected_indices:
                    messagebox.showwarning("Selection", "Please select a student.")
                    return
                
                # Get selected student
                selected_index = selected_indices[0]
                selected_student_id, selected_student_data = matches[selected_index]
                
                # Close selection window and show details
                select_student_window.destroy()
                show_student_details(selected_student_id, selected_student_data)
            
            # Select Button
            select_button = tk.Button(select_student_window, 
                                      text="View Details", 
                                      command=on_select, 
                                      font=("Helvetica", 12))
            select_button.pack(pady=(10,10))
        
        def show_student_details(student_id, student_data):
            """Display detailed information for a student"""
            details_window = tk.Toplevel(self.master)
            details_window.title(f"Student Details - {student_id}")
            details_window.geometry("300x350")
            
            # Details frame
            details_frame = tk.Frame(details_window)
            details_frame.pack(padx=20, pady=20)
            
            details = [
                ("Student ID", student_id),
                ("Name", student_data.get('name', 'N/A')),
                ("Age", student_data.get('age', 'N/A')),
                ("Classification", student_data.get('classification', 'N/A'))
            ]
            
            for label, value in details:
                tk.Label(details_frame, text=f"{label}:", 
                         font=("Helvetica", 12, "bold")).pack(anchor='w')
                tk.Label(details_frame, text=value, 
                         font=("Helvetica", 12)).pack(anchor='w', pady=(0,10))
        
        # Search Button
        search_button = tk.Button(search_window, text="Search", 
                                  command=search_students, 
                                  font=("Helvetica", 12))
        search_button.pack(pady=(0,10))

    def add_student(self):
        """Open dialog to add a new student"""
        # Create add student window
        add_student_window = tk.Toplevel(self.master)
        add_student_window.title("Add Student")
        add_student_window.geometry("400x550")  # Slightly increased height
        add_student_window.configure(bg='#F0F4F8')
        
        # Student ID
        tk.Label(add_student_window, text="Student ID:", font=("Helvetica", 12)).pack()
        student_id_entry = tk.Entry(add_student_window, font=("Helvetica", 12), width=30)
        student_id_entry.pack(pady=(0,10))
        
        # First Name
        tk.Label(add_student_window, text="First Name:", font=("Helvetica", 12)).pack()
        first_name_entry = tk.Entry(add_student_window, font=("Helvetica", 12), width=30)
        first_name_entry.pack(pady=(0,10))
        
        # Last Name
        tk.Label(add_student_window, text="Last Name:", font=("Helvetica", 12)).pack()
        last_name_entry = tk.Entry(add_student_window, font=("Helvetica", 12), width=30)
        last_name_entry.pack(pady=(0,10))
        
        # Age
        tk.Label(add_student_window, text="Age:", font=("Helvetica", 12)).pack()
        age_entry = tk.Entry(add_student_window, font=("Helvetica", 12), width=30)
        age_entry.pack(pady=(0,10))
        
        # Classification Selection
        tk.Label(add_student_window, text="Select Classification:", font=("Helvetica", 12)).pack()
        classification_var = tk.StringVar()
        classification_dropdown = ttk.Combobox(add_student_window, textvariable=classification_var, 
                                      values=["Freshman", "Sophomore", "Junior", "Senior"], 
                                      width=27, state="readonly")
        classification_dropdown.pack(pady=(0,10))

        # Major Selection
        tk.Label(add_student_window, text="Select Major:", font=("Helvetica", 12)).pack()
        major_var = tk.StringVar()
        major_dropdown = ttk.Combobox(add_student_window, textvariable=major_var, 
                                      values=["Computer Science", "Business", "Arts", "Engineering"], 
                                      width=27, state="readonly")
        major_dropdown.pack(pady=(0, 20))

        def save_student():
            """Save the new student to the system"""
            student_id = student_id_entry.get().strip()
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            age = age_entry.get().strip()
            classification = classification_var.get()
            major = major_var.get()

            # Enhanced Validation
            if not student_id:
                messagebox.showerror("Error", "Student ID is required")
                return
            
            if not first_name or not last_name:
                messagebox.showerror("Error", "First and Last name are required")
                return

            try:
                age = int(age)
                if age < 5 or age > 100:
                    raise ValueError("Invalid age")
            except ValueError:
                messagebox.showerror("Error", "Age must be a valid number between 5 and 100")
                return

            if not classification:
                messagebox.showerror("Error", "Please select a classification")
                return

            if not major:
                messagebox.showerror("Error", "Please select a major")
                return

            # Check if student ID already exists
            if student_id in self.students:
                messagebox.showerror("Error", "Student ID already exists")
                return

            # Create student based on major
            full_name = f"{first_name} {last_name}"
            student_data = {
                'id': student_id,
                'name': full_name,
                'age': age,
                'classification': classification,  # Added classification
                'major': major
            }

            # Save student to dictionary
            try:
                self.students[student_id] = student_data
                self.save_students()

                # Dynamically create student objects based on major
                if major == "Computer Science":
                    student = ComputerScienceStudent(student_id, full_name, age, classification)
                elif major == "Business":
                    student = BusinessStudent(student_id, full_name, age, classification)
                elif major == "Arts":
                    student = ArtStudent(student_id, full_name, age, classification)
                elif major == "Engineering":
                    student = EngineeringStudent(student_id, full_name, age, classification)

                # Reset entry fields
                student_id_entry.delete(0, tk.END)
                first_name_entry.delete(0, tk.END)
                last_name_entry.delete(0, tk.END)
                age_entry.delete(0, tk.END)
                classification_dropdown.set('')
                major_dropdown.set('')

                messagebox.showinfo("Success", f"Student {full_name} added successfully!")

            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save student: {str(e)}")

        # Save Button
        save_button = tk.Button(add_student_window, text="Save Student", 
                                command=save_student, 
                                font=("Helvetica", 12), 
                                width=25)
        save_button.pack(pady=(0, 20))
    
    def create_new_user(self):
        """Create a new user with validation"""
        # Open signup dialog
        signup_window = tk.Toplevel(self.master)
        signup_window.title("Sign Up")
        signup_window.geometry("400x300")
        signup_window.configure(bg='#F0F4F8')
        
        # Username Label and Entry
        tk.Label(signup_window, text="Choose Username:", font=("Helvetica", 12), bg='#F0F4F8').pack(pady=(20,0))
        username_entry = tk.Entry(signup_window, font=("Helvetica", 12), width=30)
        username_entry.pack(pady=(0,10))
        
        # Password Label and Entry
        tk.Label(signup_window, text="Choose Password:", font=("Helvetica", 12), bg='#F0F4F8').pack()
        password_entry = tk.Entry(signup_window, show="*", font=("Helvetica", 12), width=30)
        password_entry.pack(pady=(0,10))
        
        # Confirm Password Label and Entry
        tk.Label(signup_window, text="Confirm Password:", font=("Helvetica", 12), bg='#F0F4F8').pack()
        confirm_password_entry = tk.Entry(signup_window, show="*", font=("Helvetica", 12), width=30)
        confirm_password_entry.pack(pady=(0,20))
        
        def submit_signup():
            """Handle user signup submission"""
            new_username = username_entry.get().strip()
            new_password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            
            # Validation checks
            if not new_username:
                messagebox.showerror("Error", "Username cannot be empty")
                return
            
            if new_username in self.users:
                messagebox.showerror("Error", "Username already exists!")
                return
            
            if not new_password:
                messagebox.showerror("Error", "Password cannot be empty")
                return
            
            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            # Save new user
            self.users[new_username] = new_password
            self.save_users()
            
            messagebox.showinfo("Success", "User created successfully!")
            signup_window.destroy()
            
            # Reset login attempts
            self.login_attempts = 0
        
        # Submit Button
        submit_button = tk.Button(signup_window, text="Submit", 
                                  command=submit_signup, 
                                  font=("Helvetica", 12), 
                                  width=15,
                                  bg='#3498DB',  # Bright blue
                                 fg='black',
                                 activebackground='#2980B9',
                                 relief=tk.FLAT)
        submit_button.pack(pady=(20,0))



def main():
    root = tk.Tk()
    LoginSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
