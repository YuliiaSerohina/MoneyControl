from django.urls import path
import reports.views

urlpatterns = [
    path('balance/', reports.views.get_cash_balance_report),
    path('cost_by_groups/', reports.views.get_report_cost_by_groups),
    path('cost/', reports.views.get_report_cost),
    path('', reports.views.get_all_reports)
]
