from django.contrib import auth
from django.contrib.auth.decorators import login_required
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
from accounts.models import LastLogin, ServiceUser


def app(request, page="main", function="index"):
    request.page = bleach.clean(page)
    request.function = bleach.clean(function)
    request.current_page = bleach.clean(request.path.split("/")[-2])

    if request.POST.get("action"):
        request._action = bleach.clean(request.POST.get("action"))
    else:
        request._action = request.page

    context = {
        "current_page": request.current_page if request.current_page != "" else "main",
        "page": request.page,
        "function": request.function,
        "template": f"app/{request.page}/index.html",
        "action": request._action,
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


@login_required(login_url="/login/")
def logout(request):
    request.session["user_token"] = "0"
    context = {"js": "js/logout.js"}
    if is_post(request):
        auth.logout(request)
        return render(request, "src/logout.html", context)
    elif is_get(request):
        return render(request, "src/logout.html")
    else:
        return forbidden()


def login(request):
    if is_post(request):
        user = auth.authenticate(
            username=request.POST["email"], password=request.POST["password"]
        )
        if user is not None:
            auth.login(request, user)
            service_user = get_object_or_404(ServiceUser, user=user)
            push_msg(
                request,
                f"Welcome back: [{user.username}] your last login was on: [{service_user.last_login()}]",
                "alert-primary",
            )
            login_time = LastLogin(user=service_user)
            login_time.save()
            next = request.session.pop("next")
            return redirect(next)
        else:
            return render(
                request,
                "src/login.html",
                {"error": "Incorrect login"},
            )
            
    elif is_get(request):
        if "next" in request.GET:
            request.session["next"] = request.GET["next"]
        else:
            request.session["next"] = "/"
        return render(request, "src/login.html")
    else:
        return forbidden()


def registration(request):
    if is_post(request):
        user = auth.authenticate(
            username=request.POST["email"], password=request.POST["password"]
        )
        if user is not None:
            auth.login(request, user)
            service_user = get_object_or_404(ServiceUser, user=user)
            push_msg(
                request,
                f"Welcome back: [{user.username}] your last login was on: [{service_user.last_login()}]",
                "alert-primary",
            )
            login_time = LastLogin(user=service_user)
            login_time.save()
            next = request.session.pop("next")
            return redirect(next)
        else:
            return render(
                request,
                "src/login.html",
                {"error": "Incorrect login"},
            )
            
    elif is_get(request):
        if "next" in request.GET:
            request.session["next"] = request.GET["next"]
        else:
            request.session["next"] = "/"
        return render(request, "src/login.html")
    else:
        return forbidden()
