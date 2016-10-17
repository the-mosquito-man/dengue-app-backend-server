from django.conf.urls import url
from pages import views

urlpatterns = [
    url(r'^$', views.AdminLoginPage.as_view()),
]
