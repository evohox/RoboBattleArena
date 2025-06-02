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
from QtWindow.settings import SettingsDialog


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Arena")
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        MainWindow.showFullScreen()

        self.team_update_timer = QTimer()
        self.team_update_timer.start(1000)

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
        self.main_layout.addWidget(self.ui_widget)

        # Layout для интерфейса
        self.ui_layout = QVBoxLayout(self.ui_widget)
        self.ui_layout.setContentsMargins(0, 0, 0, 0)

        # Запрашиваем количество команд и их названия
        self.team_names = ["Загрузка...", "Загрузка..."]
        self.preparation_time = 3

        # layout
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
        self.team1_frame.setFixedSize(500, 200)
        central_layout.addWidget(self.team1_frame, alignment=Qt.AlignCenter)

        team1_layout = QVBoxLayout(self.team1_frame)
        self.team1_label = QLabel(self.team_names[0])
        self.team1_label.setFont(QFont("Bebas Neue", 40, QFont.Bold))
        self.team1_label.setStyleSheet("color: white; background: transparent;")
        self.team1_label.setAlignment(Qt.AlignCenter)
        team1_layout.addWidget(self.team1_label)

        # Фрейм для таймера
        self.timer_frame = QFrame(self.ui_widget)
        self.timer_frame.setStyleSheet(
            """
            QFrame {
                background: qradialgradient(cx:0.5, cy:0.5, radius:1,
                    stop:0 rgba(0, 0, 0, 0.8),
                    stop:1 rgba(0, 0, 0, 0.5));
                border-radius: 15px;
            }
        # """
        )
        self.timer_frame.setMinimumSize(650, 400)
        self.timer_frame.setMaximumSize(900, 500)

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
        self.time_label.setStyleSheet(
            "color: rgba(255, 255, 255, 1); background: transparent;"
        )
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
            self.team2_frame.setFixedSize(500, 200)
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

    def show_settings_dialog(self):
        dialog = SettingsDialog(self)
        if dialog.exec_():
            self.team_names, self.preparation_time = dialog.get_settings()
            self.apply_settings()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Arena"))
