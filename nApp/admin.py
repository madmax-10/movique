from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from io import TextIOWrapper
import csv

from .models import Video, Genre
from .forms import CSVImportForm

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    change_list_template = "application_changelist.html"  # or whatever path/name you use
    filter_horizontal = ('genres',)

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.import_csv),
                name="napp_video_import_csv",
            ),
        ]
        return custom + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = CSVImportForm(request.POST, request.FILES)
            if form.is_valid():
                text = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
                reader = csv.DictReader(text)
                for row in reader:
                    video, created = Video.objects.update_or_create(
                        title=row['title'],
                        defaults={'url': row['trailer_url']}
                    )
                    genres = [g.strip() for g in row['genres'].split(',') if g.strip()]
                    for name in genres:
                        genre_obj, _ = Genre.objects.get_or_create(name=name)
                        video.genres.add(genre_obj)
                self.message_user(request, "CSV imported successfully.", level=messages.SUCCESS)
                return redirect("..")
        else:
            form = CSVImportForm()

        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'form': form,
        }
        return render(request, "import_form.html", context)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass