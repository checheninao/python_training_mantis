from model.project import Project


def test_add_project(app, json_projects):
    old_projects = app.soap.get_project_list()
    project = json_projects
    app.project.create(project)
    new_projects = app.soap.project.get_project_list()
    if project.name != "" and project.name not in [proj.name for proj in old_projects]:
       old_projects.append(project)
    assert len(old_projects) == len(new_projects)
    assert sorted(old_projects, key=Project.key) == sorted(new_projects, key=Project.key)