import sys
import time
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QImage, QPixmap

root_dir = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root_dir / "apps" / "platform" / "src"))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ODPlatform 桌面推理演示 (测试画框)")
        self.resize(800, 600)
        central = QWidget()
        layout = QVBoxLayout(central)
        self.label = QLabel("点击开始推理...")
        self.label.setStyleSheet("background-color: black; color: white;")
        self.label.setMinimumSize(640, 480)
        layout.addWidget(self.label)
        self.btn = QPushButton("开始推理")
        self.btn.clicked.connect(self.start_infer)
        layout.addWidget(self.btn)
        self.setCentralWidget(central)

    def start_infer(self):
        self.btn.setEnabled(False)
        self.btn.setText("推理中...")
        
        import cv2
        import numpy as np
        
        # 造一张纯黑图
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        # 画一个绿色的框
        cv2.rectangle(img, (100, 100), (500, 400), (0, 255, 0), 3)
        # 写一行字
        cv2.putText(img, "Person 0.95", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 转换并显示
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qimg))
        
        self.btn.setText("推理结束")
        self.btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
