import sys
import time
from pymongo import MongoClient

# MongoDb config
ip = 'localhost'
port = 27017
db_name = 'masakra'
db_collection = 'task'


# Other
version = "0.0.1"

def GetTime():
    time_now = time.strftime("%H:%M:%S %d/%m/%Y")
    return time_now

class db:
    def __init__(self):
        self.client = MongoClient(ip, port) 
        self.db = self.client[db_name]
        self.coll = self.db[db_collection]
    
    def getLastId(self):
        ids = [x for x in self.coll.find({}, {'_id':0,'id':1})]
        if len(ids) == 0:
            return 0
        ids_ = [x['id'] for x in ids]
        ids_.sort()
        return ids_[-1]

    def getAllTask(self):
        tasks = [x for x in self.coll.find()]
        for x in tasks:
            print(x)
    
    def insertTask(self, task_):
        # Adding Template
        task_template = {
            'id': self.getLastId() + 1,
            'done': 0,
            'task_body': task_,
            'task_time': GetTime()
        }
        self.coll.insert_one(task_template)

    
class Task(db):
    def __init__(self):
        super().__init__()
        # Get taks list

def Interface():
    Temp = Task()
    Temp.insertTask("masakra cos tam")
    Temp.insertTask("masakra cos taam 22")


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
        print("interface")
        Interface()
    else:
        print("Nieprawidłowe użycie, użyj --help by dowiedzieć się jak używać") 





if __name__ == "__main__":
    print("mTask by masakra(.dev), v%s" % (version))
    Core()