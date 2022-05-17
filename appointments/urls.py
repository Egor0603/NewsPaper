from django.urls import path

from appointments.views import AppointmentCreateView, Success

urlpatterns = [
    # path('make_appointment/', AppointmentCreateView.as_view(), name='make_appointment'),
    path('make_appointment/', AppointmentCreateView.as_view(), name='make_appointment'),
    path('success/<int:pk>', Success.as_view(), name='success_appointment')
]
