import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import *

import Backup_comparer
import Backup_creator


class Application(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file1_dir = ""
        self.file2_dir = ""
        self.save_loc = ""
        self.file1 = QLabel("None")
        self.file2 = QLabel("None")
        self.main_layout = QGridLayout()
        app.setStyle('Fusion')
        self.setWindowTitle("Suave Detector v1.1")
        self.save_label = QLabel("None")
        self.save_label.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        self.save_button = QPushButton("Choose a save location")
        self.save_button.pushed = 0
        self.save_button.clicked.connect(self.save_dir_open)
        save_layout = QVBoxLayout()
        save_layout.addWidget(self.save_label)
        save_layout.addWidget(self.save_button)
        save_group = QGroupBox()
        save_group.setLayout(save_layout)
        self.big_button = QPushButton("Compare Backups")
        self.big_button.setEnabled(False)
        self.big_button.clicked.connect(self.big_button_click)
        self.file1_button = QPushButton("Choose Backup 1")
        self.file1_button.pushed = 0
        self.file1_button.clicked.connect(self.file1_open)
        self.file2_button = QPushButton("Choose Backup 2")
        self.file2_button.pushed = 0
        self.file2_button.clicked.connect(self.file2_open)
        file_select_lay = QFormLayout()
        file_select_lay.addRow(self.file1, self.file1_button)
        file_select_lay.addRow(self.file2, self.file2_button)
        self.file_group = QGroupBox("Compare Files")
        self.file_group.setCheckable(True)
        self.file_group.checked = True
        self.file_group.clicked.connect(self.file_group_checked)
        self.file_group.setLayout(file_select_lay)
        self.main_layout.addWidget(self.file_group, 0, 0)
        self.main_layout.addWidget(save_group, 0, 1)
        self.main_layout.addWidget(self.big_button, 0, 2)
        self.setLayout(self.main_layout)

    def file_group_checked(self):
        self.file_group.checked = not self.file_group.checked
        self.file_group.setChecked(self.file_group.checked)
        if self.file_group.checked:
            self.big_button.setText("Compare Backups")
        else:
            self.big_button.setText("Create a Backup")
        if (
                self.big_button.text() == "Compare Backups" and self.save_label.text() != "None" and self.file1.text() != "None" and self.file2.text() != "None") or (
                self.big_button.text() == "Create a Backup" and self.save_label.text() != "None"):
            self.big_button.setEnabled(True)
        else:
            self.big_button.setEnabled(False)

    def save_dir_open(self):
        directory = QFileDialog.getExistingDirectory(None, 'Select a folder')
        if sys.platform == "win32":
            root = "\\"
        else:
            root = "/"
        if directory:
            dir_ = directory.split("/")
            self.save_loc = root.join(dir_)
            self.save_label.setText(dir_[len(dir_) - 1])
        if (
                self.file1.text() != "None" and self.file2.text() != "None" and self.big_button.text() == "Compare Backups") or (
                self.big_button.text() == "Create a Backup") and self.save_label.text() != "None":
            self.big_button.setEnabled(True)
        else:
            self.big_button.setEnabled(False)

    def file1_open(self):
        file, check = QFileDialog.getOpenFileName(None, "Open Backup 1", "", "CSV files (*.csv)")
        if sys.platform == "win32":
            root = "\\"
        else:
            root = "/"
        if check:
            file = file.split("/")
            self.file1_dir = root.join(file)
            self.file1.setText(file[len(file) - 1])
        if (self.file1.text() != "None" and self.file2.text() != "None") and (
                self.big_button.text() == "Compare Backups" or self.big_button.text() == "Create a Backup") and self.save_label.text() != "None":
            self.big_button.setEnabled(True)
        else:
            self.big_button.setEnabled(False)

    def big_button_click(self):
        alert = QMessageBox()
        alert.setText("Press Ok to start process.")
        alert.exec()
        if sys.platform == "win32":
            root = "\\"
            save_loc = self.save_loc + root
        else:
            root = "/"
            save_loc = self.save_loc + root
        if self.big_button.text() == "Compare Backups":
            adds, dels, mods = Backup_comparer.open_files(self.file1_dir, self.file2_dir)
            Backup_comparer.write_to_file(adds, dels, mods, save_loc)
        else:
            Backup_creator.main(save_loc)
        alert = QMessageBox()
        alert.setText("File saved at " + save_loc + "!")
        alert.setInformativeText("Press ok to continue")
        alert.exec()

    def proceeding(self):
        self.setLayout(self.main_layout)

    def file2_open(self):
        file, check = QFileDialog.getOpenFileName(None, "Open Backup 1", "", "CSV files (*.csv)")
        if sys.platform == "win32":
            root = "\\"
        else:
            root = "/"
        if check:
            file = file.split("/")
            self.file2_dir = root.join(file)
            self.file2.setText(file[len(file) - 1])
        if ((
                    self.file1.text() != "None" and self.file2.text() != "None" and self.big_button.text() == "Compare Backups") or self.big_button.text() == "Create a Backup") and self.save_label.text() != "None":
            self.big_button.setEnabled(True)
        else:
            self.big_button.setEnabled(False)


app = QApplication([])
ex = Application()
ex.show()
sys.exit(app.exec())
