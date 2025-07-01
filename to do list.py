import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import json
import os
from PIL import Image
from tkcalendar import Calendar # Import the Calendar widget

# --- TaskDialog for a professional Add/Edit experience ---
class TaskDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Add Task", task_data=None, icons=None):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)
        self.geometry("400x520") # Increased height to ensure buttons are visible
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        
        self.result = None
        self.icons = icons
        self.categories = parent.categories[1:] # Exclude "All"

        self.configure(fg_color=parent.colors['bg_secondary'])

        ctk.CTkLabel(self, text=title, font=("Inter", 20, "bold")).pack(pady=(20, 10))

        # Task Text
        ctk.CTkLabel(self, text="Task Description", anchor="w", font=("Inter", 12)).pack(fill="x", padx=30, pady=(10, 5))
        self.entry_task = ctk.CTkEntry(self, placeholder_text="e.g., Buy groceries for the week", height=40, font=("Inter", 14))
        self.entry_task.pack(fill="x", padx=30)

        # Category
        ctk.CTkLabel(self, text="Category", anchor="w", font=("Inter", 12)).pack(fill="x", padx=30, pady=(20, 5))
        self.category_var = ctk.StringVar(value=self.categories[0])
        self.category_combo = ctk.CTkComboBox(self, variable=self.category_var, values=self.categories, height=40, font=("Inter", 14), state="readonly")
        self.category_combo.pack(fill="x", padx=30)

        # Priority
        ctk.CTkLabel(self, text="Priority", anchor="w", font=("Inter", 12)).pack(fill="x", padx=30, pady=(20, 5))
        self.priority_var = ctk.StringVar(value="Medium")
        self.priority_combo = ctk.CTkComboBox(self, variable=self.priority_var, values=["High", "Medium", "Low"], height=40, font=("Inter", 14), state="readonly")
        self.priority_combo.pack(fill="x", padx=30)
        
        # Due Date with Calendar Button
        ctk.CTkLabel(self, text="Due Date", anchor="w", font=("Inter", 12)).pack(fill="x", padx=30, pady=(20, 5))
        
        due_date_frame = ctk.CTkFrame(self, fg_color="transparent")
        due_date_frame.pack(fill="x", padx=30)
        
        self.due_date_var = ctk.StringVar()
        self.due_date_entry = ctk.CTkEntry(due_date_frame, textvariable=self.due_date_var, placeholder_text="YYYY-MM-DD (Optional)", height=40, font=("Inter", 14))
        self.due_date_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        calendar_btn = ctk.CTkButton(due_date_frame, text="", image=self.icons.get('calendar'), width=40, height=40, command=self.open_calendar)
        calendar_btn.pack(side="right")

        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=30)

        ctk.CTkButton(button_frame, text="Cancel", command=self.cancel, height=40, fg_color=parent.colors['bg_tertiary'], text_color=parent.colors['text_primary'], hover_color=parent.colors['border']).pack(side="left", expand=True, padx=(0, 5))
        ctk.CTkButton(button_frame, text="Save Task", command=self.save, height=40, font=("Inter", 14, "bold")).pack(side="right", expand=True, padx=(5, 0))

        if task_data:
            self.populate_data(task_data)
        
        self.entry_task.focus()
        self.grab_set()

    def open_calendar(self):
        cal_win = ctk.CTkToplevel(self)
        cal_win.title("Select Date")
        cal_win.grab_set()
        cal_win.resizable(False, False)
        
        def on_date_select(e):
            selected_date = cal.get_date()
            self.due_date_var.set(selected_date)
            cal_win.destroy()

        cal = Calendar(cal_win, selectmode='day', date_pattern='y-mm-dd',
                       background="#3b82f6", foreground='white',
                       headersbackground="#3b82f6", headersforeground='white',
                       normalbackground='#ffffff', normalforeground='#0f172a',
                       weekendbackground='#f1f5f9', weekendforeground='#0f172a',
                       othermonthforeground='gray', othermonth2foreground='gray',
                       selectbackground='#2563eb', selectforeground='white',
                       font=("Inter", 12), bordercolor="#e2e8f0", borderwidth=1)
        cal.pack(pady=10, padx=10)
        cal.bind("<<CalendarSelected>>", on_date_select)
    
    def populate_data(self, data):
        self.entry_task.insert(0, data['text'])
        self.category_var.set(data['category'])
        self.priority_var.set(data['priority'])
        self.due_date_var.set(data.get('due_date', ''))

    def save(self):
        task_text = self.entry_task.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Task description cannot be empty.", parent=self)
            return
        
        due_date_str = self.due_date_entry.get().strip()
        if due_date_str:
            try:
                datetime.strptime(due_date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.", parent=self)
                return

        self.result = {
            'text': task_text,
            'category': self.category_var.get(),
            'priority': self.priority_var.get(),
            'due_date': due_date_str or None
        }
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()

# --- MAIN APPLICATION ---
class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TodoMaster Pro")
        self.geometry("1100x750")
        self.resizable(True, True)
        self.minsize(900, 600)
        
        self.tasks = []
        self.categories = ["All", "Personal", "Work", "Shopping", "Health", "Education"]
        self.current_category = "All"
        self.data_file = "todo_data.json"
        
        self.setup_styles_and_theme()
        
        self.load_icons()
        self.create_widgets()
        self.load_data()
        self.apply_colors()

    def setup_styles_and_theme(self):
        ctk.set_appearance_mode("Light")
        
        self.light_colors = {
            'bg_primary': '#f8fafc', 'bg_secondary': '#ffffff', 'bg_tertiary': '#f1f5f9',
            'accent': '#3b82f6', 'accent_hover': '#2563eb',
            'text_primary': '#0f172a', 'text_secondary': '#64748b',
            'success': '#10b981', 'warning': '#f59e0b', 'danger': '#ef4444', 'border': '#e2e8f0',
        }
        
        self.dark_colors = {
            'bg_primary': '#0f172a', 'bg_secondary': '#1e293b', 'bg_tertiary': '#334155',
            'accent': '#60a5fa', 'accent_hover': '#3b82f6',
            'text_primary': '#f8fafc', 'text_secondary': '#94a3b8',
            'success': '#10b981', 'warning': '#f59e0b', 'danger': '#ef4444', 'border': '#334155',
        }
        
        self.colors = self.light_colors
        self.title_font = ("Inter", 24, "bold")
        self.body_font = ("Inter", 14)
        self.small_font = ("Inter", 10)

    def load_icons(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "icons")
        try:
            self.icons = {
                "logo": ctk.CTkImage(Image.open(os.path.join(icon_path, "logo.png")), size=(28, 28)),
                "All": ctk.CTkImage(Image.open(os.path.join(icon_path, "home.png"))),
                "Personal": ctk.CTkImage(Image.open(os.path.join(icon_path, "user.png"))),
                "Work": ctk.CTkImage(Image.open(os.path.join(icon_path, "briefcase.png"))),
                "Shopping": ctk.CTkImage(Image.open(os.path.join(icon_path, "shopping-cart.png"))),
                "Health": ctk.CTkImage(Image.open(os.path.join(icon_path, "heart-pulse.png"))),
                "Education": ctk.CTkImage(Image.open(os.path.join(icon_path, "book-marked.png"))),
                "add": ctk.CTkImage(Image.open(os.path.join(icon_path, "plus.png"))),
                "edit": ctk.CTkImage(Image.open(os.path.join(icon_path, "edit.png")), size=(16, 16)),
                "delete": ctk.CTkImage(Image.open(os.path.join(icon_path, "delete.png")), size=(16, 16)),
                "calendar": ctk.CTkImage(Image.open(os.path.join(icon_path, "calendar.png"))),
                "no_tasks": ctk.CTkImage(Image.open(os.path.join(icon_path, "no-tasks.png")), size=(200, 200))
            }
        except FileNotFoundError as e:
            messagebox.showerror("Icon Error", f"Could not find an icon file.\nPlease ensure the 'icons' folder exists and is in the same directory as the script.\n\nMissing file: {e.filename}")
            self.quit()

    def create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_propagate(False)
        
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.create_sidebar()
        self.create_main_content()
    
    def create_sidebar(self):
        logo_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        logo_frame.pack(pady=30, padx=20)
        ctk.CTkLabel(logo_frame, image=self.icons['logo'], text="").pack(side="left")
        self.logo_text = ctk.CTkLabel(logo_frame, text="TodoMaster", font=("Inter", 20, "bold"))
        self.logo_text.pack(side="left", padx=10)
        
        self.category_buttons = {}
        for category in self.categories:
            btn = ctk.CTkButton(
                self.sidebar_frame, text=category, command=lambda c=category: self.set_category_filter(c),
                font=("Inter", 15, "bold"), corner_radius=8, height=45,
                image=self.icons.get(category), anchor="w", compound="left"
            )
            btn.pack(fill="x", padx=20, pady=5)
            self.category_buttons[category] = btn
        
        theme_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        theme_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        self.theme_label = ctk.CTkLabel(theme_frame, text="Light Mode", font=("Inter", 12))
        self.theme_label.pack(side="left")
        self.theme_switch = ctk.CTkSwitch(theme_frame, text="", command=self.toggle_theme, width=0)
        self.theme_switch.pack(side="right")
        self.theme_switch.select()

    def create_main_content(self):
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.current_category_label = ctk.CTkLabel(header_frame, text="All Tasks", font=self.title_font)
        self.current_category_label.pack(side="left")
        
        add_task_btn = ctk.CTkButton(
            header_frame, text="Add New Task", command=self.show_add_task_dialog,
            image=self.icons['add'], font=("Inter", 14, "bold"), height=40,
        )
        add_task_btn.pack(side="right")
        
        self.task_list_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        self.task_list_frame.grid(row=1, column=0, sticky="nsew")

    def create_task_widget(self, task):
        task_frame = ctk.CTkFrame(self.task_list_frame, fg_color=self.colors['bg_secondary'], border_width=1, border_color=self.colors['border'])
        task_frame.pack(fill="x", pady=(0, 10), padx=5)

        priority_colors = {'High': self.colors['danger'], 'Medium': self.colors['warning'], 'Low': self.colors['success']}
        ctk.CTkFrame(task_frame, width=5, fg_color=priority_colors[task['priority']], corner_radius=0).pack(side="left", fill="y")
        
        content_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        content_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
        
        top_row = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_row.pack(fill="x")
        
        strike_font = ("Inter", 15, "overstrike") if task['completed'] else ("Inter", 15)
        text_color = self.colors['text_secondary'] if task['completed'] else self.colors['text_primary']
        
        checkbox = ctk.CTkCheckBox(
            top_row, text="", variable=ctk.BooleanVar(value=task['completed']), 
            command=lambda: self.toggle_task(task['id']),
            onvalue=True, offvalue=False
        )
        checkbox.pack(side="left", padx=(0, 10))
        
        task_label = ctk.CTkLabel(top_row, text=task['text'], font=strike_font, text_color=text_color, anchor="w", wraplength=500)
        task_label.pack(side="left", fill="x", expand=True)

        bottom_row = ctk.CTkFrame(content_frame, fg_color="transparent")
        bottom_row.pack(fill="x", pady=(8, 0))

        if task.get('due_date'):
            due_date = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
            days_left = (due_date - datetime.now().date()).days
            
            if days_left < 0:
                due_text, due_color = f"Overdue by {abs(days_left)} days", self.colors['danger']
            elif days_left == 0:
                due_text, due_color = "Due Today", self.colors['warning']
            else:
                due_text, due_color = f"Due in {days_left} days", self.colors['text_secondary']
                
            ctk.CTkLabel(bottom_row, text=due_text, font=self.small_font, text_color=due_color).pack(side="left", padx=(34, 10))

        actions_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        actions_frame.pack(side="right", padx=15)
        
        edit_btn = ctk.CTkButton(actions_frame, text="", image=self.icons['edit'], width=30, height=30, command=lambda t=task: self.show_edit_task_dialog(t))
        edit_btn.pack(pady=(0,5))
        
        delete_btn = ctk.CTkButton(actions_frame, text="", image=self.icons['delete'], width=30, height=30, fg_color=self.colors['danger'], hover_color="#B33A3A", command=lambda t_id=task['id']: self.delete_task(t_id))
        delete_btn.pack()

    def apply_colors(self):
        self.configure(fg_color=self.colors['bg_primary'])
        self.sidebar_frame.configure(fg_color=self.colors['bg_secondary'])
        self.main_frame.configure(fg_color=self.colors['bg_primary'])
        self.task_list_frame.configure(fg_color=self.colors['bg_primary'])
        
        self.logo_text.configure(text_color=self.colors['text_primary'])
        self.current_category_label.configure(text_color=self.colors['text_primary'])
        self.theme_label.configure(text_color=self.colors['text_primary'])
        
        self.update_category_buttons()

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Light")
            self.colors = self.light_colors
            self.theme_label.configure(text="Light Mode")
        else:
            ctk.set_appearance_mode("Dark")
            self.colors = self.dark_colors
            self.theme_label.configure(text="Dark Mode")
        
        self.apply_colors()
        self.refresh_task_display()

    def update_category_buttons(self):
        for category, btn in self.category_buttons.items():
            if category == self.current_category:
                btn.configure(fg_color=self.colors['accent'], text_color=self.colors['bg_secondary'])
            else:
                btn.configure(fg_color="transparent", hover_color=self.colors['bg_tertiary'], text_color=self.colors['text_secondary'])

    def show_add_task_dialog(self):
        dialog = TaskDialog(self, title="Add New Task", icons=self.icons)
        self.wait_window(dialog)
        
        if dialog.result:
            new_task = {
                'id': int(datetime.now().timestamp()),
                'text': dialog.result['text'],
                'completed': False,
                'category': dialog.result['category'],
                'priority': dialog.result['priority'],
                'due_date': dialog.result['due_date'],
                'created_at': datetime.now().isoformat(),
                'completed_at': None
            }
            self.tasks.append(new_task)
            self.refresh_task_display()
            self.save_data()

    def show_edit_task_dialog(self, task):
        dialog = TaskDialog(self, title="Edit Task", task_data=task, icons=self.icons)
        self.wait_window(dialog)
        
        if dialog.result:
            task.update(dialog.result)
            self.refresh_task_display()
            self.save_data()

    def toggle_task(self, task_id):
        task = next((t for t in self.tasks if t['id'] == task_id), None)
        if task:
            task['completed'] = not task['completed']
            task['completed_at'] = datetime.now().isoformat() if task['completed'] else None
            self.refresh_task_display()
            self.save_data()

    def delete_task(self, task_id):
        if messagebox.askyesno("Delete Task", "Are you sure you want to permanently delete this task?"):
            self.tasks = [t for t in self.tasks if t['id'] != task_id]
            self.refresh_task_display()
            self.save_data()

    def set_category_filter(self, category):
        self.current_category = category
        self.current_category_label.configure(text=f"{category} Tasks")
        self.update_category_buttons()
        self.refresh_task_display()

    def get_filtered_tasks(self):
        filtered = self.tasks
        if self.current_category != "All":
            filtered = [t for t in filtered if t['category'] == self.current_category]
        
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        filtered.sort(key=lambda t: (
            t['completed'],
            t['due_date'] or '9999-12-31',
            priority_order[t['priority']]
        ))
        return filtered

    def refresh_task_display(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        filtered_tasks = self.get_filtered_tasks()
        
        if not filtered_tasks:
            empty_frame = ctk.CTkFrame(self.task_list_frame, fg_color="transparent")
            empty_frame.pack(expand=True, fill="both", pady=50)
            ctk.CTkLabel(empty_frame, image=self.icons['no_tasks'], text="").pack()
            no_task_label = ctk.CTkLabel(empty_frame, text="No tasks here!", font=("Inter", 18, "bold"), text_color=self.colors['text_primary'])
            no_task_label.pack(pady=(10, 5))
            no_task_sublabel = ctk.CTkLabel(empty_frame, text=f"Add a new task in the '{self.current_category}' category to get started.", text_color=self.colors['text_secondary'])
            no_task_sublabel.pack()
        else:
            for task in filtered_tasks:
                self.create_task_widget(task)
        
        self.update_category_buttons()

    def save_data(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.tasks = []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
        
        self.set_category_filter("All")

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()