import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QTextEdit, QPushButton, QSizePolicy, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class CharacterChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Character Chat")
        self.setGeometry(100, 100, 800, 600)
        
        # メインウィジェットとレイアウトの設定
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # 左側のレイアウト（キャラクター画像とチャット履歴）
        left_layout = QVBoxLayout()
        
        # キャラクター画像の表示
        image_label = QLabel()
        # image_label.setScaledContents(True)
        image_path = os.path.join(os.path.dirname(__file__), "img", "akane_shinjo", "img_base", "default", "akane_normal.png")
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setMinimumSize(300, 300)
        # image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
        # left_layout.addWidget(image_label, 2)
        left_layout.addWidget(image_label)
        
        # チャット履歴の表示
        chat_history = QTextEdit()
        chat_history.setReadOnly(True)
        # chat_history.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # left_layout.addWidget(chat_history, 1)
        left_layout.addWidget(chat_history)
        
        # 右側のレイアウト（入力エリアと送信ボタン）
        right_layout = QVBoxLayout()
        
        # 入力エリア
        input_area = QTextEdit()
        input_area.setPlaceholderText("メッセージを入力してください...")
        # input_area.setMaximumHeight(60)
        # input_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # right_layout.addWidget(input_area, 1)
        right_layout.addWidget(input_area)

        # 送信ボタン
        send_button = QPushButton("送信")
        # send_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # right_layout.addWidget(send_button, 0)
        right_layout.addWidget(send_button)
        
        # レイアウトの追加
        main_layout.addLayout(left_layout, 2)  # 左側を2倍の幅に
        main_layout.addLayout(right_layout, 1)  # 右側を1倍の幅に

def main():
    app = QApplication(sys.argv)
    window = CharacterChatApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
