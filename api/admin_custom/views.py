from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import GenerateDigestForm


@staff_member_required
def generate_digest_view(request):
    if request.method == "POST":
        form = GenerateDigestForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            messages.success(request, f"Digest generated for {date}")
            return HttpResponseRedirect(reverse("admin:api_digest_changelist"))
    else:
        form = GenerateDigestForm()

    context = admin.site.each_context(request)
    context["form"] = form

    return render(
        request,
        "admin/api/generate_digest.html",
        context,
    )
