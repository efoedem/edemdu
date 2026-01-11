from django.contrib import admin, messages
from django.utils.html import format_html
from urllib.parse import quote
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Count, Sum, Q
from openpyxl import Workbook  # Ensure 'pip install openpyxl' is run
from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'course', 'reference_id', 'status', 'whatsapp_action', 'delete_button')
    list_editable = ('status',)
    search_fields = ('full_name', 'index_number', 'reference_id')
    actions = ['export_to_excel']

    # --- Summary Dashboard Logic ---
    def changelist_view(self, request, extra_context=None):
        stats = Enrollment.objects.aggregate(
            total_count=Count('id'),
            confirmed_count=Count('id', filter=Q(status='confirmed')),
            # This assumes your Course model has a 'price' field
            total_revenue=Sum('course__price', filter=Q(status='confirmed'))
        )
        extra_context = extra_context or {}
        extra_context['stats'] = stats
        return super().changelist_view(request, extra_context=extra_context)

    # --- Excel Export Logic ---
    def export_to_excel(self, request, queryset):
        wb = Workbook()
        ws = wb.active
        ws.title = "Enrollments"
        ws.append(['Full Name', 'Course', 'Index Number', 'WhatsApp', 'Transaction ID', 'Status'])

        for obj in queryset:
            ws.append(
                [obj.full_name, obj.course.title, obj.index_number, obj.whatsapp_number, obj.reference_id, obj.status])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=enrollments.xlsx'
        wb.save(response)
        return response

    export_to_excel.short_description = "📊 Export Selected to Excel"

    def whatsapp_action(self, obj):
        if obj.status == 'confirmed' and obj.whatsapp_number:
            raw_phone = str(obj.whatsapp_number).replace('+', '').replace(' ', '').replace('-', '')
            phone = '233' + raw_phone[1:] if raw_phone.startswith('0') else raw_phone
            receipt_url = f"http://127.0.0.1:8001/receipt/{obj.id}/"
            message = f"Hello *{obj.full_name}*,\n\nYour payment for *{obj.course.title}* is confirmed! ✅\n\nDownload receipt:\n{receipt_url}"
            url = f"https://api.whatsapp.com/send?phone={phone}&text={quote(message)}"
            return format_html(
                '<a href="{}" target="_blank" style="background-color: #25D366; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none; font-weight: bold;">Send WhatsApp</a>',
                url)
        return format_html('<small style="color: gray;">Confirm status first</small>')

    def delete_button(self, obj):
        delete_url = reverse('admin:courses_enrollment_delete', args=[obj.id])
        return format_html(
            '<a href="{}" style="background-color: #d9534f; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none; font-size: 11px;">Remove</a>',
            delete_url)

    delete_button.short_description = 'Remove Student'
    whatsapp_action.short_description = 'WhatsApp Action'