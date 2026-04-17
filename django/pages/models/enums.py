from django.db import models

class Roles(models.TextChoices):
    TEACHER = 'teacher', "Teacher"

    FOUNDER = 'founder', "Founder"

    BACKEND_BEGINNER = 'backend_beginner', "Beginner Backend Developer"
    FRONTEND_BEGINNER = 'frontend_beginner', "Beginner Frontend Developer"

    BACKEND_JUNIOR = 'backend_junior', "Junior Backend Developer"
    FRONTEND_JUNIOR = 'frontend_junior', "Junior Frontend Developer"

    BACKEND_MIDDLE = 'backend_middle', "Middle Backend Developer"
    FRONTEND_MIDDLE = 'frontend_middle', "Middle Frontend Developer"

    BACKEND_SENIOR = 'backend_senior', "Senior Backend Developer"
    FRONTEND_SENIOR = 'frontend_senior', "Senior Frontend Developer"

class CompletedCourseStatuses(models.TextChoices):
    IN_PROGRESS = 'in_progress', "In Progress"
    COMPLETED = 'completed', "Completed"

class CodeSnippetStatuses(models.TextChoices):
    SUCCESS = 'success', "Success"
    WRONG = 'wrong', "Wrong Answer"
    RUNTIME = 'runtime', "Runtime Error"
    ERROR = 'error', "Error"
    TIME_LIMIT_EXCEEDED = 'time_limit_exceeded', "Time Limit Exceeded"
    MEMORY_LIMIT_EXCEEDED = 'memory_limit_exceeded', "Memory Limit Exceeded"
