from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import get_user_model

User = get_user_model()


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get("username")
            # raw_password = form.cleaned_data.get("password1")
            # user = User.objects.create_user(username=username, password=raw_password)

            msg = 'Account created successfully.'
            success = True

            messages.success(request, "Account created successfully.")
            return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})



