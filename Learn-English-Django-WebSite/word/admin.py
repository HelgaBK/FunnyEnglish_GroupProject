from django.contrib import admin
from word.models import Word, WordKnowledge, CompletedWord, QuizModel

# Register your models here.
admin.site.site_header = 'Funny English Admin Panel'

# admin.site.register(QuizModel)

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):

    list_display = ["engWord", "trWord", "structure"]
    list_display_links = ["engWord", "trWord", "structure"]
    list_filter = ["structure"]
    search_fields = ["engWord", "trWord", "structure"]

    class Meta:
        model = Word


@admin.register(WordKnowledge)
class WordKnowlegeAdmin(admin.ModelAdmin):
    list_display = ["user", "word", "date", "level"]
    list_display_links = ["user", "word", "date", "level"]
    list_filter = ["user", "word", "date", "level"]

    class Meta:
        model = WordKnowledge


@admin.register(CompletedWord)
class TamamlananKelimeAdmin(admin.ModelAdmin):
    list_display = ["user", "word", "date"]
    list_display_links = ["user", "word", "date"]
    list_filter = ["user", "word", "date"   ]

    class Meta:
        model = CompletedWord

#@admin.register(QuizModel)
#class QuizModelAdmin(admin.ModelAdmin):
#    list_display = ['','','']
#    list_display_links = ['','','']
#    list_filter = ['','','']