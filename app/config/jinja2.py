from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment


def query(request=None, **kwargs):
    query_params = {k: v for k, v in request.GET.items() if v} if request else {}
    query_params.update(kwargs)
    query_params = {k: v for k, v in query_params.items() if v}
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
