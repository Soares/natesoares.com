from django.db import models
from django.db.models.signals import post_save
from django.core.mail import mail_admins
from django.template import loader, Context
from django.contrib.comments.models import Comment
from django.contrib.comments.managers import CommentManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import get_hexdigest, check_password
from django.utils.html import escape
from django.utils.safestring import mark_safe
from markdown2 import markdown
from overviewer.utilities.managers import Manager
from datetime import datetime, timedelta

# Time will be displayed as:
# "X seconds ago" for the first 60 seconds
# "X minutes ago" for the first hour
# "X hours ago" for the first day
# "yesterday" for the second day
# "X days ago" for the first week
# Then the date.
first_minute = timedelta(0, 60)
first_hour = timedelta(0, 60*60)
first_day = timedelta(1)
first_week = timedelta(7)


class EditableComment(Comment):
    edited = models.BooleanField(default=False)
    objects = CommentManager()

    class Meta:
        verbose_name = 'comment'

    def show_time(self):
        delta = datetime.now() - self.submit_date
        if delta < first_minute:
            return '%s seconds ago' % delta.seconds
        if delta < first_hour:
            return '%s minutes ago' % (delta.seconds // 60)
        if delta < first_day:
            return '%s hours ago' % (delta.seconds // (60 * 60))
        if delta.days == 1:
            return 'yesterday'
        if delta < first_week:
            return '%s days ago' % delta.days
        return self.submit_date.strftime('%B %d, %Y')

    def render(self):
        return mark_safe(markdown(escape(self.comment)))

    def ancestor(self):
        parent = self.content_object
        if isinstance(parent, EditableComment):
            return parent.ancestor()
        return parent

    def save(self, *args, **kwargs):
        if self.id is None and not self.ancestor().enable_comments:
            return None
        return super(EditableComment, self).save(*args, **kwargs)

    def has_comments(self):
        return EditableComment.objects.for_model(self).count()


def email(sender, instance, **kwargs):
    t = loader.get_template('comments/email.txt')
    c = Context({'comment': instance})
    mail_admins('New comment to %s' % instance.ancestor(), t.render(c))
post_save.connect(email, sender=EditableComment)
