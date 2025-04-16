from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QSpinBox,
    QLabel,
    QGroupBox
)
from PyQt5.QtCore import Qt


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Настройки приложения")
        self.setFixedSize(500, 400)  # Оптимальный размер для всех настроек

        # Основной layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)  # Выравнивание по верху

        # Группа "Настройки команд"
        teams_group = QGroupBox("Настройки команд")
        teams_layout = QFormLayout()

        self.team1_edit = QLineEdit()
        if parent and hasattr(parent, 'team1_label'):
            self.team1_edit.setText(parent.team1_label.text())
        teams_layout.addRow("Команда 1:", self.team1_edit)

        self.team2_edit = QLineEdit()
        if parent and hasattr(parent, 'team2_label'):
            self.team2_edit.setText(parent.team2_label.text())
        teams_layout.addRow("Команда 2:", self.team2_edit)

        teams_group.setLayout(teams_layout)
        main_layout.addWidget(teams_group)

        # Группа "Настройки времени"
        time_group = QGroupBox("Настройки времени")
        time_layout = QFormLayout()

        self.minutes_edit = QSpinBox()
        self.minutes_edit.setRange(0, 59)
        if parent and hasattr(parent, 'initial_time'):
            self.minutes_edit.setValue(parent.initial_time // 60)
        time_layout.addRow("Минуты:", self.minutes_edit)

        self.seconds_edit = QSpinBox()
        self.seconds_edit.setRange(0, 59)
        if parent and hasattr(parent, 'initial_time'):
            self.seconds_edit.setValue(parent.initial_time % 60)
        time_layout.addRow("Секунды:", self.seconds_edit)

        time_group.setLayout(time_layout)
        main_layout.addWidget(time_group)

        # Кнопки управления
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(10)

        self.save_btn = QPushButton("Сохранить все настройки")
        self.save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(btn_layout)

    def save_settings(self):
        """Сохраняет все настройки"""
        parent = self.parent()
        if parent:
            # Сохраняем названия команд
            if hasattr(parent, 'team1_label'):
                parent.team1_label.setText(self.team1_edit.text())
            if hasattr(parent, 'team2_label'):
                parent.team2_label.setText(self.team2_edit.text())

            # Сохраняем время
            if hasattr(parent, 'initial_time'):
                parent.initial_time = self.minutes_edit.value() * 60 + self.seconds_edit.value()

            # Здесь можно добавить сохранение других параметров

        self.accept()  # Закрываем окно с результатом Accepted
