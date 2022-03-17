from django.forms import ModelForm, BooleanField

from .models import Post


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cats'].empty_label = 'Choose category'
    check_box = BooleanField(label='Check the box!')

    class Meta:
        model = Post
        fields = ['title', 'author', 'cats', 'text', 'check_box']
        labels = {
            'cats': ('Category'),
        }


