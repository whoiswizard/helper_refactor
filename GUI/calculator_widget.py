# GUI/calculator_widget.py

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, 
    QComboBox, QVBoxLayout, QGridLayout, QMessageBox, QGroupBox
)
# Імпортуємо логіку з папки logic
from logic.calculator import Calculator

class CalculatorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculator = Calculator()
        self.init_ui()

    def init_ui(self):
        # ... (решта коду цього файлу не змінюється)
        main_layout = QVBoxLayout(self)
        calc_group = QGroupBox("Калькулятор Угод"); calc_layout = QGridLayout()
        investment_label = QLabel("Сума інвестиції:"); self.investment_input = QLineEdit(); self.investment_input.setPlaceholderText("Введіть суму")
        entry_price_label = QLabel("Ціна входу:"); self.entry_price_input = QLineEdit(); self.entry_price_input.setPlaceholderText("Введіть ціну")
        take_profit_label = QLabel("Тейк-профіт:"); self.take_profit_input = QLineEdit(); self.take_profit_input.setPlaceholderText("Введіть ціль по прибутку")
        stop_loss_label = QLabel("Стоп-лос:"); self.stop_loss_input = QLineEdit(); self.stop_loss_input.setPlaceholderText("Введіть стоп-ціну")
        leverage_label = QLabel("Кредитне плече:"); self.leverage_input = QLineEdit(); self.leverage_input.setPlaceholderText("Введіть плече")
        position_type_label = QLabel("Тип позиції:"); self.position_type_combo = QComboBox(); self.position_type_combo.addItems(["Лонг", "Шорт"])
        self.calculate_button = QPushButton("Розрахувати"); self.calculate_button.clicked.connect(self.calculate)
        self.profit_label = QLabel("Прибуток: "); self.loss_label = QLabel("Збиток: "); self.liquidation_label = QLabel("Ціна ліквідації: ")
        calc_layout.addWidget(investment_label, 0, 0); calc_layout.addWidget(self.investment_input, 0, 1)
        calc_layout.addWidget(entry_price_label, 1, 0); calc_layout.addWidget(self.entry_price_input, 1, 1)
        calc_layout.addWidget(take_profit_label, 2, 0); calc_layout.addWidget(self.take_profit_input, 2, 1)
        calc_layout.addWidget(stop_loss_label, 3, 0); calc_layout.addWidget(self.stop_loss_input, 3, 1)
        calc_layout.addWidget(leverage_label, 4, 0); calc_layout.addWidget(self.leverage_input, 4, 1)
        calc_layout.addWidget(position_type_label, 5, 0); calc_layout.addWidget(self.position_type_combo, 5, 1)
        calc_layout.addWidget(self.calculate_button, 6, 0, 1, 2)
        calc_layout.addWidget(self.profit_label, 7, 0, 1, 2); calc_layout.addWidget(self.loss_label, 8, 0, 1, 2); calc_layout.addWidget(self.liquidation_label, 9, 0, 1, 2)
        calc_group.setLayout(calc_layout); main_layout.addWidget(calc_group)

    def calculate(self):
        try:
            investment_amount = float(self.investment_input.text()) if self.investment_input.text() else 0
            entry_price = float(self.entry_price_input.text()) if self.entry_price_input.text() else 0
            take_profit = float(self.take_profit_input.text()) if self.take_profit_input.text() else 0
            stop_loss = float(self.stop_loss_input.text()) if self.stop_loss_input.text() else 0
            leverage = float(self.leverage_input.text()) if self.leverage_input.text() else 0
            position_type = self.position_type_combo.currentText()
            results = self.calculator.calculate(investment_amount, entry_price, take_profit, stop_loss, leverage, position_type)
            self.profit_label.setText(f"Прибуток: ${results['profit']:.2f}"); self.loss_label.setText(f"Збиток: ${results['loss']:.2f}"); self.liquidation_label.setText(f"Ціна ліквідації: ${results['liquidation_price']:.4f}")
        except ValueError: QMessageBox.critical(self, "Помилка", "Будь ласка, введіть коректні числові значення.")
        except Exception as e: QMessageBox.critical(self, "Помилка", f"Сталася помилка: {str(e)}")