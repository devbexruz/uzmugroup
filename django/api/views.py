from django.shortcuts import render
from itertools import chain

# Create your views here.
from rest_framework import generics
from pages.models import (
    ChatMessage,
    User,
    Course,
    Module,
    Lesson,
    CodeSnippet,
    CodeSnippetStatuses,
    Task,
    TaskSolution
)
from .serializers import ChatMessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from pages.utils import describtion_to_html
from telebot import TeleBot
from django.conf import settings
# Faylni qaytarish image file turida
from django.http import FileResponse

import requests

bot = TeleBot(settings.FILE_UPLOAD_BOT_TOKEN)

# Xabarlar ro‘yxati va yaratish (GET, POST)
class ChatMessageListCreateView(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

# Xabarni yangilash va o‘chirish (GET, PUT, DELETE)
class ChatMessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer


# Chat Message: send, delete, update
class SendMessageAPI(APIView):
    def post(self, request, course_id, auth_token):
        content = request.data.get("content")
        try:
            user = User.objects.get(auth_token=auth_token)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)
        if user not in course.students.all() and user.id != course.teacher.id:
            return Response({"error": "You are not allowed to send messages in this course"}, status=403)
        
        # Bazaga yozish
        message = ChatMessage.objects.create(
            course=course,
            user=user,
            content=content
        )

        # WebSocket guruhiga yuborish
        channel_layer = get_channel_layer()
        print(message.content)
        try:
            content = describtion_to_html(message.content)
        except:
            return Response({"error": "Message format is not supported"}, status=404)
        async_to_sync(channel_layer.group_send)(
            f"chat_{course.id}",
            {
                "type": "chat_message",
                "message": {
                    "command": "new_message",
                    "id": message.id,
                    "user_id": user.id,
                    "name": user.name+"\n",
                    "content": content,
                    "created_at": str(message.created_at)
                }
            }
        )

        return Response({"status": "ok", "message": content})
class DeleteMessageAPI(APIView):
    def post(self, request, course_id, auth_token, message_id):
        try:
            message = ChatMessage.objects.get(id=message_id)
        except ChatMessage.DoesNotExist:
            return Response({"error": "Message not found"}, status=404)
        try:
            user = User.objects.get(auth_token=auth_token)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        if message.user.id != user.id:
            return Response({"error": "You are not allowed to delete this message"}, status=403)
        # Bazadan o‘chirish
        message.delete()

        # WebSocket guruhiga yuborish
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{message.course.id}",
            {
                "type": "chat_message",
                "message": {
                    "command": "delete_message",
                    "id": message.id,
                }
            }
        )

        return Response({"status": "ok", "message": "Message deleted"})
class EditMessageAPI(APIView):
    def post(self, request, course_id, auth_token, message_id):
        new_content = request.data.get("content")
        try:
            message = ChatMessage.objects.get(id=message_id)
        except ChatMessage.DoesNotExist:
            return Response({"error": "Message not found"}, status=404)
        
        try:
            user = User.objects.get(auth_token=auth_token)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        if message.user.id != user.id:
            return Response({"error": "You are not allowed to delete this message"}, status=403)

        # Xabarni yangilash
        message.content = new_content
        message.save()

        # WebSocket guruhiga yuborish
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{message.course.id}",
            {
                "type": "chat_message",
                "message": {
                    "command": "edit_message",
                    "id": message.id,
                    "content": describtion_to_html(message.content),
                }
            }
        )

        return Response({"status": "ok", "message": "Message edited"})

# Profile: upload image
class UploadProfileImageAPI(APIView):
    def post(self, request, auth_token):
        try:
            user = User.objects.get(auth_token=auth_token)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=400)
        file = request.FILES['file']
        # Faylni Telegram bot orqali yuklash
        try:
            result = bot.send_document(chat_id=5139310978, document=file)
            file_info = bot.get_file(result.document.file_id)
            file_url = f"https://api.telegram.org/file/bot{settings.FILE_UPLOAD_BOT_TOKEN}/{file_info.file_path}"
            user.profile_picture = file_url
            user.save()
            return Response({"status": "ok", "message": "Profile image uploaded", "image_url": file_url})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

# Profile: get image
class GetProfileImageAPI(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return FileResponse(open("templates/profile.png", "rb"), content_type="image/jpeg")
        if not user.profile_picture:
            # Default rasmni qaytarish
            return FileResponse(open("templates/profile.png", "rb"), content_type="image/jpeg")
        response = requests.get(user.profile_picture)
        if response.status_code != 200:
            return FileResponse(open("templates/profile.png", "rb"), content_type="image/jpeg")
        # Rasmni qaytarish
        return FileResponse(response, content_type="image/jpeg")

# Get user data
class GetUserAPI(APIView):
    def get(self, request, auth_token):
        try:
            user = User.objects.get(auth_token=auth_token)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        return Response({
            "id": user.id,
            "name": user.name,
            "profile_picture": f"{settings.BASE_URL}/profile/get-image/{user.id}"
        })

# Get AllDatasAPI
class GetAllDatasAPI(APIView):
    def get(self, request, auth_token):
        try:
            user = User.objects.get(auth_token=auth_token)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        # Barcha Course larni olish
        result = []
        enroled_courses = user.enrolled_courses.all()
        courses = user.courses.all()
        for course in chain(courses, enroled_courses):
            course_data = {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "teacher": {
                    "id": course.teacher.id,
                    "name": course.teacher.name
                },
                "modules": []
            }
            if user == course.teacher:
                course_data["role"] = "Teacher"
            else:
                course_data["role"] = "Student"
            modules = Module.objects.filter(course=course).all()
            for module in modules:
                module_data = {
                    "id": module.id,
                    "title": module.title,
                    "description": module.description,
                    "lessons": [],
                    "victorinas": []
                }
                lessons = Lesson.objects.filter(module=module).all()
                for lesson in lessons:
                    lesson_data = {
                        "id": lesson.id,
                        "title": lesson.title,
                        "description": lesson.description,
                        "end_access": lesson.check_end_access(user),
                        "tasks": []
                    }
                    tasks = Task.objects.filter(lesson=lesson).all()
                    for task in tasks:
                        task_data = {
                            "id": task.id,
                            "title": task.title,
                            "description": task.description,
                            "language": task.language
                        }
                        try:
                            solution = TaskSolution.objects.get(task=task, user=user)
                            task_data["solved"] = True
                            task_data["times"] = solution.times
                        except TaskSolution.DoesNotExist:
                            task_data["solved"] = False
                            task_data["times"] = 0
                        lesson_data["tasks"].append(task_data)
                    if lesson.victorina:
                        module_data["victorinas"].append(lesson_data)
                    else:
                        module_data["lessons"].append(lesson_data)
                course_data["modules"].append(module_data)
            result.append(course_data)
        return Response({
            "courses": result,
            "completed_courses": [
                {
                    "id": course.id,
                    "title": course.title,
                    "description": course.description,
                    "teacher": {
                        "id": course.teacher.id,
                        "name": course.teacher.name
                    }
                } for course in user.completed_courses.all()]
        })


class GetModulDataAPI(APIView):
    def get(self, request, auth_token, module_id):
        try:
            user = User.objects.get(auth_token=auth_token)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            return Response({"error": "Module not found"}, status=404)
        if module.course.teacher != user and user not in module.course.students.all():
            return Response({"detail": "Not access!"})
        module_data = {
            "id": module.id,
            "title": module.title,
            "description": module.description,
            "lessons": [],
            "victorinas": []
        }
        lessons = Lesson.objects.filter(module=module).all()
        for lesson in lessons:
            lesson_data = {
                "id": lesson.id,
                "title": lesson.title,
                "description": lesson.description,
                "end_access": lesson.check_end_access(user),
                "tasks": []
            }
            tasks = Task.objects.filter(lesson=lesson).all()
            for task in tasks:
                task_data = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "language": task.language
                }
                try:
                    solution = TaskSolution.objects.get(task=task, user=user)
                    task_data["solved"] = True
                    task_data["times"] = solution.times
                except TaskSolution.DoesNotExist:
                    task_data["solved"] = False
                    task_data["times"] = 0
                lesson_data["tasks"].append(task_data)
            if lesson.victorina:
                module_data["victorinas"].append(lesson_data)
            else:
                module_data["lessons"].append(lesson_data)
        return Response(module_data, status=200)

class GetLessonDataAPI(APIView):
    def get(self, request, auth_token, lesson_id):
        try:
            user = User.objects.get(auth_token=auth_token)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found"}, status=404)
        
        if lesson.module.course.teacher != user and user not in lesson.module.course.students.all():
            return Response({"detail": "Not access!"})
        lesson_data = {
            "id": lesson.id,
            "title": lesson.title,
            "description": lesson.description,
            "end_access": lesson.check_end_access(user),
            "tasks": []
        }
        tasks = Task.objects.filter(lesson=lesson).all()
        for task in tasks:
            task_data = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "language": task.language
            }
            try:
                solution = TaskSolution.objects.get(task=task, user=user)
                task_data["solved"] = True
                task_data["times"] = solution.times
            except TaskSolution.DoesNotExist:
                task_data["solved"] = False
                task_data["times"] = 0
            lesson_data["tasks"].append(task_data)
        return Response(lesson_data)

import uuid

class LoginAPI(APIView):
    def post(self, request):
        login = request.data.get("login")
        password = request.data.get("password")
        if not login or not password:
            return Response({"error": "Login and password are required"}, status=400)
        try:
            user = User.objects.get(login=login, password=password)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        # Yangi token gener qilish
        try:
            token = str(uuid.uuid4())
            user.auth_token = token
            user.save()
            return Response({"auth_token": token})
        except:
            return Response({"error": "Nimadur xato ketdi\nQayta urinib ko'ring!"}, status=501)

