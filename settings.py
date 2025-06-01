# settings_dialog.py
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QLabel,
    QSpinBox,
)


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки игры")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Настройки команд
        team_group = QLabel("Настройки команд")
        layout.addWidget(team_group)

        self.team_count_combo = QComboBox()
        self.team_count_combo.addItems(["1 команда", "2 команды"])
        layout.addWidget(QLabel("Количество команд:"))
        layout.addWidget(self.team_count_combo)

        self.team1_edit = QLineEdit("Команда 1")
        self.team2_edit = QLineEdit("Команда 2")
        layout.addWidget(QLabel("Название команды 1:"))
        layout.addWidget(self.team1_edit)
        layout.addWidget(QLabel("Название команды 2:"))
        layout.addWidget(self.team2_edit)

        # Настройки времени
        time_group = QLabel("Настройки времени")
        layout.addWidget(time_group)

        self.time_combo = QComboBox()
        self.time_combo.addItems(["3 минуты", "7 минут", "0 минут"])
        layout.addWidget(QLabel("Время подготовки:"))
        layout.addWidget(self.time_combo)

        # Кнопки
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.accept)
        layout.addWidget(self.save_btn)

    def get_settings(self):
        """Возвращает настройки в виде кортежа (team_names, preparation_time)"""
        team_count = 1 if self.team_count_combo.currentText() == "1 команда" else 2
        team_names = [self.team1_edit.text()]
        if team_count == 2:
            team_names.append(self.team2_edit.text())

        time_mapping = {"3 минуты": 3, "7 минут": 7, "0 минут": 0}
        preparation_time = time_mapping[self.time_combo.currentText()]

        return team_names, preparation_time
