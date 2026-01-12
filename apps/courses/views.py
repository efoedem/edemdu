from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Enrollment
from .forms import EnrollmentForm


def course_list(request):
    courses = Course.objects.all().select_related('category')

    levels = ['100', '200', '300', '400']
    organized_courses = {}

    for level in levels:
        level_courses = courses.filter(level=level)

        schools = {}
        for course in level_courses:
            school_name = course.category.title
            if school_name not in schools:
                schools[school_name] = []
            schools[school_name].append(course)

        # Only add the level to the dictionary if it has courses or schools
        if schools:
            organized_courses[level] = schools

    # Note the context name: 'organized_data'
    return render(request, 'courses/course_list.html', {'organized_data': organized_courses})

def course_detail(request, pk):
    """Displays details for a specific course."""
    course = get_object_or_404(Course, pk=pk)
    # Since we aren't using login, we set is_enrolled to False
    # as we can't track guest users easily here.
    return render(request, 'courses/course_detail.html', {'course': course, 'is_enrolled': False})


def manual_payment(request, pk):
    course = get_object_or_404(Course, pk=pk)

    # 1. CHECK IF SESSION ALREADY HAS AN ENROLLMENT FOR THIS COURSE
    session_key = f'enrollment_{pk}'
    if session_key in request.session:
        enrollment_id = request.session[session_key]
        enrollment = Enrollment.objects.filter(id=enrollment_id).first()
        if enrollment:
            # If they already submitted, keep them on the waiting page
            return render(request, 'courses/waiting_confirmation.html', {'enrollment': enrollment})

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            if request.user.is_authenticated:
                enrollment.user = request.user
            enrollment.course = course
            enrollment.save()

            # 2. SAVE ENROLLMENT ID TO SESSION
            # This "remembers" the user even without a login
            request.session[session_key] = enrollment.id

            # Email logic here...
            return render(request, 'courses/waiting_confirmation.html', {'enrollment': enrollment})
    else:
        form = EnrollmentForm()

    return render(request, 'courses/manual_payment.html', {'course': course, 'form': form})

def download_receipt(request, enrollment_id):
    """Allows student to view/download receipt by ID without requiring login."""
    # We removed user=request.user so the link works for guests
    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
        status='confirmed'
    )
    return render(request, 'courses/receipt.html', {'enrollment': enrollment})

# Note: student_dashboard is removed as it requires a login to track "My Courses"