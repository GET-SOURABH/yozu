from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='home'),

    path("evaluate", views.combined_api, name='evaluate'),
    # path("evaluate_math", views.evaluate_math, name='evaluate_math'),
    # path("category", views.category, name='category'),
    # path("real_life_examples", views.real_life_examples, name='real_life_examples'),
    # path("level_1_questions", views.level_1_questions, name='level_1_questions'),
    # path("level_2_questions", views.level_2_questions, name='level_2_questions'),
    # path("level_3_questions",views.level_3_questions, name='level_3_questions'),
    # path("specific_category_questions",views.specific_category_questions, name='specific_category_questions'),
    # path("combined_api", views.combined_api, name="combined_api")
]