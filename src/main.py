
#Class User
from domain.entities.user import User
from presentation.main_window import MainWindow

#Rendu UI
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
import sys


def main():
    
    user = User(email="test@mail.com", username="Alex")
    info = user.get_info()
    print(info)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    main()