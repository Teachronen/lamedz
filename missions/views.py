from django.shortcuts import render, redirect
from .forms import StudentSubmissionForm
from .models import Submission


def upload_submission(request):
    if request.method == "POST":
        form = StudentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("submission_success")
    else:
        form = StudentSubmissionForm()

    return render(request, "missions/upload.html", {"form": form})


def submission_success(request):
    return render(request, "missions/success.html")


def gallery(request):
    submissions = Submission.objects.filter(status="approved").order_by("-created_at")
    return render(request, "missions/gallery.html", {"submissions": submissions})