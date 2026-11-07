from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from .models import QuizQuestion, QuestionChoice, LeoCandidate


class QuestionChoiceInline(admin.TabularInline):
    """Allow adding choices inline on the question page."""
    model = QuestionChoice
    extra = 4
    fields = ('choice_text', 'is_correct')


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'marks')
    search_fields = ('question_text',)
    inlines = [QuestionChoiceInline]


class LeoCandidateResource(resources.ModelResource):
    """django-import-export resource for Excel export."""
    class Meta:
        model = LeoCandidate
        fields = ('id', 'nic', 'full_name', 'club_name', 'score', 'total_marks', 'is_passed', 'submitted_at')
        export_order = fields


@admin.register(LeoCandidate)
class LeoCandidateAdmin(ExportMixin, admin.ModelAdmin):
    resource_classes = [LeoCandidateResource]
    list_display = ('full_name', 'nic', 'club_name', 'score', 'total_marks', 'is_passed', 'submitted_at')
    list_filter = ('is_passed', 'submitted_at')
    search_fields = ('nic', 'full_name', 'club_name')
    readonly_fields = ('nic', 'full_name', 'club_name', 'score', 'total_marks', 'is_passed', 'submitted_at')
    date_hierarchy = 'submitted_at'

    def has_add_permission(self, request):
        return False  # Only system can create candidate records
