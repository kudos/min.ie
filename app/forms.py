from django.forms import CharField, ModelForm, TextInput

from .models import Link


class LinkForm(ModelForm):
    url = CharField(
        widget=TextInput(
            attrs={
                "class": "u-full-width",
                "placeholder": "Paste the link you want to shorten",
            }
        ),
        label="",
    )

    class Meta:
        model = Link
        fields = ["url"]
