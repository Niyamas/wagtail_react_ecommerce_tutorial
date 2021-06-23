from django.views.generic import TemplateView


class DashBoardView(TemplateView):
    """
    Renders the Dashboard page in the admin.
    """

    template_name = 'dashboard/dashboard.html'