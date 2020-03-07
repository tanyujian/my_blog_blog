from django import forms
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from django.contrib.contenttypes.models import ContentType

class CommentForm(forms.Form):
    content_type=forms.CharField(widget=forms.HiddenInput())
    object_id=forms.IntegerField(widget=forms.HiddenInput())
    context=forms.CharField(widget=CKEditorWidget())
    reply_id=forms.IntegerField(widget=forms.HiddenInput(attrs={"id":"reply_id"}))

    def clean(self):
        id=self.cleaned_data["object_id"]
        types=self.cleaned_data["content_type"]
        try:
            model=ContentType.objects.get(model=types).model_class()
            self.cleaned_data["model_obj"]=model.objects.get(id=id)
        except ObjectDoesNotExist:
            raise forms.ValidationError("博客不存在")
        return self.cleaned_data
