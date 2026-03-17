from django.shortcuts import render, redirect
from .forms import StudentSubmissionForm
from .models import Submission
from django.conf import settings

# =========================================================
# password gate
# =========================================================
def password_gate(request):
    """
    עמוד שבו המשתמש מזין סיסמה כדי להיכנס לאתר.
    אם הסיסמה נכונה → נשמור session ונעביר לגלריה.
    """

    if request.method == "POST":
        password = request.POST.get("password")

        if password == settings.SITE_PASSWORD:
            request.session["is_authenticated"] = True
            return redirect("home")

        else:
            return render(request, "missions/password.html", {
                "error": "סיסמה שגויה"
            })

    return render(request, "missions/password.html")


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
    """
    גלריה — אבל רק אם המשתמש הזין סיסמה
    """

    if not request.session.get("is_authenticated"):
        return redirect("password_gate")

    # כאן הקוד הרגיל שלך
    submissions = Submission.objects.filter(status="approved").order_by("-created_at")

    return render(request, "missions/gallery.html", {
        "submissions": submissions
    })
