import os
import subprocess
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget


UTILITIES = {
    "Backup": "backup/backup.py",
    "Copy Path": "copy_path/copy_path.py",
    "Empty": "empty/empty.py",
    "Find": "find/find.py",
    "Hasher": "hasher/hasher.py",
    "Move": "move/move.py",
    "Peek": "peek/peek.py",
    "Search": "search/search.py",
}

class MyUtilsLauncher(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Utils")
        self.setGeometry(200, 200, 300, 400)

        layout = QVBoxLayout()

        for name, script in UTILITIES.items():
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, s=script: self.run_script(s))
            layout.addWidget(btn)

        self.setLayout(layout)

    def run_script(self, script):
        script_path = os.path.join(os.path.dirname(__file__), script)
        subprocess.Popen(["python", script_path], shell=True)

if __name__ == "__main__":
    app = QApplication([])
    window = MyUtilsLauncher()
    window.show()
    app.exec()
