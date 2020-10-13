from django import forms
from blog.models import Post,Comment,Video
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','password')
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('author','title', 'text',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }


class VideoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'عنوان ویدیو'
        self.fields['cover'].label = 'کاور ویدیو'
        self.fields['video_url'].label = 'فایل ویدیو'


    class Meta:
        model = Video
        fields = ('title','cover', 'video_url')