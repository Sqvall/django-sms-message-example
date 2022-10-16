from django.urls import path

from notifications.views import ExampleSMSView

urlpatterns = [
    path('', ExampleSMSView.as_view()),
]
