from django.urls import path
from .views import (
    ChatMessageListCreateView,
    ChatMessageRetrieveUpdateDestroyView,
    SendMessageAPI, UploadProfileImageAPI,
    GetProfileImageAPI,
    GetAllDatasAPI,
    GetModulDataAPI,
    GetLessonDataAPI,
    LoginAPI
)

urlpatterns = [
    # Chat view sets
    # path("chat-messages/", ChatMessageListCreateView.as_view(), name="chatmessage-list-create"),
    # path("chat-messages/<int:pk>/", ChatMessageRetrieveUpdateDestroyView.as_view(), name="chatmessage-detail"),
    
    # Chat send message APIViews
    path("chat-messages/send/<int:course_id>/<str:auth_token>/", SendMessageAPI.as_view(), name="chatmessage-send"),
    
    # Profile APIViews
    path("profile/upload-image/<str:auth_token>/", UploadProfileImageAPI.as_view(), name="upload-image"),
    path("profile/get-image/<int:user_id>/", GetProfileImageAPI.as_view(), name="get-image"),

    # Datas APIViews
    path("datas/get-all/<str:auth_token>/", GetAllDatasAPI.as_view(), name="get-all"),
    path("datas/get-modul/<int:modul_id>/<str:auth_token>/", GetModulDataAPI.as_view(), name="get-modul"),
    path("datas/get-lesson/<int:lesson_id>/<str:auth_token>/", GetLessonDataAPI.as_view(), name="get-lesson"),

    # Login APIView
    path("auth/login/", LoginAPI.as_view(), name="login"),
]
