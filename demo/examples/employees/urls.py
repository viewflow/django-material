from django.urls import path, include
from django.views import generic

from . import views


urlpatterns = [
    path('', generic.RedirectView.as_view(
        url='./departments/'), name="index"),
    path('departments/', include(views.DepartmentViewSet().urls)),
    path('employees/', include(views.EmployeeViewSet().urls)),
]
