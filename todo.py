import os
from datetime import datetime

class Task:
    def __init__(self, serial_number, name, created_datetime, deadline, status, steps, completed_datetime=""):
        self.serial_number = serial_number
        self.name = name
        self.created_datetime = created_datetime
        self.deadline = deadline
        self.status = status
        self.completed_datetime = completed_datetime
        self.steps = steps

class ToDoListManager:
    def __init__(self, filename='tasks.txt'):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def add_task(self, name, deadline, steps):
        serial_number = len(self.tasks) + 1
        created_datetime = datetime.now().strftime('%Y-%m-%d %H:%M')
        status = 'Pending'
        task = Task(serial_number, name, created_datetime, deadline, status, steps)
        self.tasks.append(task)
        self.save_tasks()

    def edit_task(self, serial_number, name=None, deadline=None, steps=None):
        for task in self.tasks:
            if task.serial_number == serial_number:
                if name:
                    task.name = name
                if deadline:
                    task.deadline = deadline
                if steps:
                    task.steps = steps
                self.save_tasks()
                return True
        return False

    def mark_task_completed(self, serial_number):
        for task in self.tasks:
            if task.serial_number == serial_number:
                task.status = 'Completed'
                task.completed_datetime = datetime.now().strftime('%Y-%m-%d %H:%M')
                self.save_tasks()
                return True
        return False

    def delete_task(self, serial_number):
        for i, task in enumerate(self.tasks):
            if task.serial_number == serial_number:
                del self.tasks[i]
                for idx, t in enumerate(self.tasks):
                    t.serial_number = idx + 1
                self.save_tasks()
                return True
        return False

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            header = f"{'Serial No':<10}{'Task Name':<20}{'Status':<15}{'Created Date':<20}{'Due Date':<20}{'Completed Date':<20}{'Steps'}\n"
            file.write(header)
            file.write('-' * 120 + '\n')
            for task in self.tasks:
                steps_str = ';'.join(task.steps)
                line = f"{task.serial_number:<10}{task.name:<20}{task.status:<15}{task.created_datetime:<20}{task.deadline:<20}{task.completed_datetime:<20}{steps_str}\n"
                file.write(line)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                for line in lines[2:]:
                    if line.strip():
                        try:
                            serial_number = int(line[0:10].strip())
                            name = line[10:30].strip()
                            status = line[30:45].strip()
                            created_datetime = line[45:65].strip()
                            deadline = line[65:85].strip()
                            completed_datetime = line[85:105].strip()
                            steps_str = line[105:].strip()
                            steps = steps_str.split(';') if steps_str else []
                            task = Task(serial_number, name, created_datetime, deadline, status, steps, completed_datetime)
                            self.tasks.append(task)
                        except Exception as e:
                            print(f"Skipping malformed line: {line.strip()} ({e})")

    def display_tasks(self):
        if not self.tasks:
            print("No tasks to display.")
            return
        print(f"{'Serial No':<10}{'Task Name':<20}{'Status':<15}{'Created Date':<20}{'Due Date':<20}{'Completed Date':<20}{'Steps'}")
        print('-' * 120)
        for task in self.tasks:
            steps_str = ';'.join(task.steps)
            print(f"{task.serial_number:<10}{task.name:<20}{task.status:<15}{task.created_datetime:<20}{task.deadline:<20}{task.completed_datetime:<20}{steps_str}")

def main():
    manager = ToDoListManager()
    
    while True:
        print("\nWelcome to To-Do List Manager!")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Edit Task")
        print("4. Delete Task")
        print("5. Mark Task as Completed")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter task name: ")
            deadline = input("Enter due date (YYYY-MM-DD HH:MM): ")
            steps = input("Enter steps (separated by semicolon ';'): ").split(';')
            manager.add_task(name, deadline, steps)
            print("Task added successfully.")

        elif choice == '2':
            manager.display_tasks()

        elif choice == '3':
            manager.display_tasks()
            try:
                serial = int(input("Enter serial number of task to edit: "))
                print("Leave blank to keep existing value")
                name = input("Enter Malin: Enter new task name (or press Enter to keep current): ")
                deadline = input("Enter new due date (YYYY-MM-DD HH:MM) (or press Enter to keep current): ")
                steps = input("Enter new steps (separated by semicolon ';') (or press Enter to keep current): ")
                steps = steps.split(';') if steps else None
                if manager.edit_task(serial, name or None, deadline or None, steps):
                    print("Task edited successfully.")
                else:
                    print("Task not found.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '4':
            manager.display_tasks()
            try:
                serial = int(input("Enter serial number of task to delete: "))
                if manager.delete_task(serial):
                    print("Task deleted successfully.")
                else:
                    print("Task not found.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '5':
            manager.display_tasks()
            try:
                serial = int(input("Enter serial number of task to mark as completed: "))
                if manager.mark_task_completed(serial):
                    print("Task marked as completed.")
                else:
                    print("Invalid serial number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '6':
            print("Thank you for using To-Do List Manager!")
            break

        else:
            print("Invalid choice. Please select 1-6.")

if __name__ == '__main__':
    main()
