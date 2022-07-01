from dataclasses import field
from socket import fromshare
from django import forms 
from .models import Post
from crispy_forms.helper import FormHelper

class createpostform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description']
        unlabelled_fields = ('description',)

 
    def __init__(self, *args, **kwargs):
        super(createpostform, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        for field in createpostform.Meta.unlabelled_fields:
            self.fields[field].label = False
            