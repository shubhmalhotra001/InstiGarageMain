from django.urls import path
from .views import RegisterView, LoginView, UserView

# Api endpoints for user specific funtionalities
# Check ./views.py for more info
urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('', UserView.as_view()),
]