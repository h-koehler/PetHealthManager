import re
from django import template
from datetime import datetime
from django.utils import timezone

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
def pretty_date(dob):
    if dob is not None:
        return dob.strftime("%b %d, %Y")
    else:
        return ""

@register.filter
def pretty_date_time(dob):
    local_time = timezone.localtime(dob)
    return local_time.strftime("%b %d, %Y at %I:%M %p").lstrip("0")

@register.filter
def get_elapsed_time(date):
    if date is None:
        return ""
    now = timezone.now()
    if timezone.is_naive(date):
        date = timezone.make_aware(date)
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

@register.filter
def pretty_phone_number(number):
    digits = ''.join(filter(str.isdigit, number))

    if len(digits) == 7:
        return f"{digits[:3]}-{digits[3:]}"
    elif len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits.startswith("1"):
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return number

@register.filter
def truncate_pfp_url(url):
    url = str(url)
    return url[13:] if url.startswith("pet_profiles/") else url

@register.filter(name="img_name")
def img_name(value):
    if not isinstance(value, str):
        return ""
    m = re.match(r"[A-Za-z]+", value)
    return m.group(0).lower() if m else ""