from django.contrib import admin
from word.models import Word, WordKnowledge, CompletedWord, QuizModel, Theme

# Register your models here.
admin.site.site_header = 'Funny English Admin Panel'


# admin.site.register(QuizModel)

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ["theme", "img"]
    list_display_links = ["theme"]
    list_filter = ["theme"]
    search_fields = ["theme"]

    class Meta:
        model = Theme


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ["engWord", "trWord", "structure", "sentence", "img", "word_id"]
    list_display_links = ["engWord", "trWord", "word_id"]
    list_filter = ["word_id"]
    search_fields = ["engWord", "trWord"]

    class Meta:
        model = Word


@admin.register(WordKnowledge)
class WordKnowlegeAdmin(admin.ModelAdmin):
    list_display = ["user", "word", "date", "level"]
    list_display_links = ["user", "word", "date", "level"]
    list_filter = ["user", "word", "date", "level"]

    class Meta:
        model = WordKnowledge


# @admin.register(CompletedWord)
# class TamamlananKelimeAdmin(admin.ModelAdmin):
#     list_display = ["user", "word", "date"]
#     list_display_links = ["user", "word", "date"]
#     list_filter = ["user", "word", "date"]
#
#     class Meta:
#         model = CompletedWord


@admin.register(QuizModel)
class QuizModelAdmin(admin.ModelAdmin):
    list_display = ["question", "option1_id", "option2_id", "option3_id", "option4_id", "answer_id"]
    list_display_links = ["question"]
    list_filter = ["question", "answer_id"]
