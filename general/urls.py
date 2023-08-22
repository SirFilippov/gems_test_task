from django.urls import path
from .views import DealsAPIView, home_page

urlpatterns = [
    path('api/v1/general', DealsAPIView.as_view()),
    path('', home_page, name='home_page')
]
