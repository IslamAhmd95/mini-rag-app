import os

from .BaseView import BaseView


class ProjectView(BaseView):
    def __init__(self, project_id) -> None:
        super().__init__(project_id)

    def get_project_dir_path(self):
        project_dir_path = os.path.join(
            self.files_dir_path,
            self.project_id
        )

        if not os.path.exists(project_dir_path):
            os.makedirs(project_dir_path)

        return project_dir_path