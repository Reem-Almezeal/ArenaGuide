from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message_type", "other_type", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "contact-input",
                "placeholder": "Your full name"
            }),
            "email": forms.EmailInput(attrs={
                "class": "contact-input",
                "placeholder": "example@email.com"
            }),
            "phone": forms.TextInput(attrs={
                "class": "contact-input",
                "placeholder": "05XXXXXXXX"
            }),
            "message_type": forms.Select(attrs={
                "class": "contact-input",
                "id": "messageType"
            }),
            "other_type": forms.TextInput(attrs={
                "class": "contact-input",
                "placeholder": "Please specify the message type",
                "id": "otherTypeInput"
            }),
            "subject": forms.TextInput(attrs={
                "class": "contact-input",
                "placeholder": "Message subject"
            }),
            "message": forms.Textarea(attrs={
                "class": "contact-input contact-textarea",
                "placeholder": "Write your message here...",
                "rows": 6
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        message_type = cleaned_data.get("message_type")
        other_type = cleaned_data.get("other_type")

        if message_type == ContactMessage.MessageType.OTHER and not other_type:
            self.add_error("other_type", "Please specify the message type")

        if message_type != ContactMessage.MessageType.OTHER:
            cleaned_data["other_type"] = ""

        return cleaned_data