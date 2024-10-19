from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QFrame,
    QGraphicsDropShadowEffect,
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Arena")

        # Устанавливаем стиль без рамки
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)

        # Разворачиваем окно на весь экран
        MainWindow.showFullScreen()

        # Создаем центральный виджет
        self.central_widget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.central_widget)

        # Создаем QLabel для фона
        self.background_label = QLabel(self.central_widget)
        self.background_label.setPixmap(QPixmap("background.jpg"))
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, MainWindow.width(), MainWindow.height())

        # Основной layout
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы

        # Создаем горизонтальный layout для команд и таймера
        central_layout = QHBoxLayout()
        central_layout.setAlignment(Qt.AlignCenter)
        central_layout.setContentsMargins(0, 0, 0, 0)  # Отступы слева и справа

        # Фоновый фрейм для команды 1 (Красные)
        team1_frame = QFrame()
        team1_frame.setStyleSheet(
            """
            QFrame {
                background: qradialgradient(cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, 
                    stop:0 rgba(255, 0, 0, 0.8), 
                    stop:1 rgba(0, 0, 0, 0.5));
                border-radius: 15px;
                padding: 10px;
                border: none; /* Убираем рамку */
            }
            """
        )
        team1_frame.setFixedSize(400, 150)
        central_layout.addWidget(team1_frame, alignment=Qt.AlignLeft)

        # Создаем вертикальный layout для команды 1
        team1_layout = QVBoxLayout(team1_frame)
        team1_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы

        self.team1_label = QLabel("Красные", self.central_widget)
        self.team1_label.setFont(
            QFont("Bebas Neue", 40, QFont.Bold)
        )  # Спортивный шрифт
        self.team1_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.8); background: transparent;"
        )
        self.team1_label.setAlignment(Qt.AlignCenter)

        # Эффект тени для текста команды
        team_shadow_effect = QGraphicsDropShadowEffect()
        team_shadow_effect.setBlurRadius(15)
        team_shadow_effect.setColor(QtGui.QColor(0, 0, 0, 160))
        team_shadow_effect.setOffset(5, 5)
        self.team1_label.setGraphicsEffect(team_shadow_effect)

        team1_layout.addWidget(self.team1_label)

        # Таймер (по центру)
        self.timer_frame = QFrame()
        self.timer_frame.setStyleSheet(
            """
            QFrame {
                background-color: rgba(0, 0, 0, 0.7);
                border-radius: 20px;
                padding: 30px;
                border: none; /* Убираем рамку */
            }
            """
        )
        self.timer_frame.setFixedSize(630, 340)
        central_layout.addWidget(self.timer_frame, alignment=Qt.AlignCenter)

        timer_frame_layout = QVBoxLayout(self.timer_frame)

        self.time_label = QLabel(self.central_widget)
        self.time_label.setFont(QFont("Bebas Neue", 120))  # Спортивный шрифт
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.8); background: transparent;"
        )
        self.time_label.setFixedSize(550, 250)
        self.time_label.setWordWrap(True)

        # Эффект тени для таймера
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(30)
        shadow_effect.setColor(QtGui.QColor(0, 0, 0, 200))
        shadow_effect.setOffset(6, 6)
        self.time_label.setGraphicsEffect(shadow_effect)

        timer_frame_layout.addWidget(self.time_label)

        # Фоновый фрейм для команды 2 (Синие)
        team2_frame = QFrame()
        team2_frame.setStyleSheet(
            """
            QFrame {
                background: qradialgradient(cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, 
                    stop:0 rgba(0, 0, 255, 0.8), 
                    stop:1 rgba(0, 0, 0, 0.5));
                border-radius: 15px;
                padding: 10px;
                border: none; /* Убираем рамку */
            }
            """
        )
        team2_frame.setFixedSize(400, 150)
        central_layout.addWidget(team2_frame, alignment=Qt.AlignRight)

        # Создаем вертикальный layout для команды 2
        team2_layout = QVBoxLayout(team2_frame)
        team2_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы

        self.team2_label = QLabel("Синие", self.central_widget)
        self.team2_label.setFont(
            QFont("Bebas Neue", 40, QFont.Bold)
        )  # Спортивный шрифт
        self.team2_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.8); background: transparent;"
        )
        self.team2_label.setAlignment(Qt.AlignCenter)

        # Эффект тени для текста команды
        team_shadow_effect = QGraphicsDropShadowEffect()
        team_shadow_effect.setBlurRadius(15)
        team_shadow_effect.setColor(QtGui.QColor(0, 0, 0, 160))
        team_shadow_effect.setOffset(5, 5)
        self.team2_label.setGraphicsEffect(team_shadow_effect)

        team2_layout.addWidget(self.team2_label)

        # Добавляем горизонтальный макет на основной
        main_layout.addLayout(central_layout)

        # Таймер
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

        # Анимация изменения цвета
        self.color_animation = QPropertyAnimation(self.time_label, b"styleSheet")
        self.color_animation.setDuration(3000)  # Время анимации 3 секунды
        self.color_animation.setLoopCount(-1)  # Бесконечная анимация
        self.color_animation.setStartValue(
            "color: rgba(255, 255, 255, 0.8); background: transparent;"
        )
        self.color_animation.setEndValue(
            "color: rgba(255, 165, 0, 0.8); background: transparent;"
        )

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Arena"))
