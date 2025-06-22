# main.py

import sys
from PySide6.QtWidgets import QApplication
from GUI.main_window import MainWindow
from logic.database import init_db # <--- Додаємо цей імпорт

def main():
    init_db() # <--- ВИКЛИКАЄМО ІНІЦІАЛІЗАЦІЮ БД НА САМОМУ ПОЧАТКУ
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()