from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(ChatMessage)
admin.site.register(Task)
admin.site.register(TestCase)
admin.site.register(CodeSnippet)
admin.site.register(TaskSolution)
admin.site.register(Language)
