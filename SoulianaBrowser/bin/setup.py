import os
import subprocess
import sys
from PyQt5.QtWidgets import (
    QApplication, QWizard, QWizardPage, QLabel, QVBoxLayout, QPushButton, QMessageBox
)

ARCHIVE_FILE = "Release.7z"
EXE_PATH = os.path.join("Release", "Release", "SoulianaBrowser.exe")

def is_installed():
    return os.path.exists(EXE_PATH)

class WelcomePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("The installation still continues.")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("The wizard will still continue because we need to extract the archive, then you can start using the browser."))
        self.setLayout(layout)

class InstallPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Extracting the archive...")
        self.status_label = QLabel("Extracting the archive")
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def initializePage(self):
        if not os.path.exists(ARCHIVE_FILE):
            self.status_label.setText("Error: Release.7z not found.")
            return

        self.status_label.setText("Please wait.")
        QApplication.processEvents()

        try:
            subprocess.run(["7z.exe", "x", ARCHIVE_FILE, "-oRelease", "-y"], check=True)
            self.status_label.setText("Installation completed successfully.")
        except subprocess.CalledProcessError:
            self.status_label.setText("Installation failed.")

class FinishPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Installation Complete")
        layout = QVBoxLayout()
        label = QLabel("Souliana Web Browser has been installed.")
        layout.addWidget(label)

        self.launch_button = QPushButton("Launch Souliana")
        self.launch_button.clicked.connect(self.launch_app)
        layout.addWidget(self.launch_button)

        self.setLayout(layout)

    def launch_app(self):
        if os.path.exists(EXE_PATH):
            subprocess.Popen(EXE_PATH)
        else:
            QMessageBox.warning(self, "Error", "SoulianaBrowser.exe not found.")

class AlreadyInstalledDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Souliana Installer")
        self.setText("Souliana is already installed.")
        self.setIcon(QMessageBox.Information)
        launch_btn = self.addButton("Launch", QMessageBox.AcceptRole)
        exit_btn = self.addButton("Exit", QMessageBox.RejectRole)
        self.exec_()

        if self.clickedButton() == launch_btn:
            subprocess.Popen(EXE_PATH)
        sys.exit()

def main():
    app = QApplication(sys.argv)

    if is_installed():
        AlreadyInstalledDialog()
    else:
        wizard = QWizard()
        wizard.setWindowTitle("Souliana Web Browser Setup Wizard")
        wizard.addPage(WelcomePage())
        wizard.addPage(InstallPage())
        wizard.addPage(FinishPage())
        wizard.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
