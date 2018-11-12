from django.views.generic import TemplateView


class ApplicantUpdateView(TemplateView):
    template_name = 'members/applicant_update.jinja2'
