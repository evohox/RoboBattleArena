from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QSpinBox,
)


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Настройки")
        self.setFixedSize(900, 200)

        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.team1_edit = QLineEdit(self)
        self.team1_edit.setText(parent.team1_label.text())
        self.team2_edit = QLineEdit(self)
        self.team2_edit.setText(parent.team2_label.text())

        # Отдельные спинбоксы для минут и секунд
        self.minutes_edit = QSpinBox(self)
        self.minutes_edit.setRange(0, 59)  # Диапазон минут от 0 до 59
        self.minutes_edit.setValue(
            parent.initial_time // 60
        )  # Устанавливаем текущие минуты

        self.seconds_edit = QSpinBox(self)
        self.seconds_edit.setRange(0, 59)  # Диапазон секунд от 0 до 59
        self.seconds_edit.setValue(
            parent.initial_time % 60
        )  # Устанавливаем текущие секунды

        form_layout.addRow("Команда 1:", self.team1_edit)
        form_layout.addRow("Команда 2:", self.team2_edit)
        form_layout.addRow("Минуты:", self.minutes_edit)
        form_layout.addRow("Секунды:", self.seconds_edit)

        layout.addLayout(form_layout)

        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

    def save_settings(self):
        self.accept()  # Закрыть диалоговое окно и вернуть результат
