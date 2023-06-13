from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Sum, Q
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *
from django.db import connection


def index(request):
    polling_units = PollingUnit.objects.all()
    page = request.GET.get('page', 1)
    
    paginator = Paginator(polling_units, 20)
    try:
        emps = paginator.page(page)
    except PageNotAnInteger:
        emps = paginator.page(1)
    except EmptyPage:
        emps = paginator.page(paginator.num_pages)
    context = {
        'polling_units': polling_units,
        'emps':emps,
        }
    return render(request,'index.html',context)

def view_result(request, uniqueid):
    poll_unit = get_object_or_404(PollingUnit, uniqueid=uniqueid)
    result = AnnouncedPuResults.objects.all().filter(polling_unit_uniqueid=uniqueid)
    context = {
        'result':result,
        'poll_unit': poll_unit
    }
    return render(request, 'poll_result.html', context)


def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_lga_result():
    lga_result = {}
    with connection.cursor() as cursor:
        sql = f"""
			SELECT * FROM `announced_pu_results` apu 
            INNER JOIN `polling_unit` pu ON apu.polling_unit_uniqueid=pu.polling_unit_id 
            INNER JOIN `lga` lg ON pu.lga_id=lg.uniqueid
            """
        cursor.execute(sql)
        lga_data = dictfetchall(cursor)
    return lga_data


def sum_total_result(request):
    lga = Lga.objects.all()
    res = AnnouncedPuResults.objects.all()
    pol = PollingUnit.objects.all()
    result = get_lga_result()
    query = request.GET.get("q")
    
    if query:
        result = lga.filter(Q(lga_name__icontains=query))

    context = {
        'result':result,
        'lga': lga,
    }
    return render(request, 'sum_result.html', context)


class PollResultCreate(CreateView, SuccessMessageMixin):
    model = AnnouncedPuResults
    template_name = 'create_poll.html'
    form_class = AnnouncedPuResultsForm
        
    def get_success_url(self):
        messages.success(self.request, 'Result Created Successfully!! ')
        return '/' # or whatever url you want to redirect to