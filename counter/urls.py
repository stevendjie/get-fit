from django.conf.urls import url
from . import views

urlpatterns = [
    #/counter/
    url(r'^$', views.index, name='index'),
    url(r'^new_goal/$', views.newGoal, name='newGoal'),
    url(r'^goals/$', views.viewGoals, name='viewGoals'),
    url(r'^delete_goal/(?P<pk>\d+)/$', views.deleteGoal, name='deleteGoal'),
    url(r'^edit_goal/(?P<pk>\d+)/$', views.editGoal, name='editGoal'),
    url(r'^edit_entry/(?P<pk>\d+)/$', views.editEntry, name='editEntry'),
    url(r'^new_meal/lunch/$', views.NewMealLunch.as_view(), name='newMealLunch'),
    url(r'^new_meal/$', views.NewMeal.as_view(), name='newMeal'),
    url(r'^meals/$', views.viewMeals, name='viewMeals'),
    url(r'^edit_meal/(?P<pk>\d+)/$', views.editMeal, name='editMeal'),
    url(r'^delete_meal/(?P<pk>\d+)/$', views.deleteMeal, name='deleteMeal'),
    url(r'^new_entry/lunch/$', views.NewEntryLunch.as_view(), name='newEntryLunch'),
    url(r'^new_entry/$', views.NewEntry.as_view(), name='newEntry'),
    url(r'^new_entry/breakfast/$', views.NewEntryBreakfast.as_view(), name='newEntryBreakfast'),
    url(r'^new_entry/dinner/$', views.NewEntryDinner.as_view(), name='newEntryDinner'),
    url(r'^new_entry/snack/$', views.NewEntrySnack.as_view(), name='newEntrySnack'),
    url(r'^new_meal/breakfast/$', views.NewMealBreakfast.as_view(), name='newMealBreakfast'),
    url(r'^new_meal/dinner/$', views.NewMealDinner.as_view(), name='newMealDinner'),
    url(r'^new_meal/snack/$', views.NewMealSnack.as_view(), name='newMealSnack'),
    url(r'^search_meal/$', views.getMealDatabase, name='getMealDatabase'),
    url(r'^new_meal_database/(?P<id>[\w\+%_& ]+)/$', views.newMealDatabase, name='newMealDatabase'),

]
