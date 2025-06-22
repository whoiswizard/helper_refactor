# GUI/tracker_widget.py

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QMessageBox, QGroupBox, QHBoxLayout, QCheckBox, QTableWidget, 
    QTableWidgetItem, QHeaderView, QApplication
)
from PySide6.QtCore import Qt, QThread, QObject, Signal
from logic.tracker import get_all_coins_data
from logic.database import get_coins, add_coin, remove_coin

class Worker(QObject):
    finished = Signal(dict)
    def __init__(self, symbols):
        super().__init__(); self.symbols = symbols
    def run(self):
        all_data = get_all_coins_data(self.symbols); self.finished.emit(all_data)

class NumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, value, precision=2):
        self.numeric_value = float(value); text_to_display = f"{self.numeric_value:,.{precision}f}"
        super().__init__(text_to_display); self.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
    def __lt__(self, other):
        return self.numeric_value < other.numeric_value

class TrackerWidget(QWidget): # <-- Правильна назва класу
    def __init__(self, parent=None):
        super().__init__(parent); self.init_ui(); self.refresh_coin_display()

    def init_ui(self):
        main_layout = QVBoxLayout(self); price_group = QGroupBox("Трекінг Ринку"); price_layout = QVBoxLayout()
        top_bar_layout = QHBoxLayout(); self.refresh_button = QPushButton("Оновити"); self.refresh_button.clicked.connect(self.start_prices_update); self.delete_button = QPushButton("Видалити обрані"); self.delete_button.clicked.connect(self.delete_selected_coins)
        top_bar_layout.addWidget(self.refresh_button); top_bar_layout.addWidget(self.delete_button); top_bar_layout.addStretch(); price_layout.addLayout(top_bar_layout)
        self.coin_table = QTableWidget(); self.column_headers = ["", "Назва", "Ціна, $", "Зміна, %", "Зміна, $", "Обсяг (24г), млн $"]; self.coin_table.setColumnCount(len(self.column_headers)); self.coin_table.setHorizontalHeaderLabels(self.column_headers); self.coin_table.setSortingEnabled(True); self.coin_table.setSelectionBehavior(QTableWidget.SelectRows); self.coin_table.setEditTriggers(QTableWidget.NoEditTriggers); self.coin_table.verticalHeader().setVisible(False)
        header = self.coin_table.horizontalHeader(); header.setSectionResizeMode(0, QHeaderView.ResizeToContents); header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        for i in range(2, len(self.column_headers)): header.setSectionResizeMode(i, QHeaderView.Stretch)
        price_layout.addWidget(self.coin_table)
        add_coin_layout = QHBoxLayout(); self.new_coin_input = QLineEdit(); self.new_coin_input.setPlaceholderText("Введіть символ, напр. BTCUSDT"); self.add_coin_button = QPushButton("Додати монету"); self.add_coin_button.clicked.connect(self.add_coin)
        add_coin_layout.addWidget(self.new_coin_input); add_coin_layout.addWidget(self.add_coin_button); price_layout.addLayout(add_coin_layout)
        price_group.setLayout(price_layout); main_layout.addWidget(price_group)

    def refresh_coin_display(self):
        self.coin_table.setSortingEnabled(False); symbols = get_coins(); self.coin_table.setRowCount(len(symbols))
        for row_index, symbol in enumerate(symbols):
            checkbox_widget = QWidget(); checkbox_layout = QHBoxLayout(checkbox_widget); checkbox = QCheckBox(); checkbox_layout.addWidget(checkbox); checkbox_layout.setAlignment(Qt.AlignCenter); checkbox_layout.setContentsMargins(0,0,0,0); self.coin_table.setCellWidget(row_index, 0, checkbox_widget)
            name_item = QTableWidgetItem(symbol[:-4]); name_item.setData(Qt.UserRole, symbol); self.coin_table.setItem(row_index, 1, name_item)
            for col in range(2, len(self.column_headers)): self.coin_table.setItem(row_index, col, QTableWidgetItem("..."))
        self.coin_table.setSortingEnabled(True); self.start_prices_update()
        
    def start_prices_update(self):
        self.refresh_button.setText("Оновлення..."); self.refresh_button.setEnabled(False)
        symbols_in_table = [self.coin_table.item(row, 1).data(Qt.UserRole) for row in range(self.coin_table.rowCount()) if self.coin_table.item(row, 1)]
        self.thread = QThread(); self.worker = Worker(symbols_in_table); self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run); self.worker.finished.connect(self.finish_prices_update); self.worker.finished.connect(self.thread.quit); self.worker.finished.connect(self.worker.deleteLater); self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def finish_prices_update(self, all_data):
        for row in range(self.coin_table.rowCount()):
            name_item = self.coin_table.item(row, 1)
            if not name_item: continue
            symbol = name_item.data(Qt.UserRole); data = all_data.get(symbol)
            if data:
                price = float(data['lastPrice']); price_change_percent = float(data['priceChangePercent']); price_change_usd = price * (price_change_percent / 100); volume_usd = float(data['quoteVolume'])
                self.coin_table.setItem(row, 2, NumericTableWidgetItem(price, precision=4)); self.coin_table.setItem(row, 3, NumericTableWidgetItem(price_change_percent, precision=2)); self.coin_table.setItem(row, 4, NumericTableWidgetItem(price_change_usd, precision=2)); self.coin_table.setItem(row, 5, NumericTableWidgetItem(volume_usd / 1_000_000, precision=2))
        self.refresh_button.setText("Оновити"); self.refresh_button.setEnabled(True)

    def add_coin(self):
        symbol = self.new_coin_input.text().strip().upper()
        if not symbol: return
        if not symbol.endswith("USDT"): QMessageBox.warning(self, "Помилка", "Символ монети повинен закінчуватися на 'USDT'."); return
        if symbol in get_coins(): QMessageBox.information(self, "Інформація", f"Монета {symbol} вже відстежується."); return
        add_coin(symbol); self.new_coin_input.clear(); self.refresh_coin_display()
    
    def delete_selected_coins(self):
        coins_to_delete = []
        for row in range(self.coin_table.rowCount()):
            checkbox_widget = self.coin_table.cellWidget(row, 0)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    symbol = self.coin_table.item(row, 1).data(Qt.UserRole); coins_to_delete.append(symbol)
        if not coins_to_delete: QMessageBox.information(self, "Інформація", "Будь ласка, оберіть монети для видалення."); return
        reply = QMessageBox.question(self, "Підтвердження", f"Ви впевнені, що хочете видалити {len(coins_to_delete)} монет(и)?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for symbol in coins_to_delete: remove_coin(symbol)
            self.refresh_coin_display()