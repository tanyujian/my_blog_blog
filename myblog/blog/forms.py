from django import forms
from ckeditor.widgets import CKEditorWidget

#填写博客
class ChangeBlog(forms.Form):
    title=forms.CharField(max_length=50,
                          widget=forms.TextInput(attrs={"class":"form_control","placeholder":"输入标题"}))
    blog_type = forms.ChoiceField(label="博客类型", choices=[('文学', '文学'), ('IT','IT')])
    content = forms.CharField(label="描述",widget=CKEditorWidget())

    def clean(self):
        title=self.cleaned_data.get("title",'').strip()
        content=self.cleaned_data.get("content",'').strip()
        if title =='' and content=="" :
            raise forms.ValidationError("请输入完整的内容")
        return self.cleaned_data
