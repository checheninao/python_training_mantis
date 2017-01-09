# -*- coding: utf-8 -*-
from model.project import Project
import random

def test_delete_project(app):
    if app.project.count() == 0:
        app.project.create(Project(name="proj1"))
    old_projects = app.soap.get_project_list()
    project = random.choice(old_projects)
    app.project.delete_project_by_name(project.name)
    new_projects = app.soap.get_project_list()
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(project)
    assert sorted(old_projects, key=Project.key) == sorted(new_projects, key=Project.key)