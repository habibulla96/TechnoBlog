from datetime import datetime

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.utils.safestring import mark_safe

from .models import Post


class PostUserForm(forms.ModelForm):
    created = forms.DateTimeField(initial=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), required=False)
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        prepopulated_fields = {'slug': ('title',)}
        model = Post
        # save_as = True
        save_on_top = True
        search_fields = ('title',)
        list_filter = ('category', 'tags')
        readonly_fields = ('created_at', 'get_photo')
        fields = ('title', 'author', 'category', 'tags', 'content', 'photo')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='50'>")
        return '-'

    get_photo.short_description = 'Фото'
