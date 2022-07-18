import json
import ast
import pandas as pd
from functools import reduce
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from pyparsing import empty
from .core import (
    is_ajax,
    render_to_string,
    get_object_or_404,
    is_get,
    log,
    time,
    format_time,
    bleach,
)
from .models import AH_Item, Item


def get_main_context(request):
    """     
    if "search_terms" in request.session:
        search_terms = pd.unique(
            list(t for t in request.session["search_terms"].split(","))
        ).tolist()
    else:
        search_terms = {}

    search_hist = []
    for s in search_terms:
        if Item.objects.filter(name__contains=s).exists():
            try:
                search_hist.append(get_object_or_404(Item, name__exact=s))
            except:
                continue 
    """
    
    if "view_list" in request.session:
        view_list = pd.unique(
            list(i for i in request.session["view_list"].split(","))
        ).tolist()
    else:
        view_list = {}

    view_hist = []
    for s in view_list:
        view_hist.append(get_object_or_404(Item, item_id=s))

    if is_get(request):
        return {
            "watchlist_items": "",
           # "search_terms": search_terms,
            "view_list": view_hist,
        }

    if is_ajax(request):
        s = bleach.clean(request.POST.get("search_value").lower())
        if "search_terms" in request.session:
            request.session["search_terms"] = request.session["search_terms"] + f",{s}"
        else:
            request.session["search_terms"] = f"{s}"

        words = list(i for i in s.split(" "))
        search_items = (
            Item.objects.annotate(
                search=SearchVector(
                    "item_id",
                    "name",
                ),
            )
            .filter(
                reduce(
                    lambda x, y: x & y,
                    [Q(search__contains=word) for word in words],
                )
            )
            .all()
        )
        return {
            "html": render_to_string(
                "app/main/search_items.html",
                {
                    "search_items": search_items,
                },
                request,
            ),
        }


def get_item_context(request):
    _id = request.function
    if "view_list" in request.session:
        request.session["view_list"] = request.session["view_list"] + f",{_id}"
    else:
        request.session["view_list"] = f"{_id}"

    item = get_object_or_404(Item, item_id=_id)
    qs = list(AH_Item.objects.filter(item_id=_id).values())
    
    if item.item_data != "":
        item_data = dict(ast.literal_eval(item.item_data))
    else:
        item_data = {}
    
    count = len(qs)
    total = 0

    for n in qs:
        p = float(n["buyout"]) / 10000
        q = float(n["quantity"])
        n["buyout"] = p / q
        n["quantity"] = q
        total += q

    df = pd.DataFrame.from_records(qs)
    grouped = df.groupby(pd.Grouper(key='created',freq='H'))
    
    # lol what even is this.
    #times = pd.DatetimeIndex(df.created)
    #grouped = df.groupby(times.hour)    

    labels = []
    price_data = []
    quant_data = []

    for group, matches in grouped: 
        labels.append(format_time(group))
        price_data.append(min(list(a for a in matches['buyout']), default=0)) 
        quant_data.append(sum(list(a for a in matches['quantity'])))   

    if is_get(request):
        return {
            "time": time(),
            "name": item.name,
            "item_data": item_data,
            "labels": labels,
            "price_data": price_data,
            "quant_data": quant_data,
            "count": count,
            "total": total,
        }

    if is_ajax(request):
        pass
