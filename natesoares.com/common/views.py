from django.views.generic.list_detail import object_list, object_detail
from personal.utilities.decorators import gets_tags

def objects(request, model):
    return model.all_objects if request.user.is_staff else model.objects


def update_to_tags(dict, tags):
    qualifier = ('?tags=' + ','.join(tags)) if tags else ''
    dict.update({'tags': tags, 'qualifier': qualifier})


@gets_tags
def list(request, model, tags, **kwargs):
    update_to_tags(kwargs.setdefault('extra_context', {}), tags)
    return object_list(request, objects(request, model).tagged_with(tags), **kwargs)


@gets_tags
def detail(request, model, tags, **kwargs):
    update_to_tags(kwargs.setdefault('extra_context', {}), tags)
    return object_detail(request, objects(request, model).tagged_with(tags), **kwargs)
