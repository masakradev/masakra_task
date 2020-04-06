import sys
import time
from pymongo import MongoClient
from wincon import *

# MongoDb config
IP = 'localhost'
PORT = 27017
DB_NAME = 'masakra'
DB_COLLECTION = 'task'


# Other
VERSION = "0.0.1"

def GetTime():
    time_now = time.strftime("%H:%M:%S %d/%m/%Y")
    return time_now

#Evrything about DB
class db:
    def __init__(self):
        # Connection connection exception will be added
        self.client = MongoClient(IP, PORT) 
        self.db = self.client[DB_NAME]
        self.coll = self.db[DB_COLLECTION]

    def checkId(self, id):
        ids = [x for x in self.coll.find({}, {'_id':0,'id':1})]
        ids_tab = [x['id'] for x in ids]
        if id in ids_tab:
            return True
        return False
    
    def getLastId(self):
        ids = [x for x in self.coll.find({}, {'_id':0,'id':1})]
        if len(ids) == 0:
            return 0
        ids_ = [x['id'] for x in ids]
        ids_.sort()
        return ids_[-1]

    def getAllTask(self):
        tasks = [x for x in self.coll.find()]
        return tasks

    def getNonDoneTask(self):
        tasks = [x for x in self.coll.find({'done':0}, {'_id':0})]
        return tasks

    def setTaskToDone(self, id__):
        if self.checkId(id__):
            self.coll.find_one_and_update(
                {'id':id__},
                {"$set": {"done": 1}}
                )
            return True
        return False
        
        
    def insertTask(self, task_):
        # Adding Template
        task_template = {
            'id': self.getLastId() + 1,
            'done': 0,
            'task_body': task_,
            'task_time': GetTime()
        }
        self.coll.insert_one(task_template)

# Task class, evrything about UI, commandline   
class Task(db):
    def ui_refresh(self):
        self.tasks = self.getNonDoneTask()
        self.tasks_len = len(self.tasks)
        self.page_len = int(self.tasks_len/10) + 1

    def __init__(self):
        super().__init__()
        # Ui init
        self.page_now = 1
        self.ui_refresh()

    def ui_send_error(self, error):
        gotoxy(0,15)
        print("[Error] %s " % error)
        gotoxy(0,0)

    def ui_next(self):
        if self.page_now + 1 >= self.page_len:
            self.ui_send_error("Nie ma takiej strony")
            return
        self.page_now += 1
    
    def ui_prev(self):
        if self.page_now - 1 == 0:
            self.ui_send_error("Nie ma takiej strony")
            return
        self.page_now -= 1

    def ui_add(self, args=None):
        if not args:
            self.ui_send_error("Ta komenda potrzebuje argumenty")
            return
        self.insertTask(args)
        self.ui_refresh()

    def ui_done(self, args=None):
        print(args)
        if not args:
            self.ui_send_error("Ta komenda potrzebuje argumenty")
            return
        if not self.setTaskToDone(int(args)):
            self.ui_send_error("Nie ma takiego id")
        self.ui_refresh()

    def do_function(self, func, args=None):
        if args:
            func(args)
            return
        func()


def Interface():
    Task_ = Task()
    input_ = None
    while True:
        cls()
        OFFSET = " "

        commands = {
            'next': Task_.ui_next,
            'prev': Task_.ui_prev,
            'add': Task_.ui_add,
            'done': Task_.ui_done,
        }

        if input_:
            if input_.split()[0] in commands.keys():
                if len(input_.split()) > 1:
                    args = " ".join(input_.split()[1:])
                    Task_.do_function(commands[input_.split()[0]], args)
                else:
                    Task_.do_function(commands[input_.split()[0]])
            else:
                Task_.ui_send_error("Nie ma takiej komendy, użyj help do sprawdzenia komand")
            input_ = None
                      
        print("mTask by masakra(.dev), v%s" % (VERSION))
        print("\n Id" + " "*2 + "Data" + " "*17 + "Task")
        tasks = Task_.getNonDoneTask()
        for task in tasks[(Task_.page_now-1)*10:Task_.page_now*10]:
            print(" %s%s %s%s %s" %
                (
                    task['id'], OFFSET * (3 - len(str(task['id']))),
                    task['task_time'], OFFSET * (20 -len(task['task_time'])),
                    task['task_body']
                )
            )

        gotoxy(0,14)
        print("Strona: %s/%s" % (Task_.page_now, Task_.page_len))
        gotoxy(0,16)
        input_ = input(">")


def Core():
    args_help = {
        'mtask': 'Uruchomienie interfejsu',
        'mtask --add': 'Dodawanie do listy todo nie wchodząc do programu, użycie --add <string>',
        'mtask --help': 'Komenda wyświetlająca pomoc'
        }
    print(len(sys.argv))
    if len(sys.argv) >= 2:
        if len(sys.argv) == 2 and sys.argv[1] == "--help":
            print("Użycie programu: ")
            for x in args_help.keys():
                offset = " " * (13 - len(x))
                print("%s%s -> %s" % (x, offset, args_help[x]))
            return
        if len(sys.argv) > 2 and sys.argv[1] == "--add":
            task_body = " ".join(sys.argv[2:])
            print("Czy napewno chcesz dodać : %s" % (task_body))
            print("(Y)es, (N)o")
            input_var = input()
            if input_var == "Y" or input_var == "y":
                print("Zadanie dodano")
                return
    if len(sys.argv) == 1:
        Interface()
    print("Nieprawidłowe użycie, użyj --help by dowiedzieć się jak używać") 


if __name__ == "__main__":
    print("mTask by masakra(.dev), v%s" % (VERSION))
    Core()