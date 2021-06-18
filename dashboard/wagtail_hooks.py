"""
Adds Wagtail menu items via hooks.

Resources:
 - https://docs.wagtail.io/en/stable/reference/hooks.html
 - https://github.com/wagtail/wagtail/blob/main/wagtail/admin/wagtail_hooks.py
 - https://dev.to/lb/adding-a-react-component-in-wagtail-admin-3e
"""

from django.urls import reverse, path

from wagtail.core import hooks
from wagtail.admin.menu import MenuItem

from dashboard.views import DashBoardView


@hooks.register('register_admin_menu_item')
def register_dashboard_menu_item():
    return MenuItem('Dashboard', reverse('admin-dashboard'), classnames='icon icon-cog', order=7000)

@hooks.register('register_admin_urls')
def urlconf_time():
    return [
        path('dashboard/', DashBoardView.as_view(), name='admin-dashboard')
    ]






from django.templatetags.static import static
from django.utils.html import format_html


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    """Add /static/css/custom.css to the admin"""
    return format_html('<link rel="stylesheet" href="{}">', static("dashboard/css/custom.css"))