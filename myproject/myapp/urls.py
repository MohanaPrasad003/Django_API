from django.urls import path
from .views import UserProfileCreateView, UserProfileUpdateView

app_name = 'myapp'

urlpatterns = [
    path('create/', UserProfileCreateView.as_view(), name='user-profile-create'),
    path('update/<int:pk>/', UserProfileUpdateView.as_view(), name='user-profile-update'),
]

