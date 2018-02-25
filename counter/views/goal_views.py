from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from counter.models import Goal, GoalForm
from django.contrib.auth.decorators import login_required
@login_required
def newGoal(request):

    if request.method == 'GET':
        form = GoalForm()
    else:
        form = GoalForm(data=request.POST)
        currGoals = Goal.objects.all()

        if form.is_valid():
            newGoal = form.save(commit=False)

            if not newGoal.calories:
                newGoal.calories = 0.00
            if not newGoal.carbohydrates:
                newGoal.carbohydrates = 0.00
            if not newGoal.protein:
                newGoal.protein = 0.00
            if not newGoal.fats:
                newGoal.fats = 0.00

            if not currGoals:
                newGoal.isActive = True
            else:
                if (newGoal.isActive is True):
                    for g in currGoals:
                        g.isActive = False
                        g.save()
            newGoal.save()
            messages.success(request, "Goal successfully added.")
            return redirect('counter:index')
    context = {'form' : form }
    return render(request, 'counter/new_goal.html', context=context)

@login_required
def viewGoals(request):
    if request.method == 'GET':
        allGoals = Goal.objects.order_by('-dateAdded')
        hasGoal = True
        hasActiveGoal = True
        if not allGoals:
            hasGoal = False
        try:
            activeGoal = Goal.objects.get(isActive=True)
        except ObjectDoesNotExist:
            hasActiveGoal = False
        context = {
            'allGoals' : allGoals,
            'hasGoal' : hasGoal,
            'hasActiveGoal' : hasActiveGoal,
        }
        if hasActiveGoal:
            context.update({'activeGoal' : activeGoal})
        return render(request, 'counter/view_goals.html', context=context)
    else:
        Goal.objects.filter(isActive=True).update(isActive=False)
        Goal.objects.filter(pk=request.POST['activeButton']).update(isActive=True)
        set = Goal.objects.all()
        for s in set:
            s.save()
        return redirect('counter:viewGoals')

@login_required
def deleteGoal(request, pk):
    try:
        deletedGoal = Goal.objects.get(id=pk)
    except ObjectDoesNotExist:
        messages.warning(request, "Goal cannot be deleted. Try again.")
        return redirect('counter:viewGoals')
    deletedGoal.delete()
    messages.success(request, "Goal successfully deleted.")
    return redirect('counter:viewGoals')

@login_required
def editGoal(request, pk):
    toBeEdited = Goal.objects.get(id=pk)
    if request.method == 'GET':
        form=GoalForm(instance=toBeEdited)
        context = {
            'form' : form,
            'toBeEdited' : toBeEdited,
        }
        return render(request, 'counter/edit_goal.html', context=context)
    else:
        form = GoalForm(instance=toBeEdited, data=request.POST)
        fields = ['calories', 'protein', 'carbohydrates', 'fats']
        currGoals = Goal.objects.all()
        if form.is_valid():
            editedGoal = form.save(commit=False)

            if not editedGoal.calories:
                editedGoal.calories = 0.00
            if not editedGoal.carbohydrates:
                editedGoal.carbohydrates = 0.00
            if not editedGoal.protein:
                editedGoal.protein = 0.00
            if not editedGoal.fats:
                editedGoal.fats = 0.00

            if (editedGoal.isActive is True):
                for g in currGoals:
                    if (g.id is not editedGoal.id):
                        g.isActive = False
                        g.save()
            editedGoal.save()
            messages.success(request, "Goal successfully edited.")
            return redirect('counter:index')

