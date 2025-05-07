import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QTextEdit, QPushButton, QSizePolicy, QFrame, QGroupBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QResizeEvent

class CharacterChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("修正イメージ再現")
        self.setMinimumSize(900, 700)  # 最小サイズのみを指定
        
        # メインウィジェットの作成
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # メインウィンドウの全体レイアウト (縦方向)
        main_layout = QVBoxLayout(main_widget)
        
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
        
        # --- 画像のアスペクト比固定のための追加設定 ---
        self.image_label = QLabel() # self をつけてインスタンス変数にする
        self.image_label.setScaledContents(False)
        # 画像パスとロード
        self.image_path = os.path.join(os.path.dirname(__file__), "img", "akane_shinjo", "img_base", "default", "akane_normal.png")
        self.original_pixmap = QPixmap(self.image_path)

        if self.original_pixmap.isNull():
            print(f"エラー: 画像ファイルのロードに失敗しました。パス: {self.image_path}")
            self.image_label.setText(f"画像ロード失敗:\n{self.image_path}")
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.image_label.setFrameStyle(QFrame.Box | QFrame.Plain)
        else:
            # --- サイズポリシーの詳細設定 ---
            size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            size_policy.setHorizontalStretch(1)
            size_policy.setVerticalStretch(1)
            size_policy.setHeightForWidth(True)
            self.image_label.setSizePolicy(size_policy)
            self.image_label.setMinimumSize(300, 300)  # 最小サイズも設定
            self.image_label.setMaximumSize(300, 300)  # 初期サイズを制限
            # --- 設定ここまで ---

            # 画像を表示するためのQLabelをコンテナレイアウトに追加する部分
            image_container_layout = QHBoxLayout()
            
            # 中央揃えのレイアウト
            image_container_layout.addStretch()  # 引数なしのaddStretch
            image_container_layout.addWidget(self.image_label)
            image_container_layout.addStretch()  # 引数なしのaddStretch
            
            # レイアウトの比率は2のまま
            left_area_layout.addLayout(image_container_layout, 2)

        # 左側エリアの残りのスペースを埋める
        left_area_layout.addStretch(1)
        
        # 中央レイアウトに左側エリアを追加
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

        # 初期化が完了した後、最大サイズの制限を解除
        QTimer.singleShot(100, lambda: self.image_label.setMaximumSize(16777215, 16777215))

    def resizeEvent(self, event: QResizeEvent):
        # ウィンドウサイズが変更された時に呼ばれる
        if not self.original_pixmap.isNull():
            # image_label の現在のサイズを取得 (親レイアウトによって決定されたサイズ)
            current_label_size = self.image_label.size()
            window_size = self.size()

            # --- デバッグ用のprint文を追加 ---
            print(f"Window size: {window_size.width()}x{window_size.height()}")
            print(f"Image label size: {current_label_size.width()}x{current_label_size.height()}")
            print(f"Original pixmap size: {self.original_pixmap.width()}x{self.original_pixmap.height()}")
            # --- デバッグ用print文ここまで ---

            # 元の画像を、ラベルのサイズに合わせて、縦横比を維持してスケーリング
            # FastTransformationを使用して高速化
            scaled_pixmap = self.original_pixmap.scaled(
                current_label_size,
                Qt.KeepAspectRatio,
                Qt.FastTransformation  # SmoothTransformationからFastTransformationに変更
            )

            # --- スケーリング後のサイズも確認してみる ---
            print(f"Scaled pixmap size: {scaled_pixmap.width()}x{scaled_pixmap.height()}")
            print("---")
            # --- デバッグ用print文ここまで ---

            # スケーリングした画像をQLabelにセットし直す
            self.image_label.setPixmap(scaled_pixmap)

        # 親クラスの resizeEvent も呼び出す (重要)
        super().resizeEvent(event)

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