from .views.others import (
    home,
    about,
    chat,
    code_edit_python,
    code_edit_javascript,
    code_view,
    solve_task,
    task_description,
    lesson_components,
    course_communications
)
from django.contrib.auth import views as auth_views

from django.urls import path


urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('register/', home, name='request_register'),
    path('code_edit/python/', code_edit_python, name='code_edit_python'),
    path('code_edit/javascript/', code_edit_javascript, name='code_edit_javascript'),
    path('view_code_snippet/', code_view, name='view_code_snippet'),
    path('solve_task/', solve_task, name='solve_task'),
    path('solve_task/', solve_task, name='solve_task'),
    path('chat/<int:course_id>/<str:auth_token>/', chat, name='chat'),
    path('task_description/<int:task_id>/<str:auth_token>/', task_description, name='task_description'),
    path('lesson_components/<int:lesson_id>/<str:auth_token>/', lesson_components, name='lesson_component'),
    path('course_communications/<int:course_id>/<str:auth_token>/', course_communications, name='course_communications'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='custom_login')
]
from .views import admin, others
# Dashboard Urls
urlpatterns += [
    path("admin/", view=admin.dashboard_view, name="admin_dashboard"),
    path("admin/courses", view=admin.courses_view, name="admin_courses"),
    path("admin/teachers", view=admin.teachers_view, name="admin_teachers"),
    path("admin/students", view=admin.students_view, name="admin_students"),
    path("admin/settings", view=admin.settings_view, name="admin_settings"),
    path("admin/notifications", view=admin.notifications_view, name="admin_notifications"),
    path("admin/profile", view=admin.profile_view, name="admin_profile"),
    path("admin/assignments", view=admin.assignments_view, name="admin_assignments"),
    path("admin/analytics", view=admin.analytics_view, name="analytics"),
    path('admin/logout/', others.custom_logout, name='admin_custom_logout')
]
