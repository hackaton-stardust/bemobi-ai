from django.urls import path
from .views import generate_story 

urlpatterns = [
    path('generate-story/', generate_story, name='generate_story'),
]