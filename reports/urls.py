from django.urls import path
import reports.views

urlpatterns = [
    path('balance/', reports.views.get_cash_balance_report),
    path('period_costs_pie_chart/', reports.views.select_period),
    path('costs_pie_chart/', reports.views.get_costs_pie_chart),
    path('cost/', reports.views.get_report_cost),
    path('', reports.views.get_all_reports)
]
