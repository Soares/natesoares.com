from django.conf.urls.defaults import url, patterns
from personal.utilities.urls import slug

def simple_collection_patterns(model, list_args=None, detail_args=None):
    list_args, detail_args = list_args or {}, detail_args or {}
    list_args.setdefault('extra_context', {})['model'] = model
    detail_args.setdefault('extra_context', {})['model'] = model
    return patterns('personal.common.views',
        (r'^$', 'list', dict(list_args, model=model)),
        (r'^(?P<slug>%s)/$' % slug, 'detail', dict(detail_args, model=model)),
    )
