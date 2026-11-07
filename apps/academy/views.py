from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.http import require_http_methods
from .models import QuizQuestion, QuestionChoice, LeoCandidate
import random


def entry(request):
    """GET: Show candidate entry form."""
    return render(request, 'academy/entry.html')


@require_http_methods(["POST"])
def verify(request):
    """
    POST /academy/verify/
    Check NIC against LeoCandidate database.
    If new: write to session, pull 20 random questions, render quiz.
    If exists: render already_attempted.html.
    """
    nic = request.POST.get('nic', '').strip()
    full_name = request.POST.get('full_name', '').strip()
    club_name = request.POST.get('club_name', '').strip()

    if not nic or not full_name or not club_name:
        return render(request, 'academy/entry.html', {
            'error': 'All fields are required.'
        })

    # Check if already attempted
    if LeoCandidate.objects.filter(nic=nic).exists():
        candidate = LeoCandidate.objects.get(nic=nic)
        return render(request, 'academy/already_attempted.html', {
            'candidate': candidate
        })

    # New candidate — build quiz session
    question_count = getattr(settings, 'ACADEMY_QUIZ_QUESTIONS', 20)
    all_questions = list(QuizQuestion.objects.prefetch_related('choices').all())

    if len(all_questions) < question_count:
        selected_questions = all_questions
    else:
        selected_questions = random.sample(all_questions, question_count)

    # Serialize question IDs into session
    request.session['candidate_nic'] = nic
    request.session['candidate_name'] = full_name
    request.session['candidate_club'] = club_name
    request.session['quiz_question_ids'] = [q.id for q in selected_questions]
    request.session.modified = True

    return render(request, 'academy/quiz.html', {
        'questions': selected_questions,
        'timer_minutes': getattr(settings, 'ACADEMY_TIMER_MINUTES', 30),
    })


@require_http_methods(["POST"])
def submit(request):
    """
    POST /academy/submit/
    1. Read candidate_nic from session.
    2. Grade selected answers.
    3. Write LeoCandidate record.
    4. Flush session.
    5. Render result.
    """
    nic = request.session.get('candidate_nic')
    full_name = request.session.get('candidate_name')
    club_name = request.session.get('candidate_club')
    question_ids = request.session.get('quiz_question_ids', [])

    # Guard: no valid session
    if not nic:
        return redirect('academy:entry')

    # Guard: already attempted (double-submit protection)
    if LeoCandidate.objects.filter(nic=nic).exists():
        request.session.flush()
        return redirect('academy:entry')

    # Fetch questions in original quiz order
    questions = QuizQuestion.objects.prefetch_related('choices').filter(id__in=question_ids)

    total_marks = 0
    score = 0

    for question in questions:
        total_marks += question.marks
        submitted_choice_id = request.POST.get(f'question_{question.id}')
        if submitted_choice_id:
            try:
                choice = question.choices.get(id=int(submitted_choice_id))
                if choice.is_correct:
                    score += question.marks
            except QuestionChoice.DoesNotExist:
                pass

    # Calculate pass/fail
    pass_percentage = getattr(settings, 'ACADEMY_PASS_PERCENTAGE', 60)
    percentage = (score / total_marks * 100) if total_marks > 0 else 0
    is_passed = percentage >= pass_percentage

    # Write candidate record
    candidate = LeoCandidate.objects.create(
        nic=nic,
        full_name=full_name,
        club_name=club_name,
        score=score,
        total_marks=total_marks,
        is_passed=is_passed,
    )

    # Mandatory: flush session to prevent retries
    request.session.flush()

    return render(request, 'academy/result.html', {
        'candidate': candidate,
        'percentage': round(percentage, 1),
        'pass_percentage': pass_percentage,
    })
