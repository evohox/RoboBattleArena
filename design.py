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
from PyQt5.QtCore import QTimer, Qt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Arena")  # Устанавливаем имя для главного окна
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)  # Убираем рамки у окна
        MainWindow.showFullScreen()  # Разворачиваем окно на весь экран

        self.central_widget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.central_widget)

        # Устанавливаем фоновое изображение
        self.background_label = QLabel(self.central_widget)
        self.background_label.setPixmap(QPixmap("background.jpg"))
        self.background_label.setScaledContents(True)  # Масштабируем изображение
        self.background_label.setGeometry(0, 0, MainWindow.width(), MainWindow.height())

        # Основной layout для центрального виджета
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы

        # Горизонтальный layout для команд и таймера
        central_layout = QHBoxLayout()
        central_layout.setAlignment(Qt.AlignCenter)  # Выравнивание по центру
        central_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы

        # Фрейм для команды 1 (Красные)
        team1_frame = QFrame()
        team1_frame.setStyleSheet(
            """
            QFrame {
                background: qradialgradient(cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, 
                    stop:0 rgba(255, 0, 0, 0.8), 
                    stop:1 rgba(0, 0, 0, 0.5));
                border-radius: 15px;  /* Закругление углов */
                padding: 10px;  /* Отступы внутри фрейма */
                border: none;  /* Убираем рамку */
            }
        """
        )
        team1_frame.setFixedSize(400, 150)  # Устанавливаем фиксированный размер
        central_layout.addWidget(
            team1_frame, alignment=Qt.AlignLeft
        )  # Добавляем фрейм в layout

        # Вертикальный layout для команды 1
        team1_layout = QVBoxLayout(team1_frame)
        team1_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы

        # Метка для названия команды 1
        self.team1_label = QLabel("Красные", self.central_widget)
        self.team1_label.setFont(
            QFont("Bebas Neue", 40, QFont.Bold)
        )  # Устанавливаем шрифт
        self.team1_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.8); background: transparent;"
        )
        self.team1_label.setAlignment(Qt.AlignCenter)  # Центрируем текст

        # Эффект тени для текста команды
        team_shadow_effect = QGraphicsDropShadowEffect()
        team_shadow_effect.setBlurRadius(15)
        team_shadow_effect.setColor(QtGui.QColor(0, 0, 0, 160))
        team_shadow_effect.setOffset(5, 5)
        self.team1_label.setGraphicsEffect(team_shadow_effect)  # Применяем эффект

        team1_layout.addWidget(self.team1_label)  # Добавляем метку в layout команды 1

        # Фрейм для таймера
        self.timer_frame = QFrame()
        self.timer_frame.setStyleSheet(
            """
            QFrame {
                background-color: rgba(0, 0, 0, 0.7);
                border-radius: 20px;  /* Закругление углов */
                padding: 30px;  /* Отступы внутри фрейма */
                border: none;  /* Убираем рамку */
            }
        """
        )
        self.timer_frame.setFixedSize(630, 340)  # Устанавливаем фиксированный размер
        central_layout.addWidget(
            self.timer_frame, alignment=Qt.AlignCenter
        )  # Добавляем таймер

        timer_frame_layout = QVBoxLayout(
            self.timer_frame
        )  # Вертикальный layout для таймера

        # Метка для отображения времени
        self.time_label = QLabel(self.central_widget)
        self.time_label.setFont(QFont("Bebas Neue", 120))  # Устанавливаем шрифт
        self.time_label.setAlignment(Qt.AlignCenter)  # Центрируем текст
        self.time_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.8); background: transparent;"
        )
        self.time_label.setFixedSize(550, 250)  # Устанавливаем фиксированный размер
        self.time_label.setWordWrap(True)  # Включаем перенос слов

        # Эффект тени для таймера
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(30)
        shadow_effect.setColor(QtGui.QColor(0, 0, 0, 200))
        shadow_effect.setOffset(6, 6)
        self.time_label.setGraphicsEffect(shadow_effect)  # Применяем эффект

        timer_frame_layout.addWidget(
            self.time_label
        )  # Добавляем метку времени в layout таймера

        # Фрейм для команды 2 (Синие)
        team2_frame = QFrame()
        team2_frame.setStyleSheet(
            """
            QFrame {
                background: qradialgradient(cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, 
                    stop:0 rgba(0, 0, 255, 0.8), 
                    stop:1 rgba(0, 0, 0, 0.5));
                border-radius: 15px;  /* Закругление углов */
                padding: 10px;  /* Отступы внутри фрейма */
                border: none;  /* Убираем рамку */
            }
        """
        )
        team2_frame.setFixedSize(400, 150)  # Устанавливаем фиксированный размер
        central_layout.addWidget(
            team2_frame, alignment=Qt.AlignRight
        )  # Добавляем фрейм в layout

        # Вертикальный layout для команды 2
        team2_layout = QVBoxLayout(team2_frame)
        team2_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы

        # Метка для названия команды 2
        self.team2_label = QLabel("Синие", self.central_widget)
        self.team2_label.setFont(
            QFont("Bebas Neue", 40, QFont.Bold)
        )  # Устанавливаем шрифт
        self.team2_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.8); background: transparent;"
        )
        self.team2_label.setAlignment(Qt.AlignCenter)  # Центрируем текст

        # Эффект тени для текста команды
        team_shadow_effect = QGraphicsDropShadowEffect()
        team_shadow_effect.setBlurRadius(15)
        team_shadow_effect.setColor(QtGui.QColor(0, 0, 0, 160))
        team_shadow_effect.setOffset(5, 5)
        self.team2_label.setGraphicsEffect(team_shadow_effect)  # Применяем эффект

        team2_layout.addWidget(self.team2_label)  # Добавляем метку в layout команды 2

        # Добавляем горизонтальный layout на основной
        main_layout.addLayout(central_layout)

        # Настройка таймера
        self.timer = QTimer()
        self.timer.setInterval(1000)  # Устанавливаем интервал таймера (1 секунда)
        self.timer.timeout.connect(
            self.update_timer
        )  # Подключаем событие обновления таймера

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate  # Утилита для перевода текста
        MainWindow.setWindowTitle(
            _translate("MainWindow", "Arena")
        )  # Устанавливаем заголовок окна
