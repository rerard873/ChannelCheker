from django import forms
from django.core.exceptions import ValidationError
from channels.models import Channels



class SendChannelForm(forms.ModelForm):
    url = forms.URLField(widget=forms.URLInput(attrs={'class':'input_class','placeholder': 'Введите ссылку...'}))
    class Meta:
        model = Channels
        fields = ['url']


    def clean_url(self):
        url = self.cleaned_data['url']
        if self.get_platform() == "twitch":
            streamer_name = self.get_twitch_name()
            if streamer_name == "NoName":
                raise ValidationError("Не удалось определить Twitch канал")
        else:
            raise ValidationError("Неподдерживаемая платформа или неверный URL")
        return url


    def get_twitch_name(self):
        parts = self.cleaned_data['url'].rstrip('/').split('/')
        return parts[-1] if parts else "NoName"

    def get_platform(self):
        if ("twitch" in self.cleaned_data['url']):
            return 'twitch'
        return "error"



