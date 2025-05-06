import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QTextEdit, QPushButton, QSizePolicy, QFrame, QGroupBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class CharacterChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("修正イメージ再現")
        self.setMinimumSize(900, 700)  # 最小サイズのみを指定
        
        # メインウィンドウの全体レイアウト (縦方向)
        main_layout = QVBoxLayout(self)
        
        # --- 1. 上部エリア (コントロールバー + More) ---
        top_area_layout = QHBoxLayout()  # 横方向のレイアウト
        # 左側の「キャラクター変更など設定バー」部分
        self.create_placeholder("キャラクター変更など設定バー", layout=top_area_layout, fixed_height=30, expanding_width=True)
        # 右側の「More」ボタン部分
        more_button_placeholder = self.create_placeholder("More (過去チャット履歴表示)", layout=top_area_layout, fixed_height=30)
        more_button_placeholder.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        main_layout.addLayout(top_area_layout)
        
        # --- 2. 中央メインコンテンツエリア ---
        center_main_layout = QHBoxLayout()
        
        # --- 2a. 左側エリア (AI選択 + コントロール + 画像) ---
        left_area_layout = QVBoxLayout()
        
        # AIモデル選択ボックス部分をQGroupBoxで囲む
        ai_model_group = QGroupBox("AIモデル選択ボックス")
        ai_model_layout = QVBoxLayout(ai_model_group)
        self.create_placeholder("・Gemini①", layout=ai_model_layout, fixed_height=20)
        self.create_placeholder("・Gemini②", layout=ai_model_layout, fixed_height=20)
        self.create_placeholder("・ChatGPT", layout=ai_model_layout, fixed_height=20)
        left_area_layout.addWidget(ai_model_group)
        
        # キャラクター名 + 音声ON/OFF 部分
        char_control_layout = QHBoxLayout()
        self.create_placeholder("キャラクター名", layout=char_control_layout, fixed_height=30, expanding_width=True)
        self.create_placeholder("音声ON/OFF (Checkbox)", layout=char_control_layout, fixed_height=30)
        left_area_layout.addLayout(char_control_layout)
        
        # キャラクター画像の表示
        image_label = QLabel()
        image_label.setScaledContents(True)
        image_path = os.path.join(os.path.dirname(__file__), "img", "akane_shinjo", "img_base", "default", "akane_normal.png")
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap)
        image_label.setMinimumSize(300, 300)
        left_area_layout.addWidget(image_label, 2)

        left_area_layout.addStretch(1)
        
        center_main_layout.addLayout(left_area_layout, 1)
        
        # --- 2b. 右側エリア (チャット履歴) ---
        right_chat_area_layout = QVBoxLayout()
        chat_history_placeholder = self.create_placeholder("チャット履歴表示エリア (会話ログ表示)", layout=right_chat_area_layout)
        chat_history_placeholder.setMinimumSize(400, 500)
        right_chat_area_layout.addStretch(1)
        
        center_main_layout.addLayout(right_chat_area_layout, 2)
        
        main_layout.addLayout(center_main_layout)
        
        # --- 3. 下部入力エリア ---
        bottom_input_layout = QHBoxLayout()
        input_field_placeholder = self.create_placeholder("ユーザー入力欄 (テキストや画像)", layout=bottom_input_layout, fixed_height=60)
        input_field_placeholder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        send_button_placeholder = self.create_placeholder("送信", layout=bottom_input_layout, fixed_height=60)
        send_button_placeholder.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        main_layout.addLayout(bottom_input_layout)

    def create_placeholder(self, text, layout=None, fixed_height=None, expanding_width=False):
        label = QLabel(text)
        label.setFrameStyle(QFrame.Box | QFrame.Plain)
        label.setStyleSheet("background-color: #f0f0f0;")
        if fixed_height is not None:
            label.setFixedHeight(fixed_height)
        if expanding_width:
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        if layout:
            layout.addWidget(label)
        return label

def main():
    app = QApplication(sys.argv)
    window = CharacterChatApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()