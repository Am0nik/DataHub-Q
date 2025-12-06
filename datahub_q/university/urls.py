from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<int:pk>/', views.university_detail, name='university_detail'),
    path('compare/', views.compare_list, name='compare_list'),
    path('compare/<int:pk1>/<int:pk2>/', views.compare_universities, name='compare_universities'),
    path('chat/', views.chat_with_ai, name='chat_with_ai'),
    path('chat/api/', views.chat_with_ai_api, name='chat_with_ai_api'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
