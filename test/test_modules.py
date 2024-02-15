from os import listdir
from os.path import isfile, join, dirname, abspath
import sys
import importlib
import time
import traceback

class Test:
    '''Validate and test modules.'''

    def __init__(self, parent):
        self.settings = getattr(parent, 'settings', {})
        self.message = getattr(parent, 'message', '')
        file = f"modules.{getattr(parent, 'module')}"
        imp = importlib.import_module(file)
        self.module = getattr(imp, 'Module')(self)

        self.b = "\033[1m"
        self.i = "\033[3m"
        self.gray = "\033[1;30m"
        self.green = "\033[0;32m" 
        self.lgreen = "\033[1;32m"
        self.e = "\033[0m"
        
    def test_1_required_methods(self):

        print(f"\n{self.b}[Mandatory module methods]{self.e}\n")

        methods = [
            'get_defaults',
            'check_triggers',
            'set_return_data'
        ]

        for method in methods:
            print(f"- {self.i}{method}{self.e} ", end="")
            if not method in dir(self.module):
                print(f"not found! ❌")
            else:
                print(f"found! ✔️")
    
    
    def test_2_trigger(self):
        print(f"\n{self.b}[Triggered]{self.e}\n")

        if method := self.module.check_triggers(self.message):
            print(f"True; a method {self.i}{method}{self.e} was returned")
            self.method = method
        else:
            print("False")

    
    def test_3_method(self):

        if hasattr(self, 'method'):
            print(f"\n{self.b}[Calling method {self.i}{self.method}]{self.e}\n")
            self.timer()
            try:
                getattr(self.module, self.method)()
            except Exception:
                tb = traceback.format_exc()
                print(f"Calling took {self.timer():.3f} seconds, resulted in an error:\n{self.gray}{tb}{self.e}")
            else:
                print(f"Calling took {self.timer():.3f} seconds, no errors.")
                self.final_test()

    
    def final_test(self):
        
        print(f"\n{self.b}[Return data validation]{self.e}\n")
        
        attributes = [
            'return_value',
            'return_sanitize',
            'return_separator',
            'message_title'
        ]

        for attr in attributes:
            if hasattr(self.module, attr):
                print(f"{self.lgreen}{self.i}{attr}{self.e}: {self.green}{repr(getattr(self.module, attr))}{self.e}")
            else:
                print(f"{self.i}{attr}{self.e} has not been defined!")


    def timer(self):
        if hasattr(self, 'start'):
            ret = time.perf_counter() - self.start
            del self.start
        else:
            self.start = time.perf_counter()
            ret = self.start
        
        return ret



class Module:
    def __init__(self) -> None:
        
        # Change this if you want to test the module with non-default settings
        self.settings = {}

    def set_message(self):
        self.message = input("\nType a message (or leave blank): ")
    
    def get_module(self):

        self.module = None
        
        try:
            files = [f for f in listdir("./modules") if isfile(join("./modules", f))]
        except FileNotFoundError:
            print("The 'modules' directory does not exist.")
            return None

        if not files:
            print("No modules found in 'modules' directory.")
            return None
        print("Modules:\n")
        for mod in files:
            print(f" {files.index(mod)+1}: {mod}")

        file = None

        while file == None:
            try:
                idx = int(input("\nSelect the module you want to test: "))
            except ValueError:
                print(f"Please enter a value between 1-{len(files)}.\n")
            else: 
                if idx < 1 or idx > len(files):
                    print(f"Please enter a value between 1-{len(files)}.\n")
                else:
                    file = files[idx-1]

        self.module = file.split(".")[0]
        return self.module


if __name__ == '__main__':
    # Append current directory to system path (top-level package import hack)
    sys.path.append(dirname(dirname(abspath(__file__))))
    module = Module()
    
    if module.get_module():
        module.set_message()
    else:
        exit()

    test = Test(parent=module)
    test_methods = [method for method in dir(test) if method.startswith("test_")]

    for method in sorted(test_methods):
        getattr(test, method)()
    


    

    


