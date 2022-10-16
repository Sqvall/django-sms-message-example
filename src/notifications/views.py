from django.shortcuts import render
from django.views import View

from notifications.sms.sms_message import SMSMessage


class ExampleSMSView(View):
    template_name = 'example_sms.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        phone, message_text = request.POST.get('phone'), request.POST.get('message_text')
        message = SMSMessage(phone_numbers=[phone], message=message_text)
        message.send()
        context = {
            'phone': phone,
            'message_text': message_text,
            'backend': f"{message._backend.__class__.__module__}.{message._backend.__class__.__qualname__}",  # noqa
        }
        return render(request, self.template_name, context=context)
