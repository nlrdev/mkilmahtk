from .core import (
    HttpResponse,
    bleach,
    json,
    is_post,
    is_get,
    render,
    log,
    render,
    push_msg,
    forbidden,
    redirect,
    get_object_or_404,
)
from .context import get_main_context, get_item_context


def app(request, page="main", function="index"):
    request.page = bleach.clean(page)
    request.function = bleach.clean(function)
    request.current_page = bleach.clean(request.path.split("/")[-2])

    if request.POST.get("action"):
        request.action = bleach.clean(request.POST.get("action"))
    else:
        request.action = request.page

    context = {
        "current_page": request.current_page if request.current_page != "" else "main",
        "page": request.page,
        "function": request.function,
        "template": f"app/{request.page}/index.html",
        "action": request.action,
        "javascript": [
            f"js/{request.page}.js",
        ],
    }

    context_factory = {
        "main": get_main_context,
        "item": get_item_context,
    }

    try:
        _context = context_factory[request.page](request)
        context |= _context if _context else no_context()
    except Exception as e:
        log(e)

    if is_post(request):
        try:
            return HttpResponse(json.dumps(context), content_type="application/json")
        except Exception as e:
            log(e)
            return HttpResponse(
                json.dumps({"alert": "Failed to proccess the request!"}),
                content_type="application/json",
            )

    if is_get(request):
        try:
            return render(request, "index.html", context)
        except Exception as e:
            log(e)
            push_msg(request, "Failed to find the page or resource!", "alert-warning")
            return render(request, "index.html", {"template": "src/error.html"})


def no_context(*args, **kwargs):
    return {}
