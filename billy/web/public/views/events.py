"""
    views specific to events
"""
import operator
import urllib
import datetime as dt
from icalendar import Calendar, Event

from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.contrib.sites.models import Site


import billy
from billy.models import db, Metadata
from billy.models.pagination import IteratorPaginator

from .utils import templatename, RelatedObjectsList


class EventsList(RelatedObjectsList):
    '''
    Context:
        - See RelatedObjectsList.get_context_data

    Templates:
        - billy/web/public/object_list.html
        - billy/web/public/events_list_row.html
    '''
    collection_name = 'metadata'
    sort_func = operator.itemgetter('when')
    sort_reversed = True
    paginator = IteratorPaginator
    query_attr = 'events'
    use_table = True
    rowtemplate_name = templatename('events_list_row')
    column_headers_tmplname = templatename('events_column_headers')
    show_per_page = 15
    nav_active = 'events'
    description_template = '{{obj.legislature_name}} Events'
    title_template = 'Events - {{obj.legislature_name}}'


def event_ical(request, abbr, event_id):
    event = db.events.find_one({'_id': event_id})
    if event is None:
        raise Http404

    x_name = "X-BILLY"

    cal = Calendar()
    cal.add('prodid', '-//Sunlight Labs//billy//')
    cal.add('version', billy.__version__)

    cal_event = Event()
    cal_event.add('summary', event['description'])
    cal_event['uid'] = "%s@%s" % (event['_id'], Site.objects.all()[0].domain)
    cal_event.add('priority', 5)
    cal_event.add('dtstart', event['when'])
    cal_event.add('dtend', (event['when'] + dt.timedelta(hours=1)))
    cal_event.add('dtstamp', event['updated_at'])

    if "participants" in event:
        for participant in event['participants']:
            name = participant['participant']
            cal_event.add('attendee', name)
            if "id" in participant and participant['id']:
                cal_event.add("%s-ATTENDEE-ID" % (x_name), participant['id'])

    if "related_bills" in event:
        for bill in event['related_bills']:
            if "bill_id" in bill and bill['bill_id']:
                cal_event.add("%s-RELATED-BILL-ID" % (x_name), bill['bill_id'])

    cal.add_component(cal_event)
    return HttpResponse(cal.to_ical(), content_type="text/calendar")


def event(request, abbr, event_id):
    '''
    Context:
        - abbr
        - metadata
        - event
        - sources
        - gcal_info
        - gcal_string
        - nav_active

    Templates:
        - billy/web/public/event.html
    '''
    event = db.events.find_one({'_id': event_id})
    if event is None:
        raise Http404

    fmt = "%Y%m%dT%H%M%SZ"

    start_date = event['when'].strftime(fmt)
    duration = dt.timedelta(hours=1)
    ed = (event['when'] + duration)
    end_date = ed.strftime(fmt)

    gcal_info = {
        "action": "TEMPLATE",
        "text": event['description'].encode('utf-8'),
        "dates": "%s/%s" % (start_date, end_date),
        "details": "",
        "location": event['location'].encode('utf-8'),
        "trp": "false",
        "sprop": "http://%s/" % Site.objects.all()[0].domain,
        "sprop": "name:billy"
    }
    gcal_string = urllib.urlencode(gcal_info)

    return render(request, templatename('event'),
                  dict(abbr=abbr,
                       metadata=Metadata.get_object(abbr),
                       event=event,
                       sources=event['sources'],
                       gcal_info=gcal_info,
                       gcal_string=gcal_string,
                       nav_active='events'))
