from PyQt5.QtWidgets import QApplication
import sys
import time
from server_connection import server
from base import MainWindow
from components import ControlComponent
from utils import clear_layout

app = QApplication(sys.argv)

root = MainWindow()

clear_layout(root.courses_layout)
clear_layout(root.modules_layout)
clear_layout(root.lessons_layout)
clear_layout(root.tasks_layout)


controller = ControlComponent(server, root)
controller.get_ui_datas()

root.show()


sys.exit(app.exec_())


