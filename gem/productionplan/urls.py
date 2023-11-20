from django.urls import path

from . import views

urlpatterns = [
	path("", views.production_plan, name="production_plan"),
]
