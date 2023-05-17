from django.urls import path
import reports.views

urlpatterns = [
    path('balance/', reports.views.get_cash_balance_report),
    path('period_costs_pie_chart/', reports.views.select_period_costs_pie_chart),
    path('costs_pie_chart/', reports.views.get_costs_pie_chart),
    path('period_group_costs_pie_chart/', reports.views.select_period_group_costs_pie_chart),
    path('group_costs_pie_chart/', reports.views.get_group_costs_pie_chart),
    path('period_top_costs/', reports.views.select_period_top_costs),
    path('top_costs/', reports.views.get_top_costs),
    path('', reports.views.get_all_reports)
]
