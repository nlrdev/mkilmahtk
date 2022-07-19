from django.contrib import auth
from django.contrib.auth.decorators import login_required
from app.core import (
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
from .models import LastLogin, ServiceUser


@login_required(login_url="/login/")
def logout(request):
    if is_post(request):
        request.session["user_token"] = "0"
        context = {"javascript": ["js/logout.js"]}
        auth.logout(request)
        return render(request, "src/logout.html", context)
    else:
        forbidden()


def login(request):
    if is_post(request):
        user = auth.authenticate(
            username=request.POST["email"], password=request.POST["password"]
        )
        if user is not None:
            auth.login(request, user)
            service_user = get_object_or_404(ServiceUser, email=user.email)
            push_msg(
                request,
                f"Welcome back: [{user.username}] your last login was on: [{service_user.last_login}]",
                "quality-color-legendary",
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
        # save user logic here

        # then login
        user = auth.authenticate(
            username=request.POST["email"], password=request.POST["password"]
        )
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            return render(
                request,
                "src/registration.html",
                {"error": "Incorrect login"},
            )

    elif is_get(request):
        if "next" in request.GET:
            request.session["next"] = request.GET["next"]
        else:
            request.session["next"] = "/"
        return render(request, "src/registration.html")
    else:
        return forbidden()
