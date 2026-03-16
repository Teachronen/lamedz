from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Submission


# =========================================================
# פעולת admin: אישור העלאות נבחרות
# =========================================================
# action היא פעולה שאפשר להפעיל על כמה רשומות יחד
# מתוך מסך הרשימה ב-admin.
#
# כאן אנחנו:
# - משנים status ל-approved
# - מעדכנים approved_at לזמן הנוכחי
# =========================================================
@admin.action(description="Approve selected submissions")
def approve_submissions(modeladmin, request, queryset):
    queryset.update(
        status="approved",
        approved_at=timezone.now()
    )


# =========================================================
# פעולת admin: דחיית העלאות נבחרות
# =========================================================
# כאן אנחנו מסמנים כמה העלאות בבת אחת כ-rejected.
# =========================================================
@admin.action(description="Reject selected submissions")
def reject_submissions(modeladmin, request, queryset):
    queryset.update(status="rejected")


# =========================================================
# רישום המודל Submission למסך הניהול
# =========================================================
# המחלקה הזו שולטת באיך המודל נראה ומתנהג ב-admin.
# =========================================================
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):

    # -----------------------------------------------------
    # list_display
    # -----------------------------------------------------
    # אילו עמודות יופיעו בטבלת הרשומות הראשית.
    #
    # כאן אנחנו מציגים:
    # - preview: תצוגה קטנה של הקובץ
    # - title: כותרת ההעלאה
    # - student_name: שם פרטי או כינוי
    # - class_name: כיתה
    # - media_type: האם זו תמונה או וידאו
    # - parent_approval: האם סומן אישור הורים
    # - status: מצב ההעלאה
    # - created_at: זמן יצירה
    # - approved_at: זמן אישור
    # -----------------------------------------------------
    list_display = (
        "is_pending_first",
        "preview",
        "title",
        "student_name",
        "class_name",
        "media_type",
        "parent_approval",
        "status",
        "created_at",
        "approved_at",
    )

    # -----------------------------------------------------
    # list_filter
    # -----------------------------------------------------
    # מסננים צדדיים לפי שדות חשובים.
    # -----------------------------------------------------
    list_filter = (
        "status",
        "class_name",
        "media_type",
        "parent_approval",
        "created_at",
    )

    # -----------------------------------------------------
    # search_fields
    # -----------------------------------------------------
    # חיפוש מהיר לפי שדות טקסט.
    # -----------------------------------------------------
    search_fields = (
        "title",
        "student_name",
        "class_name",
    )

    # -----------------------------------------------------
    # list_editable
    # -----------------------------------------------------
    # מאפשר לערוך שדות ישירות מתוך טבלת הרשימה,
    # בלי להיכנס לכל רשומה.
    #
    # חשוב:
    # שדות שנמצאים כאן לא יכולים להיות גם first column
    # או קישור ראשי לרשומה.
    # -----------------------------------------------------
    list_editable = (
        "status",
    )

    # -----------------------------------------------------
    # list_per_page
    # -----------------------------------------------------
    # כמה רשומות יוצגו בכל עמוד.
    # -----------------------------------------------------
    list_per_page = 25

    # -----------------------------------------------------
    # ordering
    # -----------------------------------------------------
    # מיון ברירת מחדל:
    # החדשים ביותר קודם.
    # -----------------------------------------------------
    ordering = ("status", "-created_at")

    # -----------------------------------------------------
    # readonly_fields
    # -----------------------------------------------------
    # שדות לקריאה בלבד במסך העריכה.
    #
    # preview_link - קישור/תצוגה לקובץ
    # created_at / approved_at - תאריכים שנעדיף לא לערוך ידנית
    # -----------------------------------------------------
    readonly_fields = (
        "preview_link",
        "created_at",
        "approved_at",
    )

    # -----------------------------------------------------
    # fields
    # -----------------------------------------------------
    # קובע את סדר השדות במסך העריכה של רשומה אחת.
    # -----------------------------------------------------
    fields = (
        "title",
        "student_name",
        "class_name",
        "media_type",
        "media_file",
        "preview_link",
        "parent_approval",
        "status",
        "created_at",
        "approved_at",
    )

    # -----------------------------------------------------
    # actions
    # -----------------------------------------------------
    # פעולות מותאמות אישית שאפשר להפעיל על כמה רשומות.
    # -----------------------------------------------------
    actions = [approve_submissions, reject_submissions]

        # =====================================================
    # is_pending_first
    # =====================================================
    # זו פונקציה שמציגה אינדיקציה בולטת אם ההעלאה
    # עדיין ממתינה לבדיקה.
    #
    # אם status הוא "pending":
    # נציג טקסט כתום ובולט.
    #
    # אם לא:
    # נחזיר מחרוזת ריקה.
    #
    # הפונקציה הזו לא שומרת שום דבר במסד הנתונים.
    # היא רק מציגה מידע במסך ה-admin.
    # =====================================================
    def is_pending_first(self, obj):
        if obj.status == "pending":
            return format_html(
                '<span style="color: #b26a00; font-weight: bold;">Pending</span>'
            )
        return ""

    # הטקסט שיופיע בכותרת העמודה
    is_pending_first.short_description = "Needs review"

    # =====================================================
    # preview
    # =====================================================
    # מציג preview קטן בתוך טבלת הרשימה.
    #
    # אם זו תמונה:
    # - נציג thumbnail קטן
    #
    # אם זה וידאו:
    # - נציג טקסט קצר + קישור
    #
    # format_html שומר על HTML בטוח.
    # =====================================================
    def preview(self, obj):
        if not obj.media_file:
            return "-"

        if obj.media_type == "image":
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px;" />',
                obj.media_file.url
            )

        if obj.media_type == "video":
            return format_html(
                '<a href="{}" target="_blank">Open video</a>',
                obj.media_file.url
            )

        return "-"

    preview.short_description = "Preview"

    # =====================================================
    # preview_link
    # =====================================================
    # מוצג בתוך מסך העריכה של רשומה אחת.
    #
    # אם זו תמונה:
    # - נציג תמונה גדולה יותר
    #
    # אם זה וידאו:
    # - נציג קישור לפתיחה
    # =====================================================
    def preview_link(self, obj):
        if not obj.media_file:
            return "No file uploaded"

        if obj.media_type == "image":
            return format_html(
                '<div><img src="{}" style="max-width: 300px; border-radius: 10px;" /></div><p><a href="{}" target="_blank">Open full file</a></p>',
                obj.media_file.url,
                obj.media_file.url
            )

        if obj.media_type == "video":
            return format_html(
                '<a href="{}" target="_blank">Open uploaded video</a>',
                obj.media_file.url
            )

        return "Unsupported file"

    preview_link.short_description = "Uploaded file preview"

    # =====================================================
    # save_model
    # =====================================================
    # הפונקציה הזו נקראת כששומרים רשומה מתוך ה-admin.
    #
    # כאן אנחנו מוסיפים לוגיקה:
    # אם הסטטוס שונה ל-approved
    # ועדיין אין approved_at
    # אז נמלא approved_at אוטומטית.
    #
    # ואם הסטטוס אינו approved,
    # נרוקן את approved_at.
    # =====================================================
    def save_model(self, request, obj, form, change):
        if obj.status == "approved" and not obj.approved_at:
            obj.approved_at = timezone.now()

        if obj.status != "approved":
            obj.approved_at = None

        super().save_model(request, obj, form, change)
