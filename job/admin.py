from django.contrib import admin
from job.models import Corpus

class CorpusAdmin(admin.ModelAdmin):
    list_display=('name', 'source', 'typ', 'tim')

admin.site.register(Corpus, CorpusAdmin)

