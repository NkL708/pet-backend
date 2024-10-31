from django.contrib.admin.widgets import AdminDateWidget
from django.forms import DateField, Form


class GenerateDigestForm(Form):
    date = DateField(
        widget=AdminDateWidget(),
        label="Select date to generate",
    )
