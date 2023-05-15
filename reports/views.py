from django.shortcuts import render
from django.db.models import Sum
from operations.models import Transactions, Cost, CostGroup, Safe
import datetime


def get_cash_balance_report(request):
    user_name = request.user.username
    total_balance_list = []
    all_user_safes = Safe.objects.filter(user_id=request.user.pk)
    for one_user_safe in all_user_safes:
        total_expenses = Transactions.objects.filter(user_id=request.user.pk,
                                                     safe_id=one_user_safe.id,
                                                     group_id__type_group=0).aggregate(total=Sum('sum_transactions'))
        total_incomes = Transactions.objects.filter(user_id=request.user.pk,
                                                    safe_id=one_user_safe.id,
                                                    group_id__type_group=1).aggregate(total=Sum('sum_transactions'))
        expenses = total_expenses['total'] or 0
        incomes = total_incomes['total'] or 0

        if expenses or incomes:
            balance = incomes - expenses
            total_balance_list.append({one_user_safe: balance})
    date = datetime.date.today()
    context = {'user_name': user_name, 'total_balance_list': total_balance_list, 'date': date}
    return render(request, 'get_cash_balance_report.html', context)


def select_period(request):
    user_name = request.user.username
    return render(request, 'select_period.html', {"user_name": user_name})


def get_costs_pie_chart(request):
    user_name = request.user.username
    start_date = request.POST.get('date_start')
    end_date = request.POST.get('date_finish')
    costs_expense = Cost.objects.filter(user_id=request.user.pk, cost_group_id__type_group=0)
    total_costs_expense = []
    for cost in costs_expense:
        cost_sum = Transactions.objects.filter(
            cost_id=cost.id, date__range=(start_date, end_date)).aggregate(total=Sum('sum_transactions'))
        cost_sum = cost_sum['total'] or 0
        if cost_sum:
            total_costs_expense.append({cost: cost_sum})
    context = {'user_name': user_name, 'total_costs_expense': total_costs_expense}
    return render(request, '.html', context)      #доделать этот эндпоинт и сделать темплейт






def get_report_cost(request):  # расходы по статьям
    pass


def get_all_reports(request):
    pass
