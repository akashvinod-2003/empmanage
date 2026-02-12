from datetime import date
from django.db.models import Q
from decimal import Decimal
from .models import AttendanceRecord, LeaveRequest, User


def attendance_flag(employee, month=None):
    records = AttendanceRecord.objects.filter(
        employee=employee, review_status=AttendanceRecord.REVIEW_APPROVED
    )
    if month:
        month_start = month.replace(day=1)
        if month.month == 12:
            month_end = month.replace(year=month.year + 1, month=1, day=1)
        else:
            month_end = month.replace(month=month.month + 1, day=1)
        records = records.filter(date__gte=month_start, date__lt=month_end)

    late_count = records.filter(status=AttendanceRecord.STATUS_LATE).count()
    absent_count = records.filter(status=AttendanceRecord.STATUS_ABSENT).count()

    if late_count > 4:
        return 'Frequently Late'
    if absent_count >= 3 and late_count >= 3:
        return 'Irregular Attendance'
    return 'Stable Attendance'


def _team_available(employee, start_date, end_date):
    if not employee.department:
        return True
    team_members = User.objects.filter(department=employee.department).exclude(id=employee.id)
    if not team_members.exists():
        return True

    overlapping = LeaveRequest.objects.filter(
        employee__in=team_members,
        status=LeaveRequest.STATUS_APPROVED,
    ).filter(Q(start_date__lte=end_date) & Q(end_date__gte=start_date))

    return team_members.count() - overlapping.values('employee').distinct().count() >= 1


def leave_recommendation(leave_request):
    if leave_request.employee.leave_balance >= leave_request.total_days and _team_available(
        leave_request.employee, leave_request.start_date, leave_request.end_date
    ):
        return 'Suggest Approve'
    return 'Suggest Review'


def payslip_summary(salary_record):
    base = salary_record.base_salary or Decimal('0.00')
    final = salary_record.final_salary or Decimal('0.00')
    deduction = max(base - final, Decimal('0.00'))
    deduction_rate = (deduction / base * Decimal('100')) if base else Decimal('0.00')

    insights = []
    warnings = []

    if deduction == 0:
        headline = 'Full payout expected for this month.'
        insights.append('No attendance deductions were applied.')
    elif deduction_rate >= Decimal('20'):
        headline = 'Significant deductions detected this month.'
    else:
        headline = 'Minor deductions applied to this month.'

    if salary_record.absent_days:
        insights.append(f'{salary_record.absent_days} day(s) marked absent.')
    if salary_record.late_days:
        insights.append(f'{salary_record.late_days} day(s) marked late.')

    if not insights:
        insights.append('Attendance signals are stable for this period.')

    if salary_record.anomaly_flag:
        warnings.append('Salary changed by more than 30% compared to last month.')

    if deduction > 0:
        warnings.append(
            f'Deduction total: {deduction:.2f} ({deduction_rate:.1f}% of base pay).'
        )

    return {
        'headline': headline,
        'insights': insights,
        'warnings': warnings,
        'deduction': deduction,
        'deduction_rate': deduction_rate,
    }
