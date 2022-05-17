from django.forms import ModelForm

from appointments.models import Appointment


class ContactForm(ModelForm):

    class Meta:
        model = Appointment
        fields = ['date', 'client_name', 'message']
        # labels = {
        #     'date': ('Date'),
        #     'client_name': ('Client name'),
        #     'message': ('Message')
        # }