import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle('PyQt5 示例')

        # 创建布局
        layout = QVBoxLayout()

        # 创建一个标签
        self.label = QLabel('欢迎来到PyQt5应用程序!', self)
        layout.addWidget(self.label)

        # 创建一个按钮
        self.button = QPushButton('点击我', self)
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button)

        # 设置主布局
        self.setLayout(layout)

    def on_button_click(self):
        self.label.setText('按钮已被点击！')


def main():
    app = QApplication(sys.argv)
    main_window = MyApp()
    main_window.resize(300, 200)  # 设置窗口大小
    main_window.show()  # 显示窗口
    sys.exit(app.exec_())  # 运行应用程序


if __name__ == '__main__':
    main()
