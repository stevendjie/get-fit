from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from counter.models import Goal, GoalForm, Entry, Meal
from django.contrib.auth.decorators import login_required

def toBase(toConvert, toConvertUnits, stateOfOunces=None):
    solidUnits = [Entry.GR, Entry.KG, Entry.LB]
    liquidUnits = [Entry.L, Entry.ML, Entry.CUP]
    if stateOfOunces == 'solid':
        solidUnits.append(Entry.OZ)
    elif stateOfOunces == 'liquid':
        liquidUnits.append(Entry.OZ)
    if any(toConvertUnits in unit for unit in solidUnits):#base is grams
        if toConvertUnits == Entry.GR:
            return toConvert
        elif toConvertUnits == Entry.KG:
            return toConvert*1000
        elif toConvertUnits == Entry.LB:
            return toConvert*453.592
        else:
            return toConvert*28.3495
    elif any(toConvertUnits in unit for unit in liquidUnits):#base is milliliters
        if toConvertUnits == Entry.ML:
            return toConvert
        elif toConvertUnits == Entry.CUP:
            return toConvert*236.588
        elif toConvertUnits == Entry.L:
            return toConvert*1000
        else:
            return toConvert*29.5735
    else:
        return toConvert

@login_required
def index(request):
    if request.method == 'GET':
        hasGoal = True
        hasActiveGoal = True
        allGoals = Goal.objects.all()
        if not allGoals:
            hasGoal = False
        try:
            activeGoal = Goal.objects.get(isActive=True)
        except ObjectDoesNotExist:
            hasActiveGoal = False

        breakfastEntries = Entry.objects.filter(mealType=Entry.BREAKFAST)
        lunchEntries = Entry.objects.filter(mealType=Entry.LUNCH)
        dinnerEntries = Entry.objects.filter(mealType=Entry.DINNER)
        snackEntries = Entry.objects.filter(mealType=Entry.SNACK)
        context = {
            'hasGoal' : hasGoal,
            'hasActiveGoal' : hasActiveGoal,
            'allGoals' : allGoals,
            'lunchEntries' : lunchEntries,
            'breakfastEntries' : breakfastEntries,
            'dinnerEntries' : dinnerEntries,
            'snackEntries' : snackEntries,
        }
        if hasActiveGoal:
            context.update({'activeGoal' : activeGoal})

        entries = Entry.objects.all()

        currCalories = 0
        currCarbs = 0
        currProtein = 0
        currFats = 0
        for entry in entries:
            ratio = 0
            if entry.units == entry.SERV:#serving
                ratio = float(entry.amount)
            else:#units
                mealAmount = toBase(float(entry.meal.servingSize), entry.meal.units)
                entryAmount = toBase(float(entry.amount), entry.units)
                ratio = float(entryAmount)/float(mealAmount)
            currCalories += float(entry.meal.caloriesPerServing) * ratio
            currCarbs += float(entry.meal.carbohydratesPerServing) * ratio
            currProtein += float(entry.meal.proteinPerServing) * ratio
            currFats += float(entry.meal.fatsPerServing) * ratio

        isCalorieNegative = False
        isCarbNegative = False
        isFatNegative = False
        isProteinNegative = False

        remCalories = float(activeGoal.calories) - currCalories
        if remCalories < 0:
            isCalorieNegative = True
            remCalories *= -1;
        remProtein = float(activeGoal.protein) - currProtein
        if remProtein < 0:
            isProteinNegative = True
            remProtein *= -1;
        remCarbs = float(activeGoal.carbohydrates) - currCarbs
        if remCarbs < 0:
            isCarbNegative = True
            remCarbs *= -1;
        remFats = float(activeGoal.fats) - currFats
        if remFats < 0:
            isFatNegative = True
            remFats *= -1;

        context.update(
            {'currCalories': int(round(currCalories)),
             'isCalorieNegative' : isCalorieNegative,
             'remCalories' : int(round(remCalories)),
             'currCarbs': int(round(currCarbs)),
             'isCarbNegative': isCarbNegative,
             'remCarbs': int(round(remCarbs)),
             'currProtein': int(round(currProtein)),
             'isProteinNegative': isProteinNegative,
             'remProtein': int(round(remProtein)),
             'currFats': int(round(currFats)),
             'isFatNegative': isFatNegative,
             'remFats': int(round(remFats)),
             }
        )

        return render(request, 'counter/index.html', context=context)
    else:
        Goal.objects.filter(isActive=True).update(isActive=False)
        Goal.objects.filter(pk=request.POST['dropdown']).update(isActive=True)
        set = Goal.objects.all()
        for s in set:
            s.save()
        return redirect('counter:index')
