from django.db import models
from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
class Goal(models.Model):
   protein = models.DecimalField(max_digits=15, decimal_places=2)
   carbohydrates = models.DecimalField(max_digits=15, decimal_places=2)
   fats = models.DecimalField(max_digits=15, decimal_places=2)
   calories = models.DecimalField(max_digits=15, decimal_places=2)
   name = models.CharField(max_length=200, blank=False)
   isActive = models.BooleanField(default=False)
   dateAdded = models.DateTimeField(auto_now=True, null=True)

   def __str__(self):
       return 'Protein:' + str(self.protein) + '-' + 'Carbs:' + str(self.carbohydrates) + '-' + 'Fats:' + str(self.fats) + '-' + 'Calories:' +  str(self.calories) + '-' + self.name


class Meal(models.Model):
    name = models.CharField(max_length=300, blank=False)
    servingSize = models.DecimalField(max_digits=15, decimal_places=5, blank=False)
    GR = 'grams'
    OZ = 'ounces'
    KG = 'kilograms'
    LB = 'pounds'
    ML = 'milliliters'
    L = 'liters'
    CUP = 'cup'
    SCOOP = 'scoop'
    PIECE = 'piece'
    CAN = 'can'
    UNIT = 'unit'
    UNITS_CHOICES = (
        (GR, 'Grams'),
        (OZ, 'Ounces'),
        (KG, 'KIlograms'),
        (LB, 'Pounds'),
        (ML, 'Milliliters'),
        (L, 'Liters'),
        (CUP, 'Cup'),
        (SCOOP, 'Scoop'),
        (PIECE, 'Piece'),
        (CAN, 'Can'),
        (UNIT, 'Unit')
    )
    units = models.CharField(
        max_length=15,
        choices=UNITS_CHOICES,
        default=GR,
        blank=False,
    )
    caloriesPerServing = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Calories Per Serving'))
    proteinPerServing = models.DecimalField(max_digits=15, decimal_places=2)
    carbohydratesPerServing = models.DecimalField(max_digits=15, decimal_places=2)
    fatsPerServing = models.DecimalField(max_digits=15, decimal_places=2)
    dateTimeAdded = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return (self.name + " - " + str(int(round(self.caloriesPerServing))) + " cals - Protein: " + str(int(round(self.proteinPerServing))) + "g - Carbs: "
        + str(int(round(self.carbohydratesPerServing))) + "g - Fats: " + str(int(round(self.fatsPerServing))) + "g")


class Entry(models.Model):
    meal = models.ForeignKey(Meal, null=True, on_delete=models.SET_NULL, blank=False)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=False)
    GR = 'grams'
    OZ = 'ounces'
    KG = 'kilograms'
    LB = 'pounds'
    ML = 'milliliters'
    L = 'liters'
    CUP = 'cup'
    SCOOP = 'scoop'
    PIECE = 'piece'
    CAN = 'can'
    SERV = 'serving'
    UNIT = 'unit'
    UNITS_CHOICES = (
        (GR, 'Grams'),
        (OZ, 'Ounces'),
        (KG, 'KIlograms'),
        (LB, 'Pounds'),
        (ML, 'Milliliters'),
        (L, 'Liters'),
        (CUP, 'Cup'),
        (SCOOP, 'Scoop'),
        (PIECE, 'Piece'),
        (CAN, 'Can'),
        (SERV, 'Serving')
    )
    units = models.CharField(
        max_length=15,
        choices=UNITS_CHOICES,
        default=GR,
        blank=False,
    )
    dateTimeAdded = models.DateTimeField(auto_now_add=False, null=False)
    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'
    SNACK = 'snack'
    TYPE_CHOICES = (
        (BREAKFAST, 'Breakfast'),
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
        (SNACK, 'Snack'),
    )
    mealType = models.CharField(
        max_length=15,
        choices=TYPE_CHOICES,
        default=BREAKFAST,
    )

class GoalForm(ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'calories', 'protein', 'carbohydrates', 'fats', 'isActive']
        labels = {
            'name' : 'Name',
            'calories' : 'Calories (cals)',
            'protein' : 'Protein (grams)',
            'carbohydrates' : 'Carbohydrates (grams)',
            'fats' : 'Fats (grams)',
            'isActive' : 'Set As Active'
        }
        help_texts = {
            'name': 'Is this goal for a bulk/cut, workout/rest day?',
        }
        error_messages = {
            'name': {
                'max_length': "Name is too long.",
                'blank' : "This field is required.",
            },
        }
    def __init__(self, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)
        fields = ['calories', 'protein', 'carbohydrates', 'fats', 'isActive']
        for f in self.fields:
            self.fields[f].required = False

class MealForm(ModelForm):
    class Meta:
        model = Meal
        labels = {
            'name' : 'Name',
            'servingSize' : 'Size of one serving',
            'units' : 'Units',
            'caloriesPerServing': _('Calories per serving (cals)'),
            'proteinPerServing' : 'Protein per serving (grams)',
            'carbohydratesPerServing' : 'Carbohydrates per serving (grams)',
            'fatsPerServing' : 'Fats per serving (grams)',
        }
        fields = ['name', 'servingSize', 'units', 'caloriesPerServing', 'proteinPerServing', 'carbohydratesPerServing', 'fatsPerServing']
    def __init__(self, *args, **kwargs):
        super(MealForm, self).__init__(*args, **kwargs)
        fields = ['caloriesPerServing', 'proteinPerServing', 'carbohydratesPerServing', 'fatsPerServing']
        for f in fields:
            self.fields[f].required = False


class EntryForm(ModelForm):
    class Meta:
        model = Entry
        labels = {
            'meal' : 'Meal',
            'amount' : 'Amount',
            'units' : 'Units',
            'mealType' : 'When?'
        }
        fields = ['meal', 'amount', 'units', 'mealType']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meal'] = ModelChoiceField(queryset=Meal.objects.order_by('-dateTimeAdded'))
        self.fields['meal'].empty_label = None

class SearchForm(forms.Form):
    searchQuery = forms.CharField(label="", max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Type a food name or brand.'}))