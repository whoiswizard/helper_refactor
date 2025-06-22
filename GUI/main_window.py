# GUI/main_window.py

from PySide6.QtWidgets import QWidget, QVBoxLayout
# Імпортуємо віджети з тієї ж папки GUI
from GUI.calculator_widget import CalculatorWidget
from GUI.tracker_widget import TrackerWidget
from GUI.sessions_widget import SessionsWidget

class MainWindow(QWidget): # <-- Переконайтесь, що назва класу саме така
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Калькулятор та Трекер Криптовалют")
        self.resize(850, 900)

        # Створюємо головний макет
        main_layout = QVBoxLayout(self)

        # Створюємо екземпляри наших віджетів-компонентів
        self.calculator = CalculatorWidget()
        self.tracker = TrackerWidget()
        self.sessions = SessionsWidget()

        # Додаємо віджети на головний макет
        main_layout.addWidget(self.calculator)
        main_layout.addWidget(self.tracker)
        main_layout.addWidget(self.sessions)