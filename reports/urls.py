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
    path('select_period_cost_to_income_ratio/', reports.views.select_period_cost_to_income_ratio),
    path('cost_to_income_ratio/', reports.views.get_cost_to_income_ratio),
    path('select_period_cost_group_structure/', reports.views.select_period_cost_group_structure),
    path('cost_group_structure/', reports.views.get_cost_group_structure),
    path('select_period_cash_flow/', reports.views.select_period_cash_flow),
    path('cash_flow/', reports.views.get_cash_flow),
    path('', reports.views.get_all_reports)
]
