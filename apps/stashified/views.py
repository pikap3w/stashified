from django.db.models import Q
from django.shortcuts import render

# from django.contrib import messages
from .models import *


# Render
def index(request):
    bags = Bag.objects.filter(
        Q(print__collection__name__contains="Tokidoki") | Q(print__collection__name__contains="Kitty") | Q(
            print__collection__name__contains="WoW"))
    prints = Print.objects.filter(Q(collection__name__contains="Tokidoki") | Q(collection__name__contains="Kitty") | Q(
        collection__name__contains="WoW"))
    context = {
        # 'collections': Collection.objects.all(),
        'prints': prints,
        # 'styles': Style.objects.filter(bags__print__collection__name__contains="Tokidoki"),
        'bags': bags,
        'styles': bags.values("style__name").distinct()
    }

    # if 'logged_in' in request.session and 'user_id' in request.session:
    #     context = {
    #         'jobs': Job.objects.all(),
    #         'accepted_jobs': Job.objects.filter(accepted_by_id=request.session["user_id"]),
    #         'available_jobs': Job.objects.filter(accepted_by_id__isnull=True),
    #     }
    #     return render(request, 'exam/dashboard.html', context)
    # else:
    #     return render(request, "exam/index.html")
    return render(request, "stashified/img-grid.html", context)
