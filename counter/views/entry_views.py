from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView
from counter.models import Goal, GoalForm, Entry, EntryForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class NewEntry(LoginRequiredMixin, CreateView):
    form_class = EntryForm
    template_name = 'counter/new_entry.html'
    success_url = reverse_lazy('counter:index')

    def form_valid(self, form):
        invalid = False
        singularUnits = ['scoop', 'piece', 'can', 'unit']
        solidUnits = ['grams', 'kilograms', 'pounds']
        liquidUnits = ['liters', 'milliliters', 'cup']

        if any(form.instance.units in u for u in singularUnits):
            if form.instance.units != form.instance.meal.units:
                invalid = True
        elif any(form.instance.units in s1 for s1 in solidUnits):
            if not any(form.instance.meal.units in s2 for s2 in solidUnits):
                invalid = True
        elif any(form.instance.units in l1 for l1 in liquidUnits):
            if not any(form.instance.meal.units in l2 for l2 in liquidUnits):
                invalid = True
        elif form.instance.units == 'ounces':
            if any(form.instance.meal.units in u for u in singularUnits):
                invalid = True
        if invalid:
            messages.error(self.request, "Could not convert " + form.instance.units + " to " + form.instance.meal.units + ". Make sure to use the correct units.")
            return super(NewEntry, self).form_invalid(form)
        messages.success(self.request, "Entry successfully added.")
        form.instance.save()
        return super(NewEntry, self).form_valid(form)

class NewEntryLunch(NewEntry):
    def get_initial(self):
        initial = super(NewEntry, self).get_initial()
        initial['mealType'] = Entry.LUNCH
        return initial

class NewEntryBreakfast(NewEntry):
    def get_initial(self):
        initial = super(NewEntry, self).get_initial()
        initial['mealType'] = Entry.BREAKFAST
        return initial

class NewEntryDinner(NewEntry):
    def get_initial(self):
        initial = super(NewEntry, self).get_initial()
        initial['mealType'] = Entry.DINNER
        return initial

class NewEntrySnack(NewEntry):
    def get_initial(self):
        initial = super(NewEntry, self).get_initial()
        initial['mealType'] = Entry.SNACK
        return initial

@login_required
def editEntry(request, pk):
    toBeEdited = Entry.objects.get(id=pk)
    if request.method == 'GET':
        form = EntryForm(instance=toBeEdited)
    else:
        form = EntryForm(instance=toBeEdited, data=request.POST)
        if form.is_valid():
            editedEntry = form.save(commit=False)
            if not editedEntry.caloriesPerServing:
                editedEntry.caloriesPerServing = 0.00
            if not editedEntry.carbohydratesPerServing:
                editedEntry.carbohydratesPerServing = 0.00
            if not editedEntry.proteinPerServing:
                editedEntry.proteinPerServing = 0.00
            if not editedEntry.fatsPerServing:
                editedEntry.fatsPerServing = 0.00
            editedEntry.save()
            messages.success(request, "Entry successfully edited.")
            return redirect('counter:index')
    context = {
        'form': form,
        'toBeEdited': toBeEdited
    }
    return render(request, 'counter/edit_entry.html', context=context)