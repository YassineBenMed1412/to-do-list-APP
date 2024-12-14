import sqlite3


conn = sqlite3.connect('todo_list.db')
cursor = conn.cursor()

def create_table():
  
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT,
                    theme TEXT)''')
    
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS PRIORITY (
                    PRIO_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER,
                    Priority TEXT CHECK (Priority IN ("Short-term","short","short term","long term","long", "Long-Term", "Life-Long-Goals")),
                    FOREIGN KEY (task_id) REFERENCES tasks(id))''')
    
    conn.commit()

def add_task(task, priority,theme):

    cursor.execute("INSERT INTO tasks (task, theme) VALUES (?,?)", (task, theme)) 

    task_id = cursor.lastrowid 
    
   
    cursor.execute("INSERT INTO PRIORITY (task_id, Priority) VALUES (?, ?)", (task_id, priority))
    conn.commit()
    print(f"Task '{task}' with Priority: {priority} and theme {theme} added successfully.")

def get_tasks():
    
    cursor.execute('''SELECT tasks.id, tasks.task, priority.Priority 
                      FROM tasks  
                      JOIN PRIORITY  ON tasks.id = priority.task_id
                      ORDER BY priority.Priority''')
    tasks = cursor.fetchall()
    
    if not tasks:
        print("No tasks available.")
        return
    
    print("\nTasks (ordered by Priority):")
    for task in tasks:
        print(f"ID: {task[0]}, Task: {task[1]}, Priority: {task[2]}")

def set_high_priority(task_id):
    
    cursor.execute("UPDATE PRIORITY SET Priority = 'Short-term' WHERE task_id = ?", (task_id,))
    conn.commit()
    print(f"Task with ID {task_id} set to high priority, HURRY UP!.")
def UPDATE_LOW_priority(task_id):
    
    cursor.execute("UPDATE PRIORITY SET Priority = 'Long-Term' WHERE task_id = ?", (task_id,))
    conn.commit()
    print(f"Task with ID {task_id} set to Low priority , Take Your sweet time :).")

def delete_(task_id):
    cursor.execute("DELETE FROM PRIORITY WHERE task_id = ?", (task_id,))
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    print(f"Task with ID {task_id} deleted successfully.")

def main():
    create_table()
    while True:
        print("\nTo-Do List Menu:")
        print("1. Add Task")
        print("2. Show Tasks (Ordered by Priority)")
        print("3. Set Task to High Priority")
        print("4. Set Task to Low Priority")
        print("5. Delete Task")
        print("6. Exit")
        
        request = input("Choose an option: ")

        if request == '1':
            task = input("Enter task description : ")
            priority = input("Enter Priority (Short-term, Long-Term, Life-Long-Goals) : ")
            theme=input("Enter theme : ")
            add_task(task, priority,theme)
        elif request == '2':
            get_tasks()
        elif request == '3':
            task_id = int(input("Enter task ID to set to high priority: "))
            set_high_priority(task_id)
        elif request == '4':
            task_id = int(input("Enter task ID to set to Low priority: "))
            UPDATE_LOW_priority(task_id)
        elif request == '5':
            task_id = int(input("Enter task ID to delete: "))
            delete_(task_id)
        elif request == '6':
            print("Closing TO-DO List, See You Later!!")
            break
        else:
            print("ERROR, try again.")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
