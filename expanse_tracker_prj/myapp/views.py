from django.shortcuts import render, redirect
from .forms import ExpanseForm
from .models import Expanse
from users.models import Profile
import datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    if request.method == 'POST':
        expanse = ExpanseForm(request.POST)
        if expanse.is_valid():
            expanse.instance.user = request.user
            expanse.save()
    
    current_user = request.user
    expanses = Expanse.objects.filter(user=current_user)
    total_expanses = expanses.aggregate(Sum('amount'))
    
    # Logic to calculate 365 days expanses
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = Expanse.objects.filter(date__gte=last_year, user=current_user)
    yearly_sum = data.aggregate(Sum('amount'))
    
    # Logic to calculate 30 days expanses
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = Expanse.objects.filter(date__gte=last_month, user=current_user)
    monthly_sum = data.aggregate(Sum('amount'))
    
    # Logic to calculate 7 days expanses
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = Expanse.objects.filter(date__gte=last_week, user=current_user)
    weekly_sum = data.aggregate(Sum('amount'))
    
    
    daily_sums = Expanse.objects.filter(user=current_user).values('date').order_by('date').annotate(sum=Sum('amount'))
    
    # Categorical expanses
    categorical_sums = Expanse.objects.filter(user=current_user).values('category').order_by('category').annotate(sum=Sum('amount'))
    
    expanseform = ExpanseForm()
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    
    return render(request, "myapp/index.html", {
        'expanseform': expanseform,
        'expanses': expanses,
        'total_expanses': total_expanses,
        'yearly_sum': yearly_sum,
        'monthly_sum': monthly_sum,
        'weekly_sum': weekly_sum,
        'daily_sums': daily_sums,
        'categorical_sums':categorical_sums,
        'profile': profile
    })

def edit(request,id):
    if request.method == 'POST':
        expanse = Expanse.objects.get(id=id)
        form = ExpanseForm(request.POST, instance=expanse)
        if form.is_valid():
            form.save()
            return redirect("index")
        
    expanse = Expanse.objects.get(id=id)
    expanse_form = ExpanseForm(instance=expanse)
    return render(request, "myapp/edit.html",{ 'expanse_form': expanse_form})

def delete(request,id):
    if request.method == 'POST' and 'delete' in request.POST:
        expanse = Expanse.objects.get(id=id)
        expanse.delete()
    return redirect("index")

def home(request):
    return render(request, "myapp/home.html")