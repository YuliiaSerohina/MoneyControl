import datetime
from django.db.models import Sum
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from operations.models import Safe, Cost, CostGroup, Transactions
from django.core.paginator import Paginator


def create_safe(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            safe = Safe(name=request.POST.get('name'),
                        safe_type=request.POST.get('safe_type'),
                        currency=request.POST.get('currency'),
                        user_id=request.user.pk
                        )
            safe.save()
        else:
            return redirect('/operations/safe/')
    user_name = request.user.username
    user_safes = Safe.objects.filter(user_id=request.user.pk)
    pages_safes = Paginator(user_safes, 10)
    page_obj = pages_safes.page(pages_safes.num_pages)
    context = {'user_name': user_name, 'page_obj': page_obj}
    return render(request, 'create_safe.html', context)


def delete_safe(request, safe_id):
    if request.method == "POST":
        safe = Safe.objects.get(id=safe_id)
        safe.delete()
        return redirect('/operations/safe/')
    user_name = request.user.username
    safe = Safe.objects.filter(id=safe_id)
    context = {'user_name': user_name, 'safe': safe, 'safe_id': safe_id}
    return render(request, 'delete_safe.html', context)


def create_group_cost(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            cost_group = CostGroup(name=request.POST.get('name'),
                                   type_group=request.POST.get('type_group'),
                                   user_id=request.user.pk
                                   )
            cost_group.save()
        else:
            return redirect('/operations/group_cost/')
    user_name = request.user.username
    user_cost_groups = CostGroup.objects.filter(user_id=request.user.pk).order_by('name')
    pages = Paginator(user_cost_groups, 10)
    page_number = request.GET.get('page')
    page_obj = pages.get_page(page_number)
    context = {'user_name': user_name, 'page_obj': page_obj}
    return render(request, 'create_group_cost.html', context)


def create_cost(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            cost = Cost(name=request.POST.get('name'),
                        cost_group_id=CostGroup.objects.get(id=request.POST.get('cost_group_id')),
                        user_id=request.user.pk
                        )
            cost.save()
        else:
            return redirect('/operations/cost/')
    user_name = request.user.username
    get_user_cost_groups = CostGroup.objects.filter(user_id=request.user.pk)
    user_costs = Cost.objects.filter(user_id=request.user.pk).order_by('cost_group_id')
    pages = Paginator(user_costs, 10)
    page_number = request.GET.get('page')
    page_obj = pages.get_page(page_number)
    context = {'get_user_cost_groups': get_user_cost_groups, 'page_obj': page_obj, 'user_name': user_name}
    return render(request, 'create_cost.html', context)


def create_cost_from_group_cost(request, group_cost_id):
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            cost = Cost(user_id=request.user.pk,
                        name=request.POST.get('name'),
                        cost_group_id=CostGroup.objects.get(id=request.POST.get('cost_group_id'))
                        )
            cost.save()
        else:
            return redirect(f'/operations/group_cost/{group_cost_id}/')
    user_name = request.user.username
    costs_by_cost_group = Cost.objects.filter(cost_group_id=group_cost_id)
    pages = Paginator(costs_by_cost_group, 10)
    page_number = request.GET.get('page')
    page_obj = pages.get_page(page_number)
    group_info = CostGroup.objects.filter(id=group_cost_id)
    context = {'group_cost_id': group_cost_id, 'user_name': user_name, 'page_obj': page_obj, 'group_info': group_info}
    return render(request, 'create_cost_from_group_cost.html', context)


def delete_cost(request, cost_id):
    if request.method == 'POST':
        cost = Cost.objects.get(id=cost_id)
        cost.delete()
        return redirect('/operations/cost/')
    user_name = request.user.username
    view_cost = Cost.objects.filter(id=cost_id)
    context = {'user_name': user_name, 'view_cost': view_cost, 'cost_id': cost_id}
    return render(request, 'delete_cost.html', context)


def create_income(request):
    if request.method == "POST":
        date = request.POST.get('date')
        safe_id = request.POST.get('safe_id')
        group_id = request.POST.get('group_id')
        cost_id = request.POST.get('cost_id')
        sum_transactions = request.POST.get('sum')

        if not date or not safe_id or not group_id or not cost_id or not sum_transactions:
            error_message = 'Fill all fields'
            user_name = request.user.username
            safes_list = Safe.objects.filter(user_id=request.user.pk)
            safes_balance_list = []
            for safe in safes_list:
                safe_expenses = Transactions.objects.filter(
                    safe_id=safe.id, group_id__type_group=0).aggregate(total=Sum('sum_transactions'))
                safe_incomes = Transactions.objects.filter(
                    safe_id=safe.id, group_id__type_group=1).aggregate(total=Sum('sum_transactions'))
                safe_expenses = safe_expenses['total'] or 0
                safe_incomes = safe_incomes['total'] or 0
                balance = safe_incomes - safe_expenses
                safes_balance_list.append({safe: balance})
            groups_list = CostGroup.objects.filter(user_id=request.user.pk, type_group=1)
            user_incomes = Transactions.objects.filter(user_id=request.user.pk, group_id__type_group=1).order_by(
                '-date')
            pages = Paginator(user_incomes, 7)
            page_number = request.GET.get('page')
            page_obj = pages.get_page(page_number)
            context = {'user_name': user_name, 'safes_balance_list': safes_balance_list, 'groups_list': groups_list,
                       'page_obj': page_obj, 'error_message': error_message}
            return render(request, 'create_income.html', context)
        income = Transactions(user_id=request.user.pk,
                              date=date,
                              safe_id=Safe.objects.get(id=safe_id),
                              group_id=CostGroup.objects.get(id=group_id),
                              cost_id=Cost.objects.get(id=cost_id),
                              sum_transactions=sum_transactions
                              )
        income.save()
    user_name = request.user.username
    safes_list = Safe.objects.filter(user_id=request.user.pk)
    safes_balance_list = []
    for safe in safes_list:
        safe_expenses = Transactions.objects.filter(
            safe_id=safe.id, group_id__type_group=0).aggregate(total=Sum('sum_transactions'))
        safe_incomes = Transactions.objects.filter(
            safe_id=safe.id, group_id__type_group=1).aggregate(total=Sum('sum_transactions'))
        safe_expenses = safe_expenses['total'] or 0
        safe_incomes = safe_incomes['total'] or 0
        balance = safe_incomes - safe_expenses
        safes_balance_list.append({safe: balance})
    groups_list = CostGroup.objects.filter(user_id=request.user.pk, type_group=1)
    user_incomes = Transactions.objects.filter(user_id=request.user.pk, group_id__type_group=1).order_by('-date')
    pages = Paginator(user_incomes, 7)
    page_number = request.GET.get('page')
    page_obj = pages.get_page(page_number)
    context = {'user_name': user_name, 'safes_balance_list': safes_balance_list, 'groups_list': groups_list, 'page_obj': page_obj}
    return render(request, 'create_income.html', context)


def get_costs(request):
    group_id = request.GET.get('group_id')
    costs = Cost.objects.filter(cost_group_id=group_id, user_id=request.user.pk)
    data = [{'id': cost.id, 'name': cost.name} for cost in costs]
    return JsonResponse(data, safe=False)


def delete_income(request, income_id):
    if request.method == "POST":
        income = Transactions.objects.get(id=income_id)
        income.delete()
        return redirect('/operations/income/')
    user_name = request.user.username
    view_income = Transactions.objects.filter(id=income_id)
    context = {'user_name': user_name, 'view_income': view_income, 'income_id': income_id}
    return render(request, 'delete_income.html', context)


def create_expense(request):
    if request.method == "POST":
        date = request.POST.get('date')
        safe_id = request.POST.get('safe_id')
        group_id = request.POST.get('group_id')
        cost_id = request.POST.get('cost_id')
        sum_transactions = request.POST.get('sum')

        if not date or not safe_id or not group_id or not cost_id or not sum_transactions:
            error_message = 'Fill all fields'
            user_name = request.user.username
            safes_list = Safe.objects.filter(user_id=request.user.pk)
            safes_balance_list = []
            for safe in safes_list:
                safe_expenses = Transactions.objects.filter(
                    safe_id=safe.id, group_id__type_group=0).aggregate(total=Sum('sum_transactions'))
                safe_incomes = Transactions.objects.filter(
                    safe_id=safe.id, group_id__type_group=1).aggregate(total=Sum('sum_transactions'))
                safe_expenses = safe_expenses['total'] or 0
                safe_incomes = safe_incomes['total'] or 0
                balance = safe_incomes - safe_expenses
                safes_balance_list.append({safe: balance})
            groups_list = CostGroup.objects.filter(user_id=request.user.pk, type_group=0)
            user_incomes = Transactions.objects.filter(user_id=request.user.pk, group_id__type_group=0).order_by(
                '-date')
            pages = Paginator(user_incomes, 7)
            page_number = request.GET.get('page')
            page_obj = pages.get_page(page_number)
            context = {'user_name': user_name, 'safes_balance_list': safes_balance_list, 'groups_list': groups_list,
                       'page_obj': page_obj, 'error_message': error_message}
            return render(request, 'create_expense.html', context)
        expense = Transactions(user_id=request.user.pk,
                               date=date,
                               safe_id=Safe.objects.get(id=safe_id),
                               group_id=CostGroup.objects.get(id=group_id),
                               cost_id=Cost.objects.get(id=cost_id),
                               sum_transactions=sum_transactions
                               )
        expense.save()
    user_name = request.user.username
    safes_list = Safe.objects.filter(user_id=request.user.pk)
    safes_balance_list = []
    for safe in safes_list:
        safe_expenses = Transactions.objects.filter(
            safe_id=safe.id, group_id__type_group=0).aggregate(total=Sum('sum_transactions'))
        safe_incomes = Transactions.objects.filter(
            safe_id=safe.id, group_id__type_group=1).aggregate(total=Sum('sum_transactions'))
        safe_expenses = safe_expenses['total'] or 0
        safe_incomes = safe_incomes['total'] or 0
        balance = safe_incomes - safe_expenses
        safes_balance_list.append({safe: balance})
    groups_list = CostGroup.objects.filter(user_id=request.user.pk, type_group=0)
    user_expense = Transactions.objects.filter(user_id=request.user.pk, group_id__type_group=0).order_by('-date')
    pages = Paginator(user_expense, 7)
    page_number = request.GET.get('page')
    page_obj = pages.get_page(page_number)
    context = {'user_name': user_name, 'safes_balance_list': safes_balance_list, 'groups_list': groups_list, 'page_obj': page_obj}
    return render(request, 'create_expense.html', context)


def delete_expense(request, expense_id):
    if request.method == "POST":
        expense = Transactions.objects.get(id=expense_id)
        expense.delete()
        return redirect('/operations/expense/')
    user_name = request.user.username
    view_expense = Transactions.objects.filter(id=expense_id)
    context = {'user_name': user_name, 'view_expense': view_expense, 'expense_id': expense_id}
    return render(request, 'delete_expense.html', context)

