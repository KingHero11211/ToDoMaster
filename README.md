# TodoMaster 

A modern, beautiful, and feature-rich desktop Todo List application built with Python and the CustomTkinter library. This project serves as an excellent example of creating a polished, professional-looking GUI application.

## 📸 Screenshots

*(Pro Tip: Replace these links with your own screenshots after uploading!)*

| Light Mode | Dark Mode |
| :---: | :---: |
| ![Image](https://github.com/user-attachments/assets/782c622e-15f8-4eb8-be04-791360c67fe4) | ![Image](https://github.com/user-attachments/assets/d7d566f5-6054-476c-b6e4-663bc0047a61) |

**Add/Edit Task Dialog with Calendar:**

![Image](https://github.com/user-attachments/assets/52c1cbd1-4a70-4810-ba88-41b29299c918)


## ✨ Features

- **Modern & Clean UI**: A visually appealing interface built with CustomTkinter.
- **Task Management**: Easily add, edit, and delete tasks.
- **Categorization**: Organize tasks into categories like "Personal," "Work," "Shopping," etc.
- **Priority Levels**: Assign "High," "Medium," or "Low" priority to tasks, each with a distinct color indicator.
- **Due Dates**: Select a due date for any task using an interactive calendar pop-up.
- **Light & Dark Modes**: Switch between a sleek light mode and a cool dark mode with a single click.
- **Persistent Storage**: Your tasks are automatically saved to a `todo_data.json` file and loaded every time you open the app.
- **Intuitive Navigation**: A clean sidebar for filtering tasks by category.
- **Empty State Illustration**: A friendly message and graphic appear when a category has no tasks.


## 🛠️ Tech Stack

- **Language**: Python 3
- **GUI Framework**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- **Calendar Widget**: [tkcalendar](https://github.com/j4321/tkcalendar)
- **Image Handling**: [Pillow (PIL)](https://python-pillow.org/)


## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

You need to have Python 3 installed on your system.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    ```
    *(Replace `your-username` and `your-repository-name` with your actual GitHub details)*

2.  **Navigate to the project directory:**
    ```bash
    cd your-repository-name
    ```

3.  **Install the required libraries:**
    This project uses a `requirements.txt` file to manage dependencies. Run the following command to install them all at once:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ensure you have the icons:**
    Make sure the `icons` folder is present in the project directory and contains all the necessary `.png` files.

### Running the Application

Once the installation is complete, you can run the application with this command:
```bash
python "to do list.py"
```

## 📂 Project Structure
The project is organized as follows:

ToDoMaster/
├── icons/
│ ├── book-marked.png
│ ├── briefcase.png
│ ├── calendar.png
│ ├── delete.png
│ ├── edit.png
│ ├── heart-pulse.png
│ ├── home.png
│ ├── logo.png
│ ├── no-tasks.png
│ ├── plus.png
│ └── shopping-cart.png
├── to do list.py
├── requirements.txt
└── README.md


## 🌟 Future Improvements

- [ ] Add a search bar to filter tasks by name.
- [ ] Implement desktop notifications for upcoming or overdue tasks.
- [ ] Add support for sub-tasks.
- [ ] Create a "Settings" page for more user customization.
- [ ] Add task sorting options (by date, by priority, etc.).

## 📜 License

This project is licensed under the MIT License.
