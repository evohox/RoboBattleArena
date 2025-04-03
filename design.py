from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QFrame,
    QGraphicsDropShadowEffect,
    QInputDialog,
    QStackedLayout,
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QTimer, Qt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Arena")
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        MainWindow.showFullScreen()

        # Создаем главный виджет с StackedLayout
        self.central_widget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.central_widget)

        # StackedLayout позволит нам наложить элементы поверх фона
        self.stacked_layout = QStackedLayout(self.central_widget)
        self.stacked_layout.setStackingMode(QStackedLayout.StackAll)

        # 1. Слой с фоном
        self.background_widget = QWidget()
        self.background_widget.setLayout(QVBoxLayout())
        self.background_widget.layout().setContentsMargins(0, 0, 0, 0)

        self.background_label = QLabel(self.background_widget)
        self.background_label.setPixmap(QPixmap("background.jpg"))
        self.background_label.setScaledContents(True)
        self.background_widget.layout().addWidget(self.background_label)

        # 2. Слой с основным интерфейсом
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Добавляем оба слоя в stacked layout
        self.stacked_layout.addWidget(self.background_widget)
        self.stacked_layout.addWidget(self.main_widget)

        # Запрашиваем количество команд и их названия
        self.team_names, self.preparation_time = self.get_team_names_and_time()

        # Проверяем количество команд и создаем соответствующий layout
        if len(self.team_names) == 1:
            # Если одна команда, используем вертикальный layout
            central_layout = QVBoxLayout()
            central_layout.setAlignment(Qt.AlignCenter)
        else:
            # Если две команды, используем горизонтальный layout
            central_layout = QHBoxLayout()
            central_layout.setAlignment(Qt.AlignCenter)

        central_layout.setContentsMargins(0, 0, 0, 0)

        # Фрейм для команды 1 (Красные)
        self.team1_frame = QFrame()
        self.team1_frame.setStyleSheet(
            """
            QFrame {
                background: qradialgradient(cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5,
                    stop:0 rgba(255, 0, 0, 0.8),
                    stop:1 rgba(0, 0, 0, 0.5));
                border-radius: 15px;
                padding: 10px;
                border: none;
            }
            """
        )
        self.team1_frame.setFixedSize(400, 150)
        central_layout.addWidget(self.team1_frame, alignment=Qt.AlignCenter)

        team1_layout = QVBoxLayout(self.team1_frame)
        team1_layout.setContentsMargins(0, 0, 0, 0)

        # Метка для названия команды 1
        self.team1_label = QLabel(self.team_names[0])
        self.team1_label.setFont(QFont("Bebas Neue", 40, QFont.Bold))
        self.team1_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.8); background: transparent;"
        )
        self.team1_label.setAlignment(Qt.AlignCenter)

        team_shadow_effect = QGraphicsDropShadowEffect()
        team_shadow_effect.setBlurRadius(15)
        team_shadow_effect.setColor(QtGui.QColor(0, 0, 0, 160))
        team_shadow_effect.setOffset(5, 5)
        self.team1_label.setGraphicsEffect(team_shadow_effect)

        team1_layout.addWidget(self.team1_label)

        # Таймер
        self.timer_frame = QFrame()
        self.timer_frame.setStyleSheet(
            """
            QFrame {
                background-color: rgba(0, 0, 0, 0.7);
                border-radius: 20px;
                padding: 30px;
                border: none;
            }
            """
        )
        self.timer_frame.setMinimumSize(630, 400)
        self.timer_frame.setMaximumSize(800, 600)
        central_layout.addWidget(self.timer_frame, alignment=Qt.AlignCenter)

        timer_frame_layout = QVBoxLayout(self.timer_frame)
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Bebas Neue", 120))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setMinimumSize(550, 0)
        self.time_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.8); background: transparent;"
        )
        self.time_label.setWordWrap(True)

        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(30)
        shadow_effect.setColor(QtGui.QColor(0, 0, 0, 200))
        shadow_effect.setOffset(6, 6)
        self.time_label.setGraphicsEffect(shadow_effect)

        timer_frame_layout.addWidget(self.time_label)

        # Фрейм для команды 2 (Синие)
        if len(self.team_names) > 1:
            self.team2_frame = QFrame()
            self.team2_frame.setStyleSheet(
                """
                QFrame {
                    background: qradialgradient(cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5,
                        stop:0 rgba(0, 0, 255, 0.8),
                        stop:1 rgba(0, 0, 0, 0.5));
                    border-radius: 15px;
                    padding: 10px;
                    border: none;
                }
                """
            )
            self.team2_frame.setFixedSize(400, 150)
            central_layout.addWidget(self.team2_frame, alignment=Qt.AlignCenter)

            team2_layout = QVBoxLayout(self.team2_frame)
            team2_layout.setContentsMargins(0, 0, 0, 0)

            # Метка для названия команды 2
            self.team2_label = QLabel(self.team_names[1])
            self.team2_label.setFont(QFont("Bebas Neue", 40, QFont.Bold))
            self.team2_label.setStyleSheet(
                "color: rgba(255, 255, 255, 0.8); background: transparent;"
            )
            self.team2_label.setAlignment(Qt.AlignCenter)

            team_shadow_effect = QGraphicsDropShadowEffect()
            team_shadow_effect.setBlurRadius(15)
            team_shadow_effect.setColor(QtGui.QColor(0, 0, 0, 160))
            team_shadow_effect.setOffset(5, 5)
            self.team2_label.setGraphicsEffect(team_shadow_effect)

            team2_layout.addWidget(self.team2_label)

        # Добавляем центральный layout на основной
        self.main_layout.addLayout(central_layout)

        # Устанавливаем обработчик изменения размера
        self.central_widget.resizeEvent = self.resizeEvent

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

    def resizeEvent(self, event):
        """Обработчик изменения размера окна"""
        # Обновляем размер фона
        self.background_label.setFixedSize(event.size())
        event.accept()

    def get_team_names_and_time(self):
        team_count, ok = QInputDialog.getInt(
            None, "Количество команд", "Введите количество команд (1 или 2):", 2, 1, 2
        )

        if ok:
            team_names = []
            for i in range(team_count):
                name, ok = QInputDialog.getText(
                    None,
                    f"Название команды {i + 1}",
                    f"Введите название команды {i + 1}:",
                )
                if ok and name:
                    team_names.append(name)
                else:
                    team_names.append(f"Команда {i + 1}")  # Название по умолчанию

            # Запрашиваем время подготовки
            time_options = ["3 минуты", "7 минут"]
            time_index, ok = QInputDialog.getItem(
                None, "Время подготовки", "Выберите время подготовки:", time_options
            )
            preparation_time = 3 if time_index == "3 минуты" else 7

            return team_names, preparation_time

        return ["Красные", "Синие"], 3  # Названия по умолчанию, если ввод отменен

    def set_preparation_time(self, minutes):
        self.preparation_time = minutes
        self.time_label.setText(f"Подготовка: {minutes} минут")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Arena"))
