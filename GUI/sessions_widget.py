# GUI/sessions_widget.py

from PySide6.QtWidgets import QWidget, QLabel, QGroupBox, QGridLayout, QVBoxLayout
from PySide6.QtCore import QTimer, Qt
from datetime import datetime
import pytz
# Імпортуємо логіку з папки logic
from logic.time_utils import get_current_time, get_time_until_open, is_exchange_active, CITIES_TIMEZONES

class SessionsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.init_timer()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        time_group = QGroupBox("Час Торгових Сесій")
        time_layout = QGridLayout()
        
        self.time_labels = {}
        self.countdown_labels = {}
        self.status_labels = {}

        for i, city in enumerate(CITIES_TIMEZONES.keys()):
            city_label = QLabel(city + ":")
            time_label = QLabel("...")
            countdown_label = QLabel("...")
            status_label = QLabel("...")
            
            self.time_labels[city] = time_label
            self.countdown_labels[city] = countdown_label
            self.status_labels[city] = status_label
            
            time_layout.addWidget(city_label, i, 0, alignment=Qt.AlignLeft)
            time_layout.addWidget(time_label, i, 1, alignment=Qt.AlignLeft)
            time_layout.addWidget(countdown_label, i, 2, alignment=Qt.AlignLeft)
            time_layout.addWidget(status_label, i, 3, alignment=Qt.AlignLeft)
            
        time_group.setLayout(time_layout)
        main_layout.addWidget(time_group)

    def init_timer(self):
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_times)
        self.time_timer.start(1000)
        self.update_times()

    def update_times(self):
        exchange_status = {}
        ref_now = datetime.now(pytz.timezone("Europe/London"))
        is_weekend = ref_now.weekday() in [5, 6]
        
        for city in CITIES_TIMEZONES.keys(): 
            current_time = get_current_time(city)
            time_until_open = get_time_until_open(city)
            status = "Вихідний" if is_weekend else ("Активна" if is_exchange_active(city) else "Пасивна")
            exchange_status[city] = { "current_time": current_time, "time_until_open": time_until_open, "status": status }
        
        sorted_exchanges = sorted(exchange_status.items(), key=lambda item: (item[1]["status"] != "Активна", item[1]["status"] != "Пасивна", item[1]["status"] != "Вихідний"))
        
        for city, info in sorted_exchanges:
            self.time_labels[city].setText(info["current_time"])
            self.countdown_labels[city].setText("Зараз торги" if info["status"] == "Активна" else f"До відкриття: {info['time_until_open']}")
            self.status_labels[city].setText(f"Статус: {info['status']}")