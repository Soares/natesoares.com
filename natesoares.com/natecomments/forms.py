from django import forms
from django.contrib.comments.forms import CommentForm
from django.utils.translation import ungettext, ugettext_lazy as _

class NateCommentForm(CommentForm):
    email = forms.EmailField(label=_("Email address"), required=False)
