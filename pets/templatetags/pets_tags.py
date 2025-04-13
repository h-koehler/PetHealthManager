import re
from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def get_age_from_dob(dob):
    today = datetime.today()
    years = today.year - dob.year
    months = today.month - dob.month
    if today.day < dob.day:
        months -= 1
    if months < 0:
        years -= 1
        months += 12

    if years == 0:
        return f"{months} months old"
    else:
        return f"{years} yrs, {months} mo. old"

@register.filter
def get_img_file_name(name):
    return re.sub(r'[^a-zA-Z0-9]', '', name)

@register.filter
def pretty_date(dob):
    return dob.strftime("%b %d, %Y")

@register.filter
def get_elapsed_time(date):
    now = datetime.now()
    elapsed = now - date
    seconds = int(elapsed.total_seconds())
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days == 1:
        return "yesterday"
    elif days > 1:
        return f"{days} days ago"
    elif hours == 1:
        return "1 hour ago"
    elif hours > 0:
        return f"{hours} hours ago"
    elif minutes == 1:
        return "1 minute ago"
    elif minutes > 0:
        return f"{minutes} minutes ago"
    elif seconds < 2:
        return "just now"
    else:
        return f"{seconds} seconds ago"