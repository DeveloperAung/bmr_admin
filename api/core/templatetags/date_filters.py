# your_app/templatetags/date_filters.py
from django import template
from datetime import datetime

register = template.Library()


@register.filter
def to_ymd(value):
    try:
        dt = datetime.strptime(value, "%d/%m/%Y %I:%M %p")  # input: 12/06/2025 12:00 AM
        return dt.strftime("%Y-%m-%d")  # output: 2025-06-12
    except Exception:
        return ""
