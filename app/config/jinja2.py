from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment


def query(request=None, **kwargs):
    query_params = {k: v for k, v in request.GET.items() if v and kwargs.get(k)} if request else {}
    query_params.update({k: v for k, v in kwargs.items() if v})
    if query_params:
        return '?' + '&'.join([f'{k}={v}' for k, v in query_params.items()])
    return ''


def environment(**options):
    extensions = options.get('extensions', [])
    extensions.append('sass_processor.jinja2.ext.SassSrc')
    options['extensions'] = extensions
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'query': query,
    })
    return env
