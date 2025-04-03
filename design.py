from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QFrame,
    QGraphicsDropShadowEffect,
    QInputDialog,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Arena")
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        MainWindow.showFullScreen()

        # Главный контейнер (фон)
        self.central_widget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.central_widget)

        # Устанавливаем фон через стиль
        self.central_widget.setStyleSheet(
            "QWidget {"
            "background-image: url(background.jpg);"
            "background-position: center;"
            "background-repeat: no-repeat;"
            "background-size: cover;"
            "}"
        )

        # Основной layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Прозрачный виджет для UI
        self.ui_widget = QWidget(self.central_widget)
        self.ui_widget.setAttribute(Qt.WA_TranslucentBackground)
        self.main_layout.addWidget(self.ui_widget)

        # Layout для интерфейса
        self.ui_layout = QVBoxLayout(self.ui_widget)
        self.ui_layout.setContentsMargins(0, 0, 0, 0)

        # Запрашиваем количество команд и их названия
        self.team_names, self.preparation_time = self.get_team_names_and_time()

        # Выбираем layout
        if len(self.team_names) == 1:
            central_layout = QVBoxLayout()
        else:
            central_layout = QHBoxLayout()
        central_layout.setAlignment(Qt.AlignCenter)
        central_layout.setContentsMargins(0, 0, 0, 0)

        # Фрейм для команды 1 (Красные)
        self.team1_frame = QFrame(self.ui_widget)
        self.team1_frame.setStyleSheet(
            """
            QFrame {
                background: qradialgradient(cx:0.5, cy:0.5, radius:1,
                    stop:0 rgba(255, 0, 0, 0.8),
                    stop:1 rgba(0, 0, 0, 0.5));
                border-radius: 15px;
            }
            """
        )
        self.team1_frame.setFixedSize(400, 150)
        central_layout.addWidget(self.team1_frame, alignment=Qt.AlignCenter)

        team1_layout = QVBoxLayout(self.team1_frame)
        self.team1_label = QLabel(self.team_names[0])
        self.team1_label.setFont(QFont("Bebas Neue", 40, QFont.Bold))
        self.team1_label.setStyleSheet("color: white; background: transparent;")
        self.team1_label.setAlignment(Qt.AlignCenter)
        team1_layout.addWidget(self.team1_label)

        # Фрейм для таймера (серый фон)
        self.timer_frame = QFrame(self.ui_widget)
        self.timer_frame.setStyleSheet(
            """
            QFrame {
                background-color: rgba(50, 50, 50, 0.8);
                border-radius: 20px;
            }
            """
        )
        self.timer_frame.setMinimumSize(650, 400)
        self.timer_frame.setMaximumSize(800, 500)
        central_layout.addWidget(self.timer_frame, alignment=Qt.AlignCenter)

        # Тень для таймера
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QtGui.QColor(0, 0, 0, 150))
        self.timer_frame.setGraphicsEffect(shadow)

        # Layout для таймера
        timer_frame_layout = QVBoxLayout(self.timer_frame)
        self.time_label = QLabel("00:00")
        self.time_label.setFont(QFont("Bebas Neue", 120))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("color: white; background: transparent;")
        timer_frame_layout.addWidget(self.time_label)

        # Фрейм для команды 2 (Синие)
        if len(self.team_names) > 1:
            self.team2_frame = QFrame(self.ui_widget)
            self.team2_frame.setStyleSheet(
                """
                QFrame {
                    background: qradialgradient(cx:0.5, cy:0.5, radius:1,
                        stop:0 rgba(0, 0, 255, 0.8),
                        stop:1 rgba(0, 0, 0, 0.5));
                    border-radius: 15px;
                }
                """
            )
            self.team2_frame.setFixedSize(400, 150)
            central_layout.addWidget(self.team2_frame, alignment=Qt.AlignCenter)

            team2_layout = QVBoxLayout(self.team2_frame)
            self.team2_label = QLabel(self.team_names[1])
            self.team2_label.setFont(QFont("Bebas Neue", 40, QFont.Bold))
            self.team2_label.setStyleSheet("color: white; background: transparent;")
            self.team2_label.setAlignment(Qt.AlignCenter)
            team2_layout.addWidget(self.team2_label)

        # Добавляем центральный layout
        self.ui_layout.addLayout(central_layout)

        # Таймер обновления
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

    def get_team_names_and_time(self):
        """Запрашивает у пользователя количество команд и их названия"""
        team_count, ok = QInputDialog.getInt(None, "Количество команд", "Введите количество команд (1 или 2):", 2, 1, 2)

        if ok:
            team_names = []
            for i in range(team_count):
                name, ok = QInputDialog.getText(None, f"Название команды {i + 1}", f"Введите название команды {i + 1}:")
                team_names.append(name if ok and name else f"Команда {i + 1}")

            time_options = ["3 минуты", "7 минут"]
            time_index, ok = QInputDialog.getItem(None, "Время подготовки", "Выберите время подготовки:", time_options)
            preparation_time = 3 if time_index == "3 минуты" else 7

            return team_names, preparation_time

        return ["Красные", "Синие"], 3

    def update_timer(self):
        """Обновляет отображение таймера (логика таймера может быть добавлена здесь)"""
        self.time_label.setText("00:00")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Arena"))
