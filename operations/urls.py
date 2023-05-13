from django.urls import path
import operations.views

urlpatterns = [
    path('safe/', operations.views.create_safe),
    path('safe/<int:safe_id>/', operations.views.delete_safe),
    path('group_cost/', operations.views.create_group_cost),
    path('group_cost/<int:group_cost_id>/', operations.views.create_cost_from_group_cost),
    path('cost/', operations.views.create_cost),
    path('cost/<int:cost_id>/', operations.views.delete_cost),
    path('income/', operations.views.create_income),
    path('get_costs/', operations.views.get_costs, name='get_costs'),
    path('income/<int:income_id>/', operations.views.delete_income),
    path('expense/', operations.views.create_expense),
    path('expense/<int:expense_id>/', operations.views.delete_expense)
]

