# -*- coding: utf-8 -*-
from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_manage_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("manage_overview_page.php")):
            wd.find_element_by_link_text("Manage").click()

    def open_manage_projects_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("manage_proj_page.php")):
            self.open_manage_page()
            wd.find_element_by_link_text("Manage Projects").click()

    def change_field_value(self, field_name, value):
        wd = self.app.wd
        if value is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(value)

    def change_status(self, value):
        wd = self.app.wd
        if value is not None:
            wd.find_element_by_xpath("//select[@name='status']/option[text()='%s']" % value).click()

    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.name)
        self.change_status(project.status)
        self.change_field_value("description", project.description)

    def create(self, group):
        wd = self.app.wd
        self.open_manage_projects_page()
        # init project creation
        wd.find_element_by_css_selector('input[value="Create New Project"]').click()
        self.fill_project_form(group)
        # submit project creation
        wd.find_element_by_css_selector('input[value="Add Project"]').click()
        self.project_cache = None

    def delete_project_by_name(self, project_name):
        wd = self.app.wd
        self.open_manage_projects_page()
        # select project by name
        wd.find_element_by_link_text(project_name).click()
        # submit project deletion
        wd.find_element_by_css_selector('input[value="Delete Project"]').click()
        wd.find_element_by_css_selector('input[value="Delete Project"]').click()
        self.project_cache = None

    def checkErrorText(self):
        wd = self.app.wd

    def count(self):
        wd = self.app.wd
        self.open_manage_projects_page()
        proj_table = wd.find_element_by_xpath("//table[3]/tbody")
        return len(proj_table.find_elements_by_tag_name("tr")[2:])

    project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_manage_projects_page()
            self.project_cache = []
            proj_table = wd.find_element_by_xpath("//table[3]/tbody")
            rows = proj_table.find_elements_by_tag_name("tr")[2:]
            for row in rows:
                cells = row.find_elements_by_tag_name("td")
                name = cells[0].text
                status = cells[1].text
                description = cells[4].text
                self.project_cache.append(Project(name=name, status=status, description=description))
        return list(self.project_cache)
