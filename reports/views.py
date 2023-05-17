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


def select_period_costs_pie_chart(request):
    user_name = request.user.username
    return render(request, 'select_period_costs_pie_chart.html', {"user_name": user_name})


def get_costs_pie_chart(request):
    user_name = request.user.username
    start_date = request.POST.get('date_start')
    end_date = request.POST.get('date_finish')
    costs_expense = Cost.objects.filter(user_id=request.user.pk, cost_group_id__type_group=0)
    currency_all = Transactions.objects.filter(user_id=request.user.pk).values_list\
        ('safe_id__currency', flat=True).distinct()
    total_costs_expense = []
    for currency in currency_all:
        one_cost_sum = []
        for cost in costs_expense:
            cost_sum = Transactions.objects.filter(
                cost_id=cost.id, date__range=(start_date, end_date), safe_id__currency=currency).aggregate(total=Sum('sum_transactions'))
            cost_sum = cost_sum['total'] or 0
            if cost_sum:
                one_cost_sum.append({cost: cost_sum})
        total_costs_expense.append({currency: one_cost_sum})
    context = {'user_name': user_name,
               'total_costs_expense': total_costs_expense,
               'start_date': start_date,
               'end_date': end_date}
    return render(request, 'get_costs_pie_chart.html', context)


def select_period_group_costs_pie_chart(request):
    user_name = request.user.username
    return render(request, 'select_period_group_costs_pie_chart.html', {"user_name": user_name})


def get_group_costs_pie_chart(request):
    user_name = request.user.username
    start_date = request.POST.get('date_start')
    end_date = request.POST.get('date_finish')
    group_costs_expense = CostGroup.objects.filter(user_id=request.user.pk, type_group=0)
    currency_all = Transactions.objects.filter(user_id=request.user.pk).values_list\
        ('safe_id__currency', flat=True).distinct()
    total_group_costs_expense = []
    for currency in currency_all:
        one_group_cost_sum = []
        for group_costs in group_costs_expense:
            group_costs_sum = Transactions.objects.filter(
                group_id=group_costs.id, date__range=(start_date, end_date),
                safe_id__currency=currency).aggregate(total=Sum('sum_transactions'))
            group_costs_sum = group_costs_sum['total'] or 0
            if group_costs_sum:
                one_group_cost_sum.append({group_costs: group_costs_sum})
        total_group_costs_expense.append({currency: one_group_cost_sum})
    context = {'user_name': user_name, 'start_date': start_date,
               'end_date': end_date, 'total_group_costs_expense': total_group_costs_expense}
    return render(request, 'get_group_costs_pie_chart.html', context)


def select_period_top_costs(request):
    user_name = request.user.username
    return render(request, 'select_period_top_costs.html', {"user_name": user_name})


def get_top_costs(request):
    user_name = request.user.username
    start_date = request.POST.get('date_start')
    end_date = request.POST.get('date_finish')
    costs_expense = Cost.objects.filter(user_id=request.user.pk, cost_group_id__type_group=0)
    currency_all = Transactions.objects.filter(user_id=request.user.pk).values_list \
        ('safe_id__currency', flat=True).distinct()
    total_costs_expense = []
    for currency in currency_all:
        one_cost_sum = []
        for cost in costs_expense:
            cost_sum = Transactions.objects.filter(
                cost_id=cost.id, date__range=(start_date, end_date), safe_id__currency=currency).aggregate(total=Sum('sum_transactions'))
            cost_sum = cost_sum['total'] or 0
            if cost_sum:
                one_cost_sum.append({cost: cost_sum})
        sorted_costs_list = sorted(one_cost_sum, key=lambda x: list(x.values())[0])
        total_costs_expense.append({currency: sorted_costs_list})
    context = {'user_name': user_name, 'total_costs_expense': total_costs_expense,
               'start_date': start_date, 'end_date': end_date}
    return render(request, 'get_top_costs.html', context)






def get_all_reports(request):
    pass
