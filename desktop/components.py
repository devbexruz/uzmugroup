from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QFrame, QDialog, QPushButton, QSizePolicy
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QCursor
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from utils import *
import requests

class CodeEditor(QWebEngineView):
    def __init__(self, mode, server=None):
        super().__init__()
        self.server = server
        self.setStyleSheet("border-radius: 10px;")
    def load_task(self, task):
        self.setUrl(QUrl(f"http://45.138.158.199:8002/solve_task/?task_id={task.id}&auth_token={self.server.auth_token}"))

class TaskDescription(QWebEngineView):
    def __init__(self, mode, server=None):
        super().__init__()
        self.server = server
        self.setStyleSheet("border-radius: 10px;background-color: transparent;background: transparent;")
    def load_task(self, task):
        self.setUrl(QUrl(f"http://45.138.158.199:8002/task_description/{task.id}/{self.server.auth_token}/"))



class ChatView(QWebEngineView):
    def __init__(self, mode, course=None, server=None):
        super().__init__()
        self.mode = mode
        self.course = course
        self.server = server
        self.setStyleSheet("border-radius: 10px;background-color: transparent;background: transparent;")
    def update_styles(self, mode):
        self.setStyleSheet("border-radius: 10px; background-color: rgb(20, 40, 80);")
        self.setUrl(QUrl(f"http://45.138.158.199:8002/chat/{self.course.id}/{self.server.auth_token}/?mode={self.mode}"))
    def load_chat(self, course):
        self.course = course
        self.setUrl(QUrl(f"http://45.138.158.199:8002/chat/{self.course.id}/{self.server.auth_token}/?mode={self.mode}"))

class LessonComponents(QWebEngineView):
    def __init__(self, mode, lesson=None, server=None):
        super().__init__()
        self.mode = mode
        self.lesson = lesson
        self.server = server
        self.setStyleSheet("border-radius: 10px;background-color: transparent;background: transparent;")
    def update_styles(self, mode):
        self.setStyleSheet("border-radius: 10px; background-color: rgb(20, 40, 80);")
        self.setUrl(QUrl(f"http://45.138.158.199:8002/lesson_components/{self.course.id}/{self.server.auth_token}/?mode={self.mode}"))
    def load_components(self, lesson):
        self.lesson = lesson
        self.setUrl(QUrl(f"http://45.138.158.199:8002/lesson_components/{self.lesson.id}/{self.server.auth_token}/?mode={self.mode}"))

class CourseCommunications(QWebEngineView):
    def __init__(self, mode, course=None, server=None):
        super().__init__()
        self.mode = mode
        self.course = course
        self.server = server
        self.setStyleSheet("border-radius: 10px;background-color: transparent;background: transparent;")
    def update_styles(self, mode):
        self.setStyleSheet("border-radius: 10px; background-color: rgb(20, 40, 80);")
        self.setUrl(QUrl(f"http://45.138.158.199:8002/course_communications/{self.course.id}/{self.server.auth_token}/?mode={self.mode}"))
    def load_communications(self, course):
        self.course = course
        self.setUrl(QUrl(f"http://45.138.158.199:8002/course_communications/{self.course.id}/{self.server.auth_token}/?mode={self.mode}"))

class MessageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        loadUi("designs/message.ui", self)


class BaseButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFocusPolicy(Qt.NoFocus)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(90)
        self.active = False
        self.collect = False
        self.clicked.connect(self.on_click)
        self.set_active()
    def set_active(self, active=False):
        self.active = active
        if active:
            self.setStyleSheet("""QPushButton{
            text-align: left;
            padding: 30px 40px;
            color: blue;
            background-color: rgba(0, 0, 255, 15);
            border:1px solid rgba(0, 0, 255, 15);
            }""")
        elif self.collect:
            self.setStyleSheet("""QPushButton{
            text-align: left;
            padding: 30px 40px;
            background-color: rgba(0, 255, 0, 20);
            border:1px solid rgba(0, 255, 0, 40);
            color: rgb(0,155,100);
            }""")
        else:
            self.setStyleSheet("""QPushButton{
            text-align: left;
            padding: 30px 40px;
            background-color: rgba(0, 0, 0, 5);
            border:1px solid rgba(0, 0, 0, 5);
            }
            QPushButton:hover {
            background-color: rgba(0, 0, 0, 20);
            border:1px solid rgba(0, 0, 0, 40);
            }""")
class Task(BaseButton):
    def __init__(self, ui, server, lesson, data):
        super().__init__()
        self.ui = ui
        self.server = server
        self.lesson = lesson
        self.data = data

        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.language = data["language"]
        self.solved = data["solved"]

        self.setText(self.title)
    def on_click(self):
        self.lesson.deactivate_childs()
        self.set_active(True)
        self.lesson.load_task(self)
class Lesson(BaseButton):
    def __init__(self, ui, server, module, data):
        super().__init__()
        self.ui = ui
        self.server = server
        self.module = module
        self.data = data

        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]

        self.tasks = []
        for task_data in data["tasks"]:
            task = Task(self.ui, self.server, self, task_data)
            self.tasks.append(task)
        self.setText(self.title)

        # Tugmalarni ulash
        self.ui.tasks_button.clicked.connect(self.go_tasks)
        self.ui.solve_task_button.clicked.connect(self.go_description)
        self.ui.chat_button.clicked.connect(self.go_chat)
        self.ui.components_button.clicked.connect(self.go_components)
        self.ui.communications_button.clicked.connect(self.go_communications)

    def on_click(self):
        self.module.deactivate_childs()
        self.set_active(True)
        clear_layout(self.ui.tasks_layout)
        self.recreate_datas()
        for task in self.tasks:
            self.ui.tasks_layout.addWidget(task)
        self.ui.lessonComponents.load_components(self)
        self.ui.menyuStack.setCurrentIndex(3)
        self.ui.tasksStack.setCurrentIndex(0)
    def deactivate_childs(self):
        for task in self.tasks:
            task.set_active(False)
    def recreate_datas(self):
        self.tasks.clear()
        for task_data in self.data["tasks"]:
            task = Task(self.ui, self.server, self, task_data)
            self.tasks.append(task)
    def clear_tasks_buttons(self):
        self.ui.tasks_button.setStyleSheet("""QPushButton{
            background-color: rgb(255,255,255, 30);
            border: white;
            }
            QPushButton:hover{
            background-color: rgba(0,0,255,20);
            border: 1px solid rgba(0,0,255,30);
            }""")
        self.ui.solve_task_button.setStyleSheet("""QPushButton{
            background-color: rgb(255,255,255, 30);
            border: white;
            }
            QPushButton:hover{
            background-color: rgba(0,0,255,20);
            border: 1px solid rgba(0,0,255,30);
            }""")
        self.ui.chat_button.setStyleSheet("""QPushButton{
            background-color: rgb(255,255,255, 30);
            border: white;
            }
            QPushButton:hover{
            background-color: rgba(0,0,255,20);
            border: 1px solid rgba(0,0,255,30);
            }""")
        self.ui.components_button.setStyleSheet("""QPushButton{
            background-color: rgb(255,255,255, 30);
            border: white;
            }
            QPushButton:hover{
            background-color: rgba(0,0,255,20);
            border: 1px solid rgba(0,0,255,30);
            }""")
        self.ui.communications_button.setStyleSheet("""QPushButton{
            background-color: rgb(255,255,255, 30);
            border: white;
            }
            QPushButton:hover{
            background-color: rgba(0,0,255,20);
            border: 1px solid rgba(0,0,255,30);
            }""")
    def load_task(self, task):
        self.ui.editor.load_task(task)
        self.ui.taskDescription.load_task(task)
        self.ui.solve_task_button.click()
    def go_tasks(self):
        self.clear_tasks_buttons()
        self.ui.tasks_button.setStyleSheet("""QPushButton{
        background-color: rgba(0,0,255,10);
        border: 1px solid rgba(0,0,255,10);
        }
        QPushButton:hover{
        background-color: rgba(0,0,255,20);
        border: 1px solid rgba(0,0,255,30);
        }""")
        self.ui.tasksStack.setCurrentIndex(0)
    def go_description(self):
        self.clear_tasks_buttons()
        self.ui.solve_task_button.setStyleSheet("""QPushButton{
        background-color: rgba(0,0,255,10);
        border: 1px solid rgba(0,0,255,10);
        }
        QPushButton:hover{
        background-color: rgba(0,0,255,20);
        border: 1px solid rgba(0,0,255,30);
        }""")
        self.ui.tasksStack.setCurrentIndex(1)
    def go_chat(self):
        self.clear_tasks_buttons()
        self.ui.chat_button.setStyleSheet("""QPushButton{
        background-color: rgba(0,0,255,10);
        border: 1px solid rgba(0,0,255,10);
        }
        QPushButton:hover{
        background-color: rgba(0,0,255,20);
        border: 1px solid rgba(0,0,255,30);
        }""")
        self.ui.tasksStack.setCurrentIndex(2)
    def go_components(self):
        self.clear_tasks_buttons()
        self.ui.components_button.setStyleSheet("""QPushButton{
        background-color: rgba(0,0,255,10);
        border: 1px solid rgba(0,0,255,10);
        }
        QPushButton:hover{
        background-color: rgba(0,0,255,20);
        border: 1px solid rgba(0,0,255,30);
        }""")
        self.ui.tasksStack.setCurrentIndex(3)
    def go_communications(self):
        self.clear_tasks_buttons()
        self.ui.communications_button.setStyleSheet("""QPushButton{
        background-color: rgba(0,0,255,10);
        border: 1px solid rgba(0,0,255,10);
        }
        QPushButton:hover{
        background-color: rgba(0,0,255,20);
        border: 1px solid rgba(0,0,255,30);
        }""")
        self.ui.tasksStack.setCurrentIndex(4)
class Module(BaseButton):
    def __init__(self, ui, server, course, data):
        super().__init__()
        self.ui = ui
        self.server = server
        self.course = course
        self.data = data

        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.lessons = []
        for lesson_data in data["lessons"]:
            lesson = Lesson(self.ui, self.server, self, lesson_data)
            self.lessons.append(lesson)
        self.setText(self.title)
    def on_click(self):
        self.course.deactivate_childs()
        self.set_active(True)
        clear_layout(self.ui.lessons_layout)
        self.recreate_datas()
        for lesson in self.lessons:
            self.ui.lessons_layout.addWidget(lesson)
        self.ui.menyuStack.setCurrentIndex(2)
    def deactivate_childs(self):
        for lesson in self.lessons:
            lesson.set_active(False)
    def recreate_datas(self):
        self.lessons.clear()
        for lesson_data in self.data["lessons"]:
            lesson = Lesson(self.ui, self.server, self, lesson_data)
            self.lessons.append(lesson)

class Course(BaseButton):
    def __init__(self, ui, server, main, data):
        super().__init__()
        self.ui = ui
        self.server = server
        self.main = main
        self.data = data

        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.modules = []
        for module_data in data["modules"]:
            module = Module(self.ui, self.server, self, module_data)
            self.modules.append(module)
        self.setText(self.title)
        
        # QPlainTextEdit ctrl + enter ignore inter send_message
        # self.ui.message_edit
        self.keyPressEvent_foreplantextadit = self.ui.message_edit.keyPressEvent
        self.ui.message_edit.keyPressEvent = self.send_message
    def on_click(self):
        self.main.deactivate_childs()
        self.set_active(True)

        clear_layout(self.ui.modules_layout)
        self.recreate_datas()
        for module in self.modules:
            self.ui.modules_layout.addWidget(module)
        
        self.ui.courseCommunications.load_communications(self)
        self.ui.chatView.load_chat(self)
        self.ui.menyuStack.setCurrentIndex(2)
    def deactivate_childs(self):
        for module in self.modules:
            module.set_active(False)
    def recreate_datas(self):
        self.modules.clear()
        for module_data in self.data["modules"]:
            module = Module(self.ui, self.server, self, module_data)
            self.modules.append(module)

    def send_message(self, event):
        if event.key() == 16777220:
            if not (event.modifiers() & Qt.ShiftModifier):
                message = self.ui.message_edit.toPlainText().strip()
                if message == "":
                    return
                self.ui.message_edit.clear()
                self.server.send_chat_message(self.id, [{"type":"text", "text": message}])
                return
            
        self.keyPressEvent_foreplantextadit(event)

class ControlComponent:
    def __init__(self, server, root):
        self.server = server
        self.ui = root
        self.courses = []
        self.completed_courses = []
        self.ui.logout_button.clicked.connect(self.logout_func)
        self.ui.login_button.clicked.connect(self.login_func)
    def get_ui_datas(self):
        res = self.server.get_all_datas()
        print(res)
        if "detail" in res or "courses" not in res:
            self.server.auth_token = None
            self.ui.menyuStack.setCurrentIndex(0)
            return
        clear_layout(self.ui.courses_layout)
        self.courses.clear()
        for course_data in res["courses"]:
            course = Course(self.ui, self.server, self, course_data)
            self.ui.courses_layout.addWidget(course)
            self.courses.append(course)
        if self.server.auth_token is None:
            self.ui.menyuStack.setCurrentIndex(0)
        else:
            self.ui.menyuStack.setCurrentIndex(1)
    def deactivate_childs(self):
        for course in self.courses:
            course.set_active(False)
    def login_func(self, event):
        login = self.ui.login_input.text()
        password = self.ui.password_input.text()
        res = self.server.login(login, password)
        if "auth_token" in res:
            self.server.save_auth_token(res["auth_token"])
            self.ui.menyuStack.setCurrentIndex(1)
            self.ui.show_success("Hisobingizga muvaffaqiyatli kirdingiz!")
            self.ui.login_input.clear()
            self.ui.password_input.clear()
            self.get_ui_datas()
        else:
            self.ui.menyuStack.setCurrentIndex(0)
            self.ui.show_error("Login yoki parol xato!")
    def logout_func(self):
        self.server.auth_token = None
        self.ui.menyuStack.setCurrentIndex(0)
        with open("auth_token.txt", "w") as f:
            f.write("")
