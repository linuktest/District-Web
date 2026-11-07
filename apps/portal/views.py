from django.shortcuts import render
from django.utils import timezone
from .models import SiteConfig, LeadershipProfile, Club, Event, PressRelease
import calendar as cal


def home(request):
    config = SiteConfig.objects.first()
    recent_events = Event.objects.filter(is_draft=False).order_by('start_time')[:6]
    highlights = PressRelease.objects.all()[:6]
    return render(request, 'portal/home.html', {
        'config': config,
        'recent_events': recent_events,
        'highlights': highlights,
    })


def about(request):
    return render(request, 'portal/about.html')


def leadership(request):
    dec = LeadershipProfile.objects.filter(role_level='DEC')
    directors = LeadershipProfile.objects.filter(role_level='Director')
    zone_chairs = LeadershipProfile.objects.filter(role_level='Zone')
    return render(request, 'portal/leadership.html', {
        'dec': dec,
        'directors': directors,
        'zone_chairs': zone_chairs,
    })


def clubs(request):
    club_list = Club.objects.all()
    regions = Club.objects.values_list('region', flat=True).distinct().order_by('region')
    zones = Club.objects.values_list('zone', flat=True).distinct().order_by('zone')
    return render(request, 'portal/clubs.html', {
        'clubs': club_list,
        'regions': regions,
        'zones': zones,
    })


def district_calendar(request):
    now = timezone.now()
    year = int(request.GET.get('year', now.year))
    month = int(request.GET.get('month', now.month))

    # Get published events for this month
    events = Event.objects.filter(
        is_draft=False,
        start_time__year=year,
        start_time__month=month,
    ).order_by('start_time')

    # Build calendar matrix
    cal_matrix = cal.monthcalendar(year, month)
    month_name = cal.month_name[month]

    # Map events by day
    events_by_day = {}
    for event in events:
        day = event.start_time.day
        events_by_day.setdefault(day, []).append(event)

    # Previous/next month navigation
    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year

    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year

    return render(request, 'portal/calendar.html', {
        'cal_matrix': cal_matrix,
        'month_name': month_name,
        'year': year,
        'month': month,
        'events_by_day': events_by_day,
        'events': events,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'today': now.day if (now.year == year and now.month == month) else None,
    })
