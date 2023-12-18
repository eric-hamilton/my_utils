import sys
import os
import configparser
import json
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QMenu, QAction
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QMimeData
import qdarkstyle

class CustomException(Exception):
    def __init__(self, message):
        self.message = message
    
class DuplicateNameError(CustomException):
    def __str__(self):
        return f'Duplicate App Name -> {self.message}'    


class MainWindow(QMainWindow):
    def __init__(self, programs):
        super().__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet())
        self.programs = programs
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        sorted_programs = sorted(self.programs.items(), key=lambda x: x[0])

        for program_name, program_info in sorted_programs:
            icon_path = program_info['icon_path']
            button = AppButton(program_name, program_info)
            if icon_path:
                icon = QIcon(icon_path)
                button.setIcon(icon)
            layout.addWidget(button)

        self.setCentralWidget(central_widget) 
        self.setWindowTitle('App Launcher')
        self.setGeometry(100, 100, 300, 200)
        self.create_menu_bar()

        
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File
        file_menu = menubar.addMenu('File')
        
        open_conf_action = QAction("Open Config File", self)
        file_menu.addAction(open_conf_action)
        
        pref_action = QAction("Preferences", self)
        file_menu.addAction(pref_action)

        quit_action = QAction('Exit', self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Apps        
        config_menu = menubar.addMenu('Apps')
        add_app_action = QAction("Manage Apps", self)
        config_menu.addAction(add_app_action)
        
        # Help
        help_menu = menubar.addMenu('Help')
        
        help_action = QAction('Help', self)
        help_menu.addAction(help_action)
        
        about_action = QAction('About', self)
        help_menu.addAction(about_action)
        

class AppButton(QPushButton):
    def __init__(self, program_name, program_info):
        super().__init__(program_name)
        self.executable_path = program_info["executable"]
        self.keep_open = program_info["keep_open"]
        self.clicked.connect(self.runProgram)

    def runProgram(self):
        self.keep_open = False
        if self.keep_open:
            subprocess.run([self.executable_path])
        else:
            subprocess.Popen(self.executable_path)                
            sys.exit()


def read_config(config_file):
    config = configparser.ConfigParser()    
    config.read(config_file)   
    programs = {}
    unique_names = []
    for section in config.sections():
        program_name = section
        program_executable = config.get(section, 'executable')
        program_icon_path = config.get(section, 'icon_path', fallback=None)
        keep_open = int(config.get(section, 'keep_open', fallback=0))
        program_arg_names = json.loads(config.get(section,"arg_names"))
        for arg_name in program_arg_names:
            if arg_name in unique_names:
                raise DuplicateNameError(f"{arg_name} from {section} is a duplicate.")
        unique_names.extend(program_arg_names)
        programs[program_name] = {
                'executable': program_executable,
                'icon_path': program_icon_path,
                "arg_names":program_arg_names, 
                "keep_open":keep_open
                }
    return programs

def run_program(given_program, programs, args):
    arg_list = args[2:]
    arg_list = " " + " ".join(arg_list)
    for program in programs:           
        if given_program in [x.lower() for x in programs[program]["arg_names"]]:
            if programs[program]["keep_open"]:
                subprocess.run(programs[program]["executable"] + arg_list)
            else:                
                subprocess.Popen(programs[program]["executable"] + arg_list)
            return
    
    print(f"Could not find program: {given_program}")

def list_programs(programs):
    for program in programs:
        print(f"{program}: -> {programs[program]['arg_names']}\n")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    conf_path = os.path.join(script_directory, 'config.ini')
    programs = read_config(conf_path)
    if len(sys.argv) >= 2:
        given_program = sys.argv[1].lower()
        if given_program == "list":
            list_programs(programs)
            sys.exit()
        run_program(given_program, programs, sys.argv)

    else:
        window = MainWindow(programs)
        window.show()
        sys.exit(app.exec_())
