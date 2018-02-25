from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from counter.models import Meal, MealForm, Entry, SearchForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import sys
import requests

#APIKEY AND ID HERE
#

APIENDPOINT = ("https://api.nutritionix.com/v1_1/")
SEARCH = "search/"
ITEM = "item?"
QUERY = ""
RESULTFORMAT = "?results=0%3A20"
FIELDS = "&fields=item_name%2Cbrand_name%2Citem_id%2Cbrand_id%2Cnf_serving_weight_grams%2Cnf_total_fat%2Cnf_protein%2Cnf_total_carbohydrate%2Cnf_calories"
IDSTRING = ""
ID = "id="
APIURL = "&appId="+APPID + "&appKey=" + APPKEY

class NewMeal(LoginRequiredMixin, CreateView):
    form_class = MealForm
    template_name = 'counter/new_meal.html'
    success_url = reverse_lazy('counter:index')
    mealTime = Entry.BREAKFAST.title()
    def get_context_data(self, **kwargs):
        context = super(NewMeal, self).get_context_data(**kwargs)
        context['type'] = self.mealTime
        return context
    def form_valid(self, form):
        newMeal = form.save(commit=False)
        if not newMeal.caloriesPerServing:
            newMeal.caloriesPerServing = 0.00
        if not newMeal.proteinPerServing:
            newMeal.proteinPerServing = 0.00
        if not newMeal.carbohydratesPerServing:
            newMeal.carbohydratesPerServing = 0.00
        if not newMeal.fatsPerServing:
            newMeal.fatsPerServing = 0.00
        newMeal.save()
        self.object = newMeal
        messages.success(self.request, "Meal successfully added.")
        if 'SaveAndAddEntry' in self.request.POST:
            return HttpResponseRedirect(reverse_lazy('counter:newEntry' + self.mealTime))
        return HttpResponseRedirect(self.get_success_url())

class NewMealLunch(NewMeal):
    mealTime = Entry.LUNCH.title()

class NewMealBreakfast(NewMeal):
    mealTime = Entry.BREAKFAST.title()

class NewMealDinner(NewMeal):
    mealTime = Entry.DINNER.title()

class NewMealSnack(NewMeal):
    mealTime = Entry.SNACK.title()

@login_required
def getMealDatabase(request):
    context = {
    }
    if request.method == 'POST':
        searchForm = SearchForm(request.POST)
        if searchForm.is_valid():
            QUERY = searchForm.cleaned_data['searchQuery']
            response = requests.get(APIENDPOINT + SEARCH + QUERY + RESULTFORMAT + FIELDS + APIURL)
            data = response.json()
            meals = data['hits']
            context.update(
                {'meals' : meals,
                 }
            )
    else:
        searchForm = SearchForm()
    context.update(
        {'searchForm':searchForm,
        }
    )
    return render(request, 'counter/search.html', context=context)
@login_required
def newMealDatabase(request, id):
    if request.method == 'POST':
        IDSTRING = str(id)
        response = requests.get(APIENDPOINT + ITEM + ID + IDSTRING + APIURL)
        data = response.json()

        thisName = data["item_name"] + ", " + data["brand_name"]
        thisServingSize = 1
        thisUnits = "unit"
        if data["nf_serving_weight_grams"]:
            thisServingSize =  data["nf_serving_weight_grams"]
            thisUnits = "grams"

        thisCalories = 0 if not data["nf_calories"] else data["nf_calories"]
        thisProtein = 0 if not data["nf_protein"] else data["nf_protein"]
        thisCarbs = 0 if not data["nf_total_carbohydrate"] else data["nf_total_carbohydrate"]
        thisFats = 0 if not data["nf_total_fat"] else data["nf_total_fat"]

        newMeal = Meal(name = thisName, servingSize = thisServingSize, units=thisUnits, caloriesPerServing = thisCalories, proteinPerServing = thisProtein, carbohydratesPerServing = thisCarbs, fatsPerServing = thisFats)
        newMeal.save()
        if 'SaveAndEdit' in request.POST:
            return redirect('counter:editMeal', pk=newMeal.pk)
        return redirect('counter:index')
    else:
        #return 404
        pass
@login_required
def viewMeals(request):
    if request.method == 'GET':
        allMeals = Meal.objects.order_by('name')
        hasMeal = True
        if not allMeals:
            hasMeal = False
        context = {
            'allMeals' : allMeals,
            'hasMeal' : hasMeal,
        }
        return render(request, 'counter/view_meals.html', context=context)
@login_required
def deleteMeal(request, pk):
    try:
        deletedMeal = Meal.objects.get(id=pk)
    except ObjectDoesNotExist:
        messages.warning(request, "Meal cannot be deleted. Try again.")
        return redirect('counter:viewMeals')
    deletedMeal.delete()
    messages.success(request, "Meal successfully deleted.")
    return redirect('counter:viewMeals')
@login_required
def editMeal(request, pk):
    toBeEdited = Meal.objects.get(id=pk)
    if request.method == 'GET':
        form=MealForm(instance=toBeEdited)
    else:
        form = MealForm(instance=toBeEdited, data=request.POST)
        if form.is_valid():
            editedMeal = form.save(commit=False)
            if not editedMeal.caloriesPerServing:
                editedMeal.caloriesPerServing = 0.00
            if not editedMeal.carbohydratesPerServing:
                editedMeal.carbohydratesPerServing = 0.00
            if not editedMeal.proteinPerServing:
                editedMeal.proteinPerServing = 0.00
            if not editedMeal.fatsPerServing:
                editedMeal.fatsPerServing = 0.00
            editedMeal.save()
            messages.success(request, "Meal successfully edited.")
            return redirect('counter:index')
    context = {
        'form' : form,
        'toBeEdited' : toBeEdited
    }
    return render(request, 'counter/edit_meal.html', context=context)


