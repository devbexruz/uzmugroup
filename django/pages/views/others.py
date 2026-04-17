from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import *
from ..utils import *

def home(request):
    context = {
        "categories": ["Web Development", "Data Science", "Mobile", "AI", "DevOps", "Security"],
        "courses": [
            {"title": "Modern React", "instructor": "Jamshid Islomov", "duration": "8 soat", "students": 1200},
            {"title": "Python Data Analysis", "instructor": "Malika Karimova", "duration": "12 soat", "students": 2000},
            {"title": "Docker & Kubernetes", "instructor": "Sardor Akhmedov", "duration": "6 soat", "students": 900},
        ],
        "instructors": [
            {"name": "Jamshid Islomov", "title": "Senior Frontend Engineer", "initials": "JI"},
            {"name": "Malika Karimova", "title": "Data Scientist", "initials": "MK"},
            {"name": "Sardor Akhmedov", "title": "DevOps Engineer", "initials": "SA"},
        ],
        "now": datetime.now(),
    }
    return render(request, "home.html", context)


def about(request):
    return render(request, 'about.html')

def login(request):
    return render(request, 'Login.html')

def chat(request, course_id, auth_token):
    mode = request.GET.get('mode', 'light')
    try:
        user = User.objects.get(auth_token=auth_token)
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': 'Unauthorized access', 'status_code': 401})
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return render(request, 'error.html', {'message': 'Course not found', 'status_code': 404})
    # User in Course students
    
    if user not in course.students.all() and user.id != course.teacher.id:
        return render(request, 'error.html', {'message': 'The course chat is not available to you', 'status_code': 401})
    messages = []
    # Limit 100 messages
    end_id = -1
    for message in ChatMessage.objects.filter(course=course).order_by('-created_at')[:100][::-1]:
        if end_id == message.user.id:
            try:
                messages.append({
                    "id": message.id,
                    "user_id": message.user.id,
                    "name": "",
                    "tanitish": 0,
                    "content": describtion_to_html(message.content),
                    "created_at": message.created_at.isoformat()
                })
            except:
                continue
        else:
            try:
                if len(messages) > 0:
                    messages[-1]["tanitish"] += 2
                messages.append({
                    "id": message.id,
                    "user_id": message.user.id,
                    "name": message.user.name+"\n",
                    "tanitish": 1,
                    "content": describtion_to_html(message.content),
                    "created_at": message.created_at.isoformat()
                })
            except:
                continue
        end_id = message.user.id
    
    if len(messages) > 0:
        messages[-1]["tanitish"] += 2
    return render(request, "ChatView.html", {
        "course": course,
        "mode": mode,
        "auth_token": auth_token,
        "user_id": user.id,
        "base_host": request.get_host(),
        "messages": messages,
        "end_id": end_id
    })


def code_edit_python(request):
    return render(request, 'CodeEdit.html', {
        'title': 'Code Editor - Python',
        'type': 'python'
    })

def code_edit_javascript(request):
    return render(request, 'CodeEdit.html', {
        'title': 'Code Editor - JavaScript',
        'type': 'javascript'
    })


def code_view(request):
    code_snippet_id = request.GET.get('snippet_id')
    auth_token = request.GET.get('auth_token')
    try:
        user = User.objects.get(auth_token=auth_token)
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': 'Unauthorized access', 'status_code': 401})
    snippets = CodeSnippet.objects.filter(user=user)
    code_snippet = snippets.first()
    if not code_snippet:
        return render(request, 'error.html', {'message': 'Code snippet not found', 'status_code': 404})
    try:
        code_snippet = CodeSnippet.objects.get(id=code_snippet_id)

    except CodeSnippet.DoesNotExist:
        return render(request, 'error.html', {'message': 'Code snippet not found', 'status_code': 404})
    return render(request, 'CodeView.html', {
        'title': 'Code Viewer - Python',
        'type': code_snippet.language,
        'code_snippet': code_snippet.code
    })
def solve_task(request):
    task_id = request.GET.get('task_id')
    auth_token = request.GET.get('auth_token')
    try:
        user = User.objects.get(auth_token=auth_token)
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': 'Unauthorized access', 'status_code': 401})
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return render(request, 'error.html', {'message': 'Task not found', 'status_code': 404})



    return render(request, 'CodeEdit.html', {
        'title': 'Code Editor - Python',
        'type': task.language,
        'code_snippet': get_code_snippet(task)
    })


def task_description(request, task_id, auth_token):
    try:
        user = User.objects.get(auth_token=auth_token)
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': 'Unauthorized access', 'status_code': 401})
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return render(request, 'error.html', {'message': 'Task not found', 'status_code': 404})

    return render(request, 'TaskDescription.html', {
        'title': task.title,
        'content': describtion_to_html(task.description)
    })

def lesson_components(request, lesson_id, auth_token):
    try:
        user = User.objects.get(auth_token=auth_token)
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': 'Unauthorized access', 'status_code': 401})
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return render(request, 'error.html', {'message': 'Lesson not found', 'status_code': 404})

    return render(request, 'LessonDescription.html', {
        'title': 'Lesson Description',
        'content': describtion_to_html(lesson.contents)
    })
def course_communications(request, course_id, auth_token):
    try:
        user = User.objects.get(auth_token=auth_token)
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': 'Unauthorized access', 'status_code': 401})
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return render(request, 'error.html', {'message': 'Course not found', 'status_code': 404})
    students = []
    for student in course.students.all():
        students.append({
            'id': student.id,
            'name': student.name,
            'roles': student.roles
        })

    return render(request, 'CourseCommunications.html', {
        'title': 'Course Communications',
        'teacher': {
            'id': course.teacher.id,
            'name': course.teacher.name,
            'roles': course.teacher.roles
        },
        'students': students
    })

def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Siz tizimdan muvaffaqiyatli chiqdingiz!")
        return redirect('custom_login')
    
    # Agar GET so'rov bo'lsa, logout tasdiqlash sahifasini ko'rsat
    return render(request, 'logout.html')

