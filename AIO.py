import sys
import base64
import time
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QPushButton, QFileDialog, 
                             QMessageBox, QTabWidget, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRectF, QPoint
from PyQt5.QtGui import QFont, QPainter, QBrush, QColor, QPainterPath

class CustomWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)

        main_layout = QHBoxLayout(self)

        tabs_layout = QVBoxLayout()
        tabs_layout.setContentsMargins(0, 0, 0, 0)
        tabs_layout.setSpacing(10)

        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background: #2e2e2e;
                color: white;
                border-radius: 10px;
                min-width: 100px;
                min-height: 30px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background: #3e3e3e;
            }
        """)
        tabs_layout.addWidget(self.tab_widget)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        tabs_layout.addItem(spacer)

        main_layout.addLayout(tabs_layout)

        self.right_panel = QVBoxLayout()
        self.right_panel.setContentsMargins(10, 10, 10, 10)
        self.right_panel.setSpacing(10)
        main_layout.addLayout(self.right_panel)

        self.webhook_sender_tab = QWidget()
        self.webhook_sender_layout = QVBoxLayout(self.webhook_sender_tab)
        self.tab_widget.addTab(self.webhook_sender_tab, "Webhook Sender/Scam troller")
        self.setup_webhook_sender()

        self.webhook_admin_tab = QWidget()
        self.webhook_admin_layout = QVBoxLayout(self.webhook_admin_tab)
        self.tab_widget.addTab(self.webhook_admin_tab, "ultimate scammer troll")
        self.setup_webhook_admin()

        self.credits_tab = QWidget()
        self.credits_layout = QVBoxLayout(self.credits_tab)
        self.tab_widget.addTab(self.credits_tab, "Credits/thewhitehatguythatmadethis")
        self.setup_credits_tab()

        self.spam_webhook_tab = QWidget()
        self.spam_webhook_layout = QVBoxLayout(self.spam_webhook_tab)
        self.tab_widget.addTab(self.spam_webhook_tab, "Spam scammers")
        self.setup_spam_webhook()

        self.change_webhook_name_tab = QWidget()
        self.change_webhook_name_layout = QVBoxLayout(self.change_webhook_name_tab)
        self.tab_widget.addTab(self.change_webhook_name_tab, "Change Webhook Name")
        self.setup_change_webhook_name()

        self.send_messages_x_times_tab = QWidget()
        self.send_messages_x_times_layout = QVBoxLayout(self.send_messages_x_times_tab)
        self.tab_widget.addTab(self.send_messages_x_times_tab, "Send Messages unlimited Times")
        self.setup_send_messages_x_times()


        self.setLayout(main_layout)

    def setup_webhook_sender(self):
        webhook_url_label = QLabel("Webhook URL:")
        webhook_url_label.setStyleSheet("color: white;")
        self.webhook_url_input = QLineEdit()
        self.webhook_url_input.setStyleSheet("background-color: #2e2e2e; color: white; border: none; border-radius: 5px; padding: 5px;")

        message_label = QLabel("Message:")
        message_label.setStyleSheet("color: white;")
        self.message_input = QTextEdit()
        self.message_input.setStyleSheet("background-color: #2e2e2e; color: white; border: none; border-radius: 5px; padding: 5px;")

        file_button = QPushButton("Attach File")
        file_button.setStyleSheet("background-color: #3e3e3e; color: white; border: none; border-radius: 5px; padding: 5px;")
        file_button.clicked.connect(self.attach_file)

        send_button = QPushButton("Send")
        send_button.setStyleSheet("background-color: #3e3e3e; color: white; border: none; border-radius: 5px; padding: 5px;")
        send_button.clicked.connect(self.send_webhook)

        delay_label = QLabel("Delay (seconds):")
        delay_label.setStyleSheet("color: white;")
        self.delay_input = QLineEdit()
        self.delay_input.setStyleSheet("background-color: #2e2e2e; color: white; border: none; border-radius: 5px; padding: 5px;")

        self.webhook_sender_layout.addWidget(webhook_url_label)
        self.webhook_sender_layout.addWidget(self.webhook_url_input)
        self.webhook_sender_layout.addWidget(message_label)
        self.webhook_sender_layout.addWidget(self.message_input)
        self.webhook_sender_layout.addWidget(file_button)
        self.webhook_sender_layout.addWidget(delay_label)
        self.webhook_sender_layout.addWidget(self.delay_input)
        self.webhook_sender_layout.addWidget(send_button)

    def setup_webhook_admin(self):
        delete_button = QPushButton("Delete Webhook")
        delete_button.setStyleSheet("background-color: #3e3e3e; color: white; border: none; border-radius: 5px; padding: 5px;")
        delete_button.clicked.connect(self.delete_webhook)

        self.webhook_admin_layout.addWidget(delete_button)

    def setup_credits_tab(self):
        credits_text = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡶⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⣺⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⡰⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢯⡢⢄⠀⠀⠀⠀⠀⠀⡰⣹⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⡪⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⢿⣾⣶⣶⣦⣤⣤⣊⣴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢔⡥⠋⠀⢀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣥⠎⠀⠀⠈⠉⠉⠙⠛⣷⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⣒⡽⠋⠀⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢺⡿⠁⠀⠀⠀⠀⠀⠀⣠⣪⡴⠿⢷⣄⠀⠀⠀⠀⠀⣠⠖⣡⡞⣉⣤⡴⢖⣿⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⣷⡟⠀⠀⠀⠀⠀⢀⣤⠞⠋⠀⠀⠀⠀⢹⠻⣦⣄⠒⠊⣠⣾⡯⠗⠛⠁⡠⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⣴⡿⠋⠀⠀⠀⠀⡀⠔⠋⠀⠀⠀⠀⠀⠀⠀⠈⣇⠀⠉⠛⠿⣿⡧⣀⠀⢀⣴⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⡄⠀⠀⠀⢀⣾⡟⠁⠀⠀⠀⠀⡖⠀⠀⠀⠀⠀⠀⢰⠀⠀⠀⠀⢹⢆⠀⠀⠀⠈⠙⢦⣑⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣄⠀⢀⣾⠏⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⢀⣀⣨⣦⣤⣐⣊⣿⣸⣿⣆⣤⣀⣠⡾⠛⠳⣭⡢⡀⠀⠀⠀⠀⠀⠀⠀⣾⠁⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣄⠀⠀⠀⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⢫⠳⣿⠃⠀⠠⠤⣤⣤⣤⢯⣂⣶⣶⡽⠿⠷⠛⠛⣿⡋⠉⠉⣩⠏⠉⠉⣻⣟⠽⣶⣤⡀⠀⠙⠻⣖⣄⠀⠀⠀⠀⢰⡿⠀⠀⠀⠀⠀⢀⣤⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡆⠀⠀⣿⢃⠈⠢⣄⠀⠀⠀⠀⠀⠈⣷⡙⢀⡠⢔⣸⠟⠋⢩⡾⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⣠⡾⠁⠀⠀⡼⠛⡇⠀⠀⠈⠻⣦⣄⠀⠈⠙⠳⣤⡀⠀⣸⡇⠀⠀⠀⠀⢀⣮⠏⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⡄⠀⣿⠸⠀⠀⠈⢿⡢⢀⠀⠀⠀⣹⣻⣽⠞⠋⠀⠀⠀⡎⡇⠀⠀⠀⠀⠀⠀⠀⠀⢀⢿⣿⣥⣤⣶⣖⣤⣤⣿⣀⠀⠀⠀⠈⠓⠷⣠⡀⠀⠈⠺⢶⣷⠀⠀⠀⢀⡴⡟⣿⠀⠀⠀⠀⠀⠀⢀⣤⠖⠉⠀⠀⠀⠀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣄⢸⡇⠀⠀⠀⡤⠙⢶⣷⡶⣾⡞⠋⠀⠀⠀⠀⠀⣰⣷⢔⣢⣭⣭⣭⢽⣷⣦⡴⣡⡞⣿⣿⣽⣶⣿⣿⡿⣿⣿⡟⡻⣷⣄⠀⠀⠈⠑⠻⢦⣤⣼⣾⡆⢀⣴⠟⢠⣽⠇⠀⠀⠀⢀⣤⣾⠛⠁⠀⠀⠀⠀⠀⢰⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢯⣾⣧⠀⠀⣰⠋⡳⣾⣿⡋⠁⠙⢶⢄⢀⣤⠶⢻⣿⡿⠮⣥⣿⣾⣿⣿⣿⡿⠷⠿⠭⢽⣿⣯⡑⠷⠾⢿⣿⣻⣿⢿⣯⣿⢿⣦⣄⠀⠀⠀⢈⣏⠿⣿⣟⡁⠀⣸⡏⠀⠀⣠⣴⡿⠊⠀⠀⠀⠀⠀⠀⠀⠀⣾⠃⢀⣠⡶⠂⠀⠀⠀⠀⢠⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⠀⢠⣿⡮⠟⡏⡟⠻⢵⣢⠄⣘⣟⣿⣦⣿⣿⣷⣿⣯⣩⣭⠴⠶⠖⠒⠋⠉⣉⡉⢻⣻⠙⠻⠷⢶⣎⣉⣉⣛⣿⣿⡿⠿⠿⣷⣦⣀⣼⣼⡾⣿⡏⠻⣷⣿⣇⣤⡾⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⠾⠋⠁⠀⠀⠀⠀⠀⣰⠏⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⣤⣴⣦⣶⠂⠐⣶⠒⢺⣿⣧⢻⠋⠀⠀⡇⢳⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⠛⠋⢸⡟⣥⠀⠒⢲⣶⣿⣯⣴⡖⠛⣧⣿⠛⠛⠛⢻⣿⢻⣿⣿⣿⣿⣿⣷⣶⣶⣮⣽⣯⣶⣽⡇⠀⣾⣿⢻⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⢠⣴⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠙⠛⣿⣿⡌⠀⠀⠀⠸⣼⣄⣤⣶⣿⣿⣿⣿⠿⢿⣻⣦⣼⠿⠛⠋⠉⢉⣉⣀⣨⣥⣴⣲⠾⠿⠾⠿⠷⢿⣿⣿⡭⣿⣿⣿⣭⣝⣯⣭⣽⣭⣥⣭⣭⣭⣟⣯⣿⣷⣾⣿⣄⣀⣀⡀⠀⠀⣀⣤⡶⠛⢁⢾⠏⠀⠀⠀⠀⠀⠀⢀⣾⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠢⡀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⣽⡟⠀⠀⠀⠀⣠⣿⣛⣩⡾⢿⣿⣾⢿⣿⣿⣷⣛⣻⣷⠶⠾⠿⠟⠛⠋⠉⠉⠁⠀⠀⠀⢀⣠⡾⠛⢻⣿⣿⣟⠻⣿⣿⣿⣿⣿⣿⣿⣿⣟⢯⡻⣍⡉⠙⣿⣿⣍⡓⠿⣿⣿⣶⢞⠟⠁⠀⢀⢾⡏⠀⠀⠀⠀⠀⠀⣠⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⢦⣄⡀⠀⠐⠢⡀⠀⠀⠀⠀⠀⠀⣴⣚⣟⣳⣶⠬⡿⣻⠿⠛⣿⣿⣿⣿⣿⣿⣿⢟⣿⡿⠋⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠞⠋⠁⠐⠚⠉⠀⠙⢿⣄⠉⢻⣾⣿⣿⣟⣿⣿⣿⣷⣿⣦⣻⣦⡘⣷⣍⠛⢷⣬⣙⠻⡁⠀⠀⢀⣼⡟⠀⠀⠀⠀⠀⢀⣜⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢮⣑⠤⡀⠙⢶⣄⠀⠀⠀⠀⢹⣻⠃⠀⣠⣺⠟⠁⢀⣼⣿⢿⣿⣿⣿⡿⢁⣿⠟⡀⠀⠀⢰⠃⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣦⣌⣿⠻⣿⣿⣿⣶⣍⠻⢿⣿⣿⣿⡿⣿⣿⣿⣦⣈⡛⠿⣮⣵⣖⣊⣿⠁⠀⢀⡀⠀⣠⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣓⠤⡙⢧⡢⢄⠀⢸⣿⣠⣾⠟⣉⡀⠤⣾⣿⣿⣿⣿⣿⠟⢀⡾⠃⠊⠀⠀⢠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⣿⣦⡹⣿⣿⣿⣿⣿⣷⣪⢙⠿⢿⣾⣿⡁⠙⠻⣯⡲⢞⠛⠽⢿⣟⡫⡉⠀⣀⣾⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣚⣷⣽⣶⣭⡒⢿⣿⣿⣿⣶⠶⣿⣿⡟⣵⣿⡿⠊⣠⡿⠉⠀⠀⢀⣤⢄⣠⢤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠔⢜⠞⠗⠲⠤⢄⡀⠀⠀⠀⠀⠈⠙⢮⣻⣿⣿⣿⣿⣿⣷⣵⣄⢻⢿⣷⣄⠀⠘⣿⣦⡧⠀⠀⠙⢷⣬⣶⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡼⠿⠿⣿⣿⠟⣠⡿⠛⠋⠁⢀⣼⣿⡿⢼⣿⡿⢁⣼⠛⢀⣴⣶⣿⣽⣦⣤⡥⠒⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠖⠸⠄⠀⠐⠀⠤⠬⠛⠿⣶⣢⣄⠀⠀⠈⢳⡹⣿⣿⣿⣿⣿⣿⣿⣷⣝⢿⣿⣷⣴⣿⡿⠁⠀⠀⠀⠀⢿⡜⣧⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣶⠾⠿⠟⠻⠯⣅⣰⣏⣰⣙⣄⢀⣴⣮⣿⣿⣿⠃⣿⣿⣧⡿⡡⣴⠷⠛⠉⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣀⣀⣀⠀⠀⠀⠘⠑⠄⠀⠀⢷⣻⣿⣽⣿⣿⣿⣿⣿⣿⣧⡹⣿⣿⣿⣿⣷⢦⡀⠀⠀⠘⣿⡏⠙⠷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣀⣠⣔⣆⡬⠿⠛⠉⠉⠁⠀⠀⠀⠀⠀⠀⢹⣿⣿⠟⠈⠙⢿⣿⠟⢹⣽⣿⣾⣿⣿⣿⠝⠁⠀⠀⠀⣄⣀⡀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⢿⡯⣿⣿⢷⣾⢿⣶⣄⠀⠀⠀⠀⠀⢸⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⢻⣿⣿⣿⣶⣿⡆⣀⣠⣿⣿⢀⣀⣀⣙⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠠⠄⠒⠚⠉⠉⠉⠁⠀⠀⠀⠈⠑⠒⠒⠚⠓⠻⠿⣦⣤⣾⢻⡿⣦⣀⢀⣾⠏⢀⣿⣿⣿⣿⣿⣿⡇⠀⠀⢠⣶⣿⣿⣿⣿⢧⡞⣄⠀⠀⢠⡇⠀⠀⠀⠀⠀⢆⣁⡶⠟⣩⠏⠀⠛⠿⠟⠹⠀⠙⢯⣳⡄⠀⠀⠀⠘⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⢿⣿⣿⣯⢿⣿⡿⠿⠛⠛⠋⠉⠉⠉⠉⠈⠑⠦⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡸⣿⠛⠿⣿⡏⠀⡟⣽⣿⣿⣿⣿⣿⠂⠀⣰⣿⠻⡟⠻⡟⢻⠀⠛⣤⣑⣨⠏⠀⠀⠀⠀⠀⡀⠀⠐⡖⡟⠭⠤⠤⣄⠈⠉⠀⣀⠀⡾⢯⡱⠀⠀⠀⠀⢻⣷⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⠈⣿⣿⣿⣿⣧⣵⣂⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠦⣀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣇⢻⡄⢠⣿⠁⢸⢷⣿⣿⢯⣿⣿⣿⠀⢠⣿⣽⢀⠌⢚⠛⠁⠐⠣⠉⡫⢃⠀⠀⠀⠀⠀⠀⠘⢄⠀⠀⢹⣢⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⢸⣿⡏⠹⣿⣿⣿⣿⣿⣇⣟⣿⣿⠖⢿⣿⣿⣿⣿⠿⢿⣭⣙⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⡤⢪⡿⠉⡀⢷⣴⣿⢀⣾⠈⣿⣿⣾⣿⡟⣿⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠎⢀⠀⠀⠀⠀⠀⠀⠈⢆⠀⠀⠀⠉⠢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢃⡁⢻⣿⣿⣿⣿⢫⣾⡿⠏⠀⣹⣿⣿⣿⢘⠄⠈⠒⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠒⠒⠚⠛⠛⠛⠛⠛⢛⣿⣷⠟⠀⢸⣧⠈⣟⣿⣿⣿⣦⢹⣿⣿⣿⣯⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⡔⣡⡀⠀⠀⢀⣥⡀⠀⠈⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⠰⣄⢹⣿⣿⣿⢧⣿⡟⠁⡜⣼⣿⣿⣿⢿⣞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⠤⠶⢻⡿⠃⠀⠀⢠⣻⠑⡘⢻⣿⢻⣿⣆⢻⣿⣿⣧⢰⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢰⣿⡇⠀⠀⠘⠻⣿⣦⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡃⠀⢻⣾⣿⣿⡿⣿⣿⠃⢠⣷⣿⣿⣿⣿⣧⢿⣖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⡀⠤⠴⠒⠋⠉⠀⠀⠀⣠⡴⠋⠀⠀⠀⠀⠸⡿⣄⢐⢄⣷⢾⢻⣿⡎⣿⣿⡟⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠟⢀⡀⠀⡀⣄⣛⠁⠀⡸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⣿⣿⣿⣿⡏⣿⢰⣼⣿⣿⣿⣿⣿⣿⣏⠾⣧⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⠋⠀⠀⠀⠀⠀⠀⡐⣿⠾⠿⠷⢿⣾⣞⣿⣟⣿⣿⠇⣾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡎⣠⣶⣇⣿⣿⣽⣮⢻⣿⣔⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⢽⣿⣿⡿⣷⡇⣰⣿⣿⣿⣿⣿⣿⣿⣻⣷⣬⣙⠻⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⢀⣿⠃⠀⠀⠠⣻⣷⣿⣿⠏⣼⣿⠁⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡿⣫⣿⣿⡽⠛⣟⡟⢿⣾⠺⡷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡿⠀⣀⣿⣿⣿⣿⣿⣧⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣯⡿⣶⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠇⠀⠀⣰⣿⣿⣿⡽⡉⣠⣿⣿⡁⣿⣆⠀⠀⠀⠀⠀⠀⠌⠀⡾⢛⣯⣷⡿⠛⠋⠀⠀⠈⠉⠻⢿⣿⡍⡙⢿⠦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⠃⠜⣵⣿⣿⣿⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⡟⠳⢼⡌⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣨⡏⠀⣠⣾⠟⣉⡿⠏⣠⣴⣿⣿⣿⡇⢻⡿⣦⡀⠀⠀⠀⠀⢀⡜⣠⣾⡿⠏⠀⢀⣀⣀⣀⣀⣀⢀⠀⠈⠻⢯⣼⣆⢻⣴⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⠃⢀⣾⣿⣿⣿⣿⣿⣿⣿⣇⠹⣿⣿⣿⣾⣿⣿⣿⣿⣻⣿⣿⣿⣷⡤⠠⢃⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡟⢀⣼⣾⠅⠋⣨⣵⠛⣹⣿⣿⣿⣿⣿⡌⣷⡌⢿⣦⠀⠀⢠⠊⣰⣿⣫⣬⡶⠗⠛⠉⠉⠉⠉⠉⠙⠛⢶⣧⣲⣌⠿⣿⣯⣻⡄⠀⠀⠀⠀⠀⠠⢀⣼⣿⡿⢈⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣌⠻⣿⣿⣿⣿⡯⢻⠿⣻⣿⣿⣿⡏⠁⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⢁⣾⢷⡣⣢⣾⡷⣡⣾⣿⣿⣿⣿⣿⣿⣧⣘⢿⣄⠙⣽⣠⢣⣼⡿⠾⠟⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠈⠉⢁⣿⣿⣿⡃⠀⠀⡈⣡⡌⣵⣾⢟⣹⣧⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣦⡛⣿⣯⣿⣷⡷⠹⣾⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⢸⣿⢳⣸⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣽⣿⣷⡽⣱⣾⡯⠀⠀⠀⠀⠀⠀⠀⠸⣧⣤⡎⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣼⢂⢳⡿⣥⣿⣿⣿⡾⢿⣧⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⢿⣿⠿⡀⣿⣿⣟⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠃⠀⢸⣿⡘⣷⣿⠿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡔⣾⡿⣇⠀⠀⠀⠀⠀⠀⠙⢧⣹⣻⠄⠀⠀⠀⠀⠀⠀⠀⢀⡿⣿⣿⣿⣿⡁⣽⢿⣿⣿⣿⢻⢏⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡻⣷⡀⢸⣿⣿⣅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⡌⠁⠀⠀⠀⠀⣴⠠⠟⣯⠞⣆⡀⠄⡀⠀⠀⢀⣴⡏⣭⣿⣿⣿⣿⣿⣾⣾⡴⢻⣿⣧⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣾⣷⡄⣿⣯⢿⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⡟⡿⢋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡊⢁⣠⣎⡾⠛⡼⠇⢨⡐⣝⠳⢴⣄⡱⡄⠊⣯⢟⡶⢿⣿⣿⣿⢿⣻⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣟⢿⣿⣿⣿⣿⣿⣿⣿⣿⡞⢹⣿⣧⡃⠀⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣷⣿⣿⣿⡿⡣⠊⣰⡻⣫⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⣿⣿⢣⣟⡿⢱⣟⡵⢛⣜⣩⠜⣚⢭⢑⡊⠏⢉⣹⡥⣀⠷⣉⢧⣿⡟⢾⢙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣜⡍⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣿⣿⣿⡤⠼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣻⣿⣿⠿⠎⣴⡞⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢾⣯⣿⣿⡿⢠⣟⣛⡿⠿⠫⠍⣠⠤⡐⠰⠀⣂⡈⢳⣵⣿⣿⡓⢦⡤⠑⠌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣮⣻⣿⣿⣿⣿⣿⣿⣿⡿⣇⢡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣽⣿⡟⠀⣾⣃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣶⣟⢻⣽⣿⣿⣥⡄⠂⣄⡘⠷⡶⢐⢤⠍⠀⢁⡈⠙⢍⠳⣽⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⡜⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⡁⡾⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⡿⣯⣿⣿⣿⣄⣣⣬⣝⡻⠎⣽⣩⡵⣎⣶⣷⣿⣦⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⢨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣇⢳⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢏⣼⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣖⣻⣿⣿⣿⣿⠿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⢿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣻⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⢿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⠋⣏⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣏⣿⣿⣻⣿⣟⣿⣿⣿⣿⣿⣿⣻⢼⡥⢹⣏⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠇⣾⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢫⠻⣿⣿⣿⢿⣿⡾⣿⣿⣿⣿⣿⡏⡟⡇⡞⣿⣟⣿⣿⣹⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣹⢰⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⢿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢿⢿⣿⣿⣿⣿⡽⣿⣿⣿⣿⡇⡇⢧⡇⣿⡽⢻⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣝⡻⢿⣿⡻⠛⠫⠽⠋⠔⢋⠒⠩⠹⠛⠣⠙⠬⢩⡘⣩⠟⣸⢭⣳⡾⠿⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⡏⢸⣺⣿⣿⣿⣿⠋⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠟⢿⣷⡽⣿⣽⣿⣿⣿⣷⣿⣼⣿⡽⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡶⠛⠽⣦⠉⠒⢉⠒⠂⠈⠄⠁⠀⢉⠀⠈⣁⠠⠨⡝⠎⣮⢏⡘⣥⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣯⠒⣴⣿⣿⣿⡿⠃⣼⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠣⣙⣿⣿⣿⣿⣿⣟⣷⢹⡘⣿⣷⣿⣹⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣳⢦⠐⢬⡓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢉⡼⢃⠒⣐⡴⢟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⢟⡴⢂⣼⣿⣿⣽⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⡼⡄⣧⢻⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣀⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡛⠠⠃⠼⢠⠘⡜⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣧⠿⢃⡼⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣻⣌⢷⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣓⠬⡑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠐⠁⡨⢡⠌⣓⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠗⡴⣋⣾⡿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀
Made by Germanized at github.com/germanized LETS STOP SCAMMERS"""

        credits_label = QLabel(credits_text)
        credits_label.setStyleSheet("color: white; background-color: #2e2e2e; border-radius: 10px; padding: 20px;")
        credits_label.setAlignment(Qt.AlignCenter)

        self.credits_layout.addWidget(credits_label)

        self.animation = QPropertyAnimation(credits_label, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setStartValue(QRectF(0, 0, 0, 0))
        self.animation.setEndValue(QRectF(50, 50, 700, 500))
        self.animation.start()

    def setup_spam_webhook(self):
        webhook_url_label = QLabel("Webhook URL:")
        webhook_url_label.setStyleSheet("color: white;")
        self.spam_webhook_url_input = QLineEdit()
        self.spam_webhook_url_input.setStyleSheet("background-color: #2e2e2e; color: white; border: none; border-radius: 5px; padding: 5px;")

        message_label = QLabel("Message:")
        message_label.setStyleSheet("color: white;")
        self.spam_message_input = QTextEdit()
        self.spam_message_input.setStyleSheet("background-color: #2e2e2e; color: white; border: none; border-radius: 5px; padding: 5px;")

        spam_button = QPushButton("Spam")
        spam_button.setStyleSheet("background-color: #3e3e3e; color: white; border: none; border-radius: 5px; padding: 5px;")
        spam_button.clicked.connect(self.spam_webhook)

        self.spam_webhook_layout.addWidget(webhook_url_label)
        self.spam_webhook_layout.addWidget(self.spam_webhook_url_input)
        self.spam_webhook_layout.addWidget(message_label)
        self.spam_webhook_layout.addWidget(self.spam_message_input)
        self.spam_webhook_layout.addWidget(spam_button)

    def setup_change_webhook_name(self):
        webhook_url_label = QLabel("Webhook URL:")
        webhook_url_label.setStyleSheet("color: white;")
        self.change_webhook_name_url_input = QLineEdit()
        self.change_webhook_name_url_input.setStyleSheet("background-color: #2e2e2e; color: white; border: none; border-radius: 5px; padding: 5px;")

        new_name_label = QLabel("New Name:")
        new_name_label.setStyleSheet("color: white;")
        self.new_name_input = QLineEdit()
        self.new_name_input.setStyleSheet("background-color: #2e2e2e; color: white; border: none; border-radius: 5px; padding: 5px;")

        change_name_button = QPushButton("Change Name")
        change_name_button.setStyleSheet("background-color: #3e3e3e; color: white; border: none; border-radius: 5px; padding: 5px;")
        change_name_button.clicked.connect(self.change_webhook_name)

        self.change_webhook_name_layout.addWidget(webhook_url_label)
        self.change_webhook_name_layout.addWidget(self.change_webhook_name_url_input)
        self.change_webhook_name_layout.addWidget(new_name_label)
        self.change_webhook_name_layout.addWidget(self.new_name_input)
        self.change_webhook_name_layout.addWidget(change_name_button)

    def setup_send_messages_x_times(self):
        webhook_url_label = QLabel("Webhook URL:")
        webhook_url_label.setStyleSheet("color: white;")
        self.send_messages_x_times_url_input = QLineEdit()
        self.send_messages_x_times_url_input.setStyleSheet("background-color: #2e2e2e; color: white; border: none; border-radius: 5px; padding: 5px;")

        message_label = QLabel("Message:")
        message_label.setStyleSheet("color: white;")
        self.send_messages_x_times_message_input = QTextEdit()
        self.send_messages_x_times_message_input.setStyleSheet("background-color: #2e2e2e; color: white; border: none; border-radius: 5px; padding: 5px;")

        times_label = QLabel("Times:")
        times_label.setStyleSheet("color: white;")
        self.times_input = QLineEdit()
        self.times_input.setStyleSheet("background-color: #2e2e2e; color: white; border: none; border-radius: 5px; padding: 5px;")

        send_button = QPushButton("Send")
        send_button.setStyleSheet("background-color: #3e3e3e; color: white; border: none; border-radius: 5px; padding: 5px;")
        send_button.clicked.connect(self.send_messages_x_times)

        self.send_messages_x_times_layout.addWidget(webhook_url_label)
        self.send_messages_x_times_layout.addWidget(self.send_messages_x_times_url_input)
        self.send_messages_x_times_layout.addWidget(message_label)
        self.send_messages_x_times_layout.addWidget(self.send_messages_x_times_message_input)
        self.send_messages_x_times_layout.addWidget(times_label)
        self.send_messages_x_times_layout.addWidget(self.times_input)
        self.send_messages_x_times_layout.addWidget(send_button)



    def attach_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("All Files (*)")
        file_dialog.setViewMode(QFileDialog.List)
        if file_dialog.exec_():
            files = file_dialog.selectedFiles()

    def send_webhook(self):
        url = self.webhook_url_input.text()
        message = self.message_input.toPlainText()
        delay = int(self.delay_input.text()) if self.delay_input.text().isdigit() else 0
        try:
            response = requests.post(url, json={"content": message})
            if response.status_code == 204:
                QMessageBox.information(self, "Success", "Message sent successfully.")
            else:
                QMessageBox.warning(self, "Failed", "Failed to send message.")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def spam_webhook(self):
        url = self.spam_webhook_url_input.text()
        message = self.spam_message_input.toPlainText()
        while True:
            try:
                response = requests.post(url, json={"content": message})
                if response.status_code == 204:
                    time.sleep(1)
                else:
                    QMessageBox.warning(self, "Failed", "Failed to send message.")
                    break
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))
                break

    def delete_webhook(self):
        url = self.webhook_url_input.text()
        try:
            response = requests.delete(url)
            if response.status_code == 204:
                QMessageBox.information(self, "Success", "Webhook deleted successfully.")
            else:
                QMessageBox.warning(self, "Failed", "Failed to delete webhook.")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def change_webhook_name(self):
        url = self.change_webhook_name_url_input.text()
        new_name = self.new_webhook_name_input.text()
        try:
            response = requests.patch(url, json={"name": new_name})
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Webhook name changed successfully.")
            else:
                QMessageBox.warning(self, "Failed", "Failed to change webhook name.")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def send_messages_x_times(self):
        url = self.send_messages_x_times_url_input.text()
        message = self.send_messages_x_times_message_input.toPlainText()
        count = int(self.send_messages_x_times_count_input.text()) if self.send_messages_x_times_count_input.text().isdigit() else 1
        for _ in range(count):
            try:
                response = requests.post(url, json={"content": message})
                if response.status_code == 204:
                    time.sleep(1)
                else:
                    QMessageBox.warning(self, "Failed", "Failed to send message.")
                    break
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))
                break



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        rect = self.rect()
        rect_f = QRectF(rect.x(), rect.y(), rect.width(), rect.height())
        path.addRoundedRect(rect_f, 15, 15)  
        painter.setClipPath(path)
        painter.fillPath(path, QBrush(QColor("#1e1e1e")))  

def main():
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
