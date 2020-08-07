from django.contrib import admin
from django.urls import path,include
from . import views
app_name='measurements'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.calculate_dis_view,name='xyz')
]
