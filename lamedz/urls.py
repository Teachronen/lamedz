from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# =========================================================
# urlpatterns של הפרויקט הראשי
# =========================================================
# כאן מוגדרות הכתובות הראשיות של הפרויקט.
# =========================================================
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("missions.urls")),
]

# =========================================================
# חיבור קבצי media בזמן פיתוח
# =========================================================
# בזמן פיתוח מקומי, Django יכול להגיש קבצים מתוך MEDIA_ROOT.
#
# זה חשוב כדי שתוכל לראות תמונות/סרטונים שהועלו.
#
# settings.MEDIA_URL  = למשל /media/
# settings.MEDIA_ROOT = התיקייה שבה הקבצים נשמרים בפועל
#
# שים לב:
# בפרודקשן בדרך כלל Nginx יגיש את הקבצים האלה,
# אבל בפיתוח מקומי זה מספיק וטוב.
# =========================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)