from projectmanager.internal.projectUpdater.projectUpdaterBase import *
import projectmanager.internal.commonConst as cc
import projectmanager.internal.projectCreator.pythonCreator as pc

class pythonUpdater(projectUpdaterBase):
    def __init__(self, module_name: str, project_path: str, logger: logging.Logger):
        super().__init__(module_name, project_path, logger)

        project_path = self._project_path.parent
        project_name = self._project_path.name # get the last part from the path
        # get paths
        self.__project_root_path = Path.joinpath(project_path, project_name)
        self.__project_action_path = Path.joinpath(project_path
                                                   , project_name
                                                   , project_name)

        self.__python_creator = pc.pythonCreator(project_name=project_name
                                                 , project_path=project_path
                                                 , logger=self._logger)

    # virtual
    def update_project(self, project_type: str) -> None:
        if cc.py_add_grpc_app == project_type:
            self.__add_grpc_app()
        elif cc.py_add_restful_api_app == project_type:
            self.__add_restful_api_app()
        elif cc.py_add_web_site_app == project_type:
            self.__add_web_site_app()
        else:
            raise ValueError(f"Not support project type: {project_type}")

    def __add_grpc_app(self):
        self.__python_creator.create_grpc_project(project_root_path=self.__project_root_path
                                                  , project_action_path=self.__project_action_path
                                                  , is_replace_file=False)

    def __add_restful_api_app(self):
        self.__python_creator.create_restful_api_project(project_root_path=self.__project_root_path
                                                         , project_action_path=self.__project_action_path
                                                         , is_replace_file=False)

    def __add_web_site_app(self):
        self.__python_creator.create_web_site_project(project_root_path=self.__project_root_path
                                                      , project_action_path=self.__project_action_path
                                                      , is_replace_file=False)
