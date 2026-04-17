from PyQt5.QtWidgets import QMainWindow, QSizePolicy
from PyQt5.uic import loadUi
from components import (
    CodeEditor,
    TaskDescription,
    ChatView,
    MessageDialog,
    LessonComponents,
    CourseCommunications
)
from PyQt5.QtCore import Qt
from server_connection import server




class MainWindow(QMainWindow):
    def __init__(self, *args, **kvargs):
        super(MainWindow, self).__init__(*args, **kvargs)
        loadUi("designs/main.ui", self)

        self.mode = "light"

        # self.menyuStack.setCurrentIndex(3)
        
        self.editor = CodeEditor(self.mode, server)
        self.verticalLayout_22.addWidget(self.editor)

        self.taskDescription = TaskDescription(self.mode, server)
        self.verticalLayout_23.addWidget(self.taskDescription)

        self.chatView = ChatView(self.mode, None, server)
        self.verticalLayout_26.addWidget(self.chatView)

        self.lessonComponents = LessonComponents(self.mode, None, server)
        self.verticalLayout_27.addWidget(self.lessonComponents)

        self.courseCommunications = CourseCommunications(self.mode, None, server)
        self.verticalLayout_7.addWidget(self.courseCommunications)

        self.message_dialog = MessageDialog(self)

        # Flaglar
        self.dragging = False
        self.start_pos = None

        # Eventlar
        self.resizer.mousePressEvent = self.startResize
        self.resizer.mouseMoveEvent = self.doResize
        self.resizer.mouseReleaseEvent = self.endResize
        self.message_edit.textChanged.connect(self.text_change_event)
        self.go_home_button.clicked.connect(self.go_home)
        self.go_course_button.clicked.connect(self.go_course)

    def startResize(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.start_pos = event.globalPos()
            self.start_width = self.content_hint.width()

    def doResize(self, event):
        self.max_hint = self.content_hint.width() + self.code_hint.width()
        if self.dragging:
            delta = event.globalPos().x() - self.start_pos.x()

            # chap panelni o‘zgartiramiz (teskari bo‘lishi uchun -delta)
            new_width = self.start_width + delta
            if new_width + 500 < self.max_hint:  # cheklash
                self.content_hint.setMaximumWidth(new_width)
                self.content_hint.setMinimumWidth(new_width)

    def endResize(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            cw = self.content_hint.width()
            ctw = self.code_hint.width()
            try:
                mn = abs(100 - (ctw / cw))
            except ZeroDivisionError:
                return
            ctw_ratio = 100
            cw_ratio = 1

            for i in range(100, 0, -1):
                for j in range(100, 0, -1):
                    if abs(i/j - ctw/cw) < mn:
                        mn = abs(i/j - ctw/cw)
                        ctw_ratio = i
                        cw_ratio = j
            self.content_hint.setMaximumWidth(10000)
            self.content_hint.setMinimumWidth(0)

            self.horizontalLayout_5.setStretch(0, cw_ratio)
            self.horizontalLayout_5.setStretch(2, ctw_ratio)
    # Chat panelini o‘zgartiramiz
    def text_change_event(self):
        doc_height = int(self.message_edit.document().size().height())*30 + 20  # 10px padding
        new_height = max(80, min(doc_height, 300))
        self.tigma_conteyneri.setFixedHeight(new_height)
        self.message_edit.setFixedHeight(new_height)
    def set_light_mode(self):
        self.mode = "light"
        self.update_styles()

    def set_dark_mode(self):
        self.mode = "dark"
        self.update_styles()

    def update_styles(self):
        if self.mode == "dark":
            self.setStyleSheet("color: white;\n"
                               "background-color: rgb(20, 40, 80);\n"
                               "padding: 20px;")
        else:
            self.setStyleSheet("padding: 20px;")
        self.chatView.update_styles(self.mode)
        self.taskDescription.update_styles(self.mode)
        self.editor.update_styles(self.mode)
    def show_success(self, message):
        self.message_dialog.title.setText("Muvaffaqiyatli!")
        self.message_dialog.info.setText(message)
        self.message_dialog.show()
    def show_message(self, message):
        self.message_dialog.title.setText("Xabar!")
        self.message_dialog.info.setText(message)
        self.message_dialog.show()
    def show_error(self, message):
        self.message_dialog.title.setText("Xatolik!")
        self.message_dialog.info.setText(message)
        self.message_dialog.show()
    def go_home(self):
        self.menyuStack.setCurrentIndex(1)
    def go_course(self):
        self.menyuStack.setCurrentIndex(2)
