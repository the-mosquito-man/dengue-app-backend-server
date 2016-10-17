from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^$', views.UserManually.as_view()),
    url(r'^fast/$', views.UserFast.as_view()),
    url(r'^signin/$', views.UserLogin.as_view()),
    url(r'^admin/signin/$', views.AdminUserLogin.as_view()),
]
