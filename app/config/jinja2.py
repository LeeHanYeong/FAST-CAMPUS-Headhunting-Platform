from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment


def environment(**options):
    extensions = options.get('extensions', [])
    extensions.append('sass_processor.jinja2.ext.SassSrc')
    options['extensions'] = extensions
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
    })
    return env
