from django import forms
from django.contrib.comments.forms import CommentForm
from overviewer.comments.models import EditableComment


class EditableCommentForm(CommentForm):
    email = forms.EmailField(required=False)

    def get_comment_model(self):
        return EditableComment
