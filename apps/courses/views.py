from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Enrollment
from .forms import EnrollmentForm

# 1. NEW LANDING PAGE VIEW
def course_list(request):
    """The 'Welcome' page where students select Level 100, 200, 300, or 400."""
    levels = ['100', '200', '300', '400']
    return render(request, 'courses/level_picker.html', {'levels': levels})

# 2. NEW SPECIFIC LEVEL VIEW
def courses_by_level(request, level):
    """The page showing schools and courses for a specific level (e.g., Level 100 only)."""
    # Fetch courses only for the selected level
    courses = Course.objects.filter(level=level).select_related('category')

    # Group those courses by their School (Category)
    schools = {}
    for course in courses:
        school_name = course.category.title
        if school_name not in schools:
            schools[school_name] = []
        schools[school_name].append(course)

    context = {
        'level': level,
        'schools': schools
    }
    return render(request, 'courses/level_view.html', context)

def course_detail(request, pk):
    """Displays details for a specific course."""
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course, 'is_enrolled': False})

def manual_payment(request, pk):
    course = get_object_or_404(Course, pk=pk)

    # CHECK IF SESSION ALREADY HAS AN ENROLLMENT
    session_key = f'enrollment_{pk}'
    if session_key in request.session:
        enrollment_id = request.session[session_key]
        enrollment = Enrollment.objects.filter(id=enrollment_id).first()
        if enrollment:
            return render(request, 'courses/waiting_confirmation.html', {'enrollment': enrollment})

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            if request.user.is_authenticated:
                enrollment.user = request.user
            enrollment.course = course
            enrollment.save()

            request.session[session_key] = enrollment.id
            return render(request, 'courses/waiting_confirmation.html', {'enrollment': enrollment})
    else:
        form = EnrollmentForm()

    return render(request, 'courses/manual_payment.html', {'course': course, 'form': form})

def download_receipt(request, enrollment_id):
    """Allows student to view/download receipt by ID without requiring login."""
    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
        status='confirmed'
    )
    return render(request, 'courses/receipt.html', {'enrollment': enrollment})