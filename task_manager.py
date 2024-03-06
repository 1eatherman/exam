import json


class Task:
    def __init__(self, task_id, name, description, status=False, assigned_employee=None):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.status = status
        self.assigned_employee = assigned_employee

    def update_status(self, status):
        self.status = status

    def to_dict(self):
        task_dict = {
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "assigned_employee": self.assigned_employee
        }
        return task_dict


class Employee:
    def __init__(self, employee_id, name, email):
        self.employee_id = employee_id
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "email": self.email
        }


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.employees = []

    def add_task(self, task, employee_id):
        if not task.task_id or not task.name or not task.description:
            print("Please provide valid task ID, name, and description.")
            return

        for existing_task in self.tasks:
            if existing_task.task_id == task.task_id:
                print(f"Task with ID {task.task_id} already exists.")
                return

        employee_found = False
        for employee in self.employees:
            if employee.employee_id == employee_id:
                task.assigned_employee = employee_id
                employee_found = True
                break

        if not employee_found:
            print("Employee with given ID not found.")

        self.tasks.append(task)
        self.save_data()

    def add_employee(self, employee):
        if not employee.employee_id or not employee.name or not employee.email:
            print("Please provide valid employee ID, name, and email.")
            return

        for existing_employee in self.employees:
            if existing_employee.employee_id == employee.employee_id:
                print(f"Employee with ID {employee.employee_id} already exists.")
                return
            if existing_employee.email == employee.email:
                print(f"Employee with email {employee.email} already exists.")
                return

        self.employees.append(employee)
        self.save_data()

    def update_task_status(self, task_id, status):
        for task in self.tasks:
            if task.task_id == task_id:
                task.update_status(status)
                self.save_data()
                break

    def delete_task(self, task_id: int):
        task_found = False
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                task_found = True
                print(f"Task with ID {task_id} successfully deleted.")
                self.save_data()
                break
        if not task_found:
            print(f"Task with ID {task_id} not found.")

    def delete_employee(self, employee_id: int):
        employee_found = False
        for employee in self.employees:
            if employee.employee_id == employee_id:
                self.employees.remove(employee)
                employee_found = True
                print(f"Employee with ID {employee_id} successfully deleted.")
                self.save_data()
                break
        if not employee_found:
            print(f"Employee with ID {employee_id} not found.")

    def save_data(self):
        with open('data.json', 'w') as data_file:
            data = {
                "tasks": [task.to_dict() for task in self.tasks],
                "employees": [employee.to_dict() for employee in self.employees]
            }
            json.dump(data, data_file, indent=4)

    def load_data(self):
        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
                self.tasks = [Task(task['task_id'], task['name'], task['description'], task['status'], task.get('assigned_employee')) for task in
                              data["tasks"]]
                self.employees = [Employee(employee['employee_id'], employee['name'], employee['email']) for employee in
                                  data["employees"]]
        except FileNotFoundError:
            print("No data found. Starting with empty task list and employee list.")

    def list_tasks(self):
        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
                tasks = data.get("tasks", [])
                if not tasks:
                    print("Список завдань порожній.")
                    return

                print("Список завдань:")
                for task_data in tasks:
                    print(
                        f"ID: {task_data['task_id']}, Назва: {task_data['name']}, Опис: {task_data['description']}, Статус: {'Виконано' if task_data['status'] else 'Не виконано'}, Призначено: {task_data.get('assigned_employee')}")
        except FileNotFoundError:
            print("Файл з даними не знайдено.")

    def list_employees(self):
        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
                employees = data.get("employees", [])
                if not employees:
                    print("Список працівників порожній.")
                    return

                print("Список працівників:")
                for employee_data in employees:
                    print(
                        f"ID: {employee_data['employee_id']}, Ім'я: {employee_data['name']}, Email: {employee_data['email']}")
        except FileNotFoundError:
            print("Файл з даними не знайдено.")

    def list_employee_tasks(self, employee_id: int):
        tasks_found = False
        for task in self.tasks:
            if task.assigned_employee == employee_id:
                if not tasks_found:
                    print(f"Список завдань для робітника з ID {employee_id}:")
                    tasks_found = True
                print(
                    f"ID: {task.task_id}, Назва: {task.name}, Опис: {task.description}, Статус: {'Виконано' if task.status else 'Не виконано'}")
        if not tasks_found:
            print(f"Робітник з ID {employee_id} не має призначених завдань.")

    def check_task_status_and_remind(self):
        try:
            employees_with_unfinished_tasks = {}

            for task in self.tasks:
                if task.assigned_employee and not task.status:
                    employee_id = task.assigned_employee
                    employee_name = self.get_employee_name(employee_id)
                    task_name = task.name
                    if employee_id in employees_with_unfinished_tasks:
                        employees_with_unfinished_tasks[employee_id]['tasks'].append(task_name)
                    else:
                        employees_with_unfinished_tasks[employee_id] = {'name': employee_name, 'tasks': [task_name]}

            if employees_with_unfinished_tasks:
                print("Працівники з невиконаними завданнями:")
                for employee_id, employee_data in employees_with_unfinished_tasks.items():
                    tasks_str = ', '.join(employee_data['tasks'])
                    print(f"{employee_data['name']} (ID: {employee_id}): {tasks_str}.")
                print("Нагадування відправлено.")
            else:
                print("Усі завдання виконані.")
        except FileNotFoundError:
            print("Файл з даними не знайдено.")
        except KeyError:
            print("Помилка у форматі даних. Перевірте структуру файлу 'data.json'.")

    def get_employee_name(self, employee_id):
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee.name
        return "Unknown"


if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.load_data()

    while True:
        print("1. Додати завдання")
        print("2. Додати працівника")
        print("3. Оновити статус завдання")
        print("4. Видалити завдання за ID")
        print("5. Видалити працівника за ID")
        print("6. Список завдань")
        print("7. Список працівників")
        print("8. Список завдань для робітника за його ID")
        print("9. Перевірити статус завдань та надіслати нагадування")
        print("10. Вихід")

        choice = input("Введіть ваш вибір: ")

        if choice == "1":
            task_id = int(input("Введіть ID завдання: "))
            name = input("Введіть назву завдання: ")
            description = input("Введіть опис завдання: ")
            employee_id = int(input("Введіть ID працівника, щоб призначити завдання: "))
            task = Task(task_id, name, description)
            task_manager.add_task(task, employee_id)
            print("Завдання успішно додано!")
        elif choice == "2":
            employee_id = int(input("Введіть ID працівника: "))
            name = input("Введіть ім'я працівника: ")
            email = input("Введіть email працівника: ")
            employee = Employee(employee_id, name, email)
            task_manager.add_employee(employee)
            print("Працівника успішно додано!")
        elif choice == "3":
            task_id = int(input("Введіть ID завдання для оновлення статусу: "))
            status = input("Введіть статус завдання (True/False): ").lower() == "true"
            task_manager.update_task_status(task_id, status)
            print("Статус завдання успішно оновлено!")
        elif choice == "4":
            task_id = int(input("Введіть ID завдання для видалення: "))
            task_manager.delete_task(task_id)
        elif choice == "5":
            employee_id = int(input("Введіть ID працівника для видалення: "))
            task_manager.delete_employee(employee_id)
        elif choice == "6":
            task_manager.list_tasks()
        elif choice == "7":
            task_manager.list_employees()
        elif choice == "8":
            employee_id = int(input("Введіть ID робітника для перегляду його завдань: "))
            task_manager.list_employee_tasks(employee_id)
        elif choice == "9":
            task_manager.check_task_status_and_remind()
        elif choice == "10":
            print("Завершення програми.")
            task_manager.save_data()
            break
        else:
            print("Неправильний вибір. Будь ласка, спробуйте знову.")
