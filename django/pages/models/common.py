from .base import BaseModel
from django.db import models
from multiselectfield import MultiSelectField
from .enums import Roles, CompletedCourseStatuses, CodeSnippetStatuses
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255)

    roles = MultiSelectField(choices=Roles.choices, blank=True)

    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    rank = models.IntegerField(default=150)

    solved_tasks = models.ManyToManyField('Task', related_name='solved_by', blank=True)

    auth_token = models.CharField(max_length=255, blank=True, null=True, unique=True)
    def __str__(self):
        return self.name



class Course(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    teacher = models.ForeignKey(User, related_name='courses', on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True, default=[])
    graduates = models.ManyToManyField(User, related_name='completed_courses', blank=True, default=[])
    def __str__(self):
        return self.title

class Module(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Lesson(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    victorina = models.BooleanField(default=False)
    contents = models.JSONField(blank=True, null=True)
    auto_end_access = models.BooleanField(default=True)
    def check_end_access(self, user):
        result = True
        if self.auto_end_access:
            tasks = self.tasks.all()
            for task in tasks:
                if user not in task.solved_by.all():
                    return False
            return True
        try:
            CompletedLesson.objects.get(user=user, lesson=self)
        except CompletedLesson.DoesNotExist:
            return False
        return result
        

    def __str__(self):
        return self.title

class CompletedLesson(BaseModel):
    user = models.ForeignKey(User, related_name='completed_lessons', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='completed_by', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default=CompletedCourseStatuses.COMPLETED, choices=CompletedCourseStatuses.choices)
    completed_at = models.DateTimeField(auto_now_add=True)


class ChatMessage(BaseModel):
    course = models.ForeignKey(Course, related_name='chat_messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='chat_messages', on_delete=models.CASCADE)
    content = models.JSONField()

    def __str__(self):
        return str(self.course) + " message"

class Language(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    language_id = models.IntegerField(unique=True)  # Judge0 API uchun til IDsi

    def __str__(self):
        return f"{self.name} {self.version}"

class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.JSONField()
    lesson = models.ForeignKey(Lesson, related_name='tasks', on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey(Language, blank=True, null=True, on_delete=models.SET_NULL)
    time_limit = models.IntegerField(default=1)  # in seconds
    memory_limit = models.IntegerField(default=16)  # in MB


    def __str__(self):
        return self.title
class TestCase(models.Model):
    task = models.ForeignKey(Task, related_name='test_cases', on_delete=models.CASCADE)
    input_data = models.TextField()
    expected_output = models.TextField()

    def __str__(self):
        return f"TestCase for {self.task.title}"


class CodeSnippet(models.Model):
    task = models.ForeignKey(Task, related_name='code_snippets', on_delete=models.CASCADE)
    code = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=CodeSnippetStatuses.choices)
    user = models.ForeignKey(User, related_name='code_snippets', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"CodeSnippet for {self.task.title}"



class TaskSolution(BaseModel):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    code_snippet = models.OneToOneField(CodeSnippet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='solutions', on_delete=models.CASCADE)
    times = models.IntegerField(default=1)
    def __str__(self):
        return f"Solution for {self.task.title}"