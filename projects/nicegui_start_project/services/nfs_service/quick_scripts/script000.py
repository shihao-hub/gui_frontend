import os

from projects.nicegui_start_project.nicegui_start_project.models.mongodb import File

files = File.objects.all()
dirs_loc = os.listdir("../files")
deleted_files = []
for file in files:
    for name in dirs_loc:
        if not name.startswith(file.filename):
            deleted_files.append(name)
for name in deleted_files:
    os.remove(f"../files/{name}")
