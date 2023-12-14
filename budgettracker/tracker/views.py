from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.http import JsonResponse
from .models import Budget, Expense
from .forms import BudgetForm, ExpenseForm
import json

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'profile')
            return redirect(next_url)    
        else:
            form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('welcome_screen')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def welcome_screen(request):
    return render(request, 'tracker/welcome_screen.html')

def profile(request):
    return render(request, 'tracker/profile.html', {'user': request.user})

def budget_list(request):
    budgets = Budget.objects.all()
    return render(request, 'tracker/budget_list.html', {'budgets': budgets})


def expenses(request, budget_id):
    budget = Budget.objects.get(pk=budget_id)
    expenses = Expense.objects.filter(budget=budget)
    total_expenses = budget.total_expenses()
    remaining_budget = budget.amount - total_expenses

    chart_data = {
        'labels': [expense.name for expense in expenses],
        'data': [float(expense.amount) for expense in expenses],
    }

    # Render the pie chart data to a JSON script
    #chart_data_json = render_to_string('tracker/pie_chart_data.json', {'chart_data': chart_data})
    chart_data_json = json.dumps(chart_data)

    return render(request, 'tracker/expenses.html', {
        'budget': budget,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'remaining_budget': remaining_budget,
        'chart_data_json': chart_data_json,
    })

def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'tracker/add_budget.html', {'form': form})


def add_expense(request, budget_id):
    budget = Budget.objects.get(pk=budget_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.budget = budget
            expense.save()
            return redirect('expenses', budget_id=budget_id)
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form, 'budget': budget})

def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, pk=budget_id)
    if request.method == 'POST':
        budget.delete()
        return redirect('budget_list')
    return render(request, 'tracker/delete_budget.html', {'budget': budget})

def delete_expense(request, budget_id, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if request.method == 'POST':
        expense.delete()
        return redirect('expenses', budget_id=budget_id)
    return render(request, 'tracker/delete_expense.html', {'expense': expense})