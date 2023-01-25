from projectmanager.internal.projectCreator.projectCreatorBase import *
import projectmanager.internal.commonConst as cc
import subprocess
import projectmanager.internal.projectCreator.k8sFiles.template_gitignore as tg
import projectmanager.internal.projectCreator.k8sFiles.template_readme_md as trm
import projectmanager.internal.projectCreator.k8sFiles.template_gitlab_ci_yml as tgcy
import projectmanager.internal.projectCreator.k8sFiles.template_Dockerfile_Deploy as tdd
import projectmanager.internal.projectCreator.k8sFiles.template_BuildImageDeployer_sh as tbds

class k8sCreator(projectCreatorBase):
    def __init__(self, project_name: str, project_path: str, logger: logging.Logger):
        super().__init__(project_name, project_path, logger)

    # virtual
    def create_project(self, project_type: str):
        # check project type
        if not cc.k8s_general_project == project_type:
            raise ValueError(f"Not support project type: {project_type}")

        # start project create
        self._logger.info(f"Creating project in folder: {self._project_path}")

        # get paths
        project_root_path = Path.joinpath(self._project_path, self._project_name)
        project_action_path = Path.joinpath(self._project_path
                                            , self._project_name
                                            , self._project_name)

        # start to create different projects
        if cc.k8s_general_project == project_type:
            self.__create_general_project(project_root_path=project_root_path
                                          , project_action_path=project_action_path)
        else:
            raise ValueError(f"Not support project type: {project_type}")

    def __create_general_project(self, project_root_path: str, project_action_path: str):
        # create python folders
        self.__create_python_folders(project_root_path=project_root_path
                                     , project_action_path=project_action_path
                                     , project_type=cc.k8s_general_project
                                     , path_list=[
                                         [Path.joinpath(project_root_path, "dockerEnv"), False]
                                     ])

        # create project files
        self.__create_project_files(project_root_path=project_root_path
                                    , project_action_path=project_action_path
                                    , project_type=cc.k8s_general_project
                                    , file_list=[
                                        [Path.joinpath(project_root_path, ".gitignore"), tg.content_st]
                                        , [Path.joinpath(project_root_path, "README.md"), trm.content_st]
                                        , [Path.joinpath(project_root_path, ".gitlab-ci.yml"), tgcy.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "Dockerfile.Deploy"), tdd.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "BuildImageDeployer.sh"), tbds.content_st]
                                    ])

        # enable execution
        self.__enable_execution(project_root_path=project_root_path
                                , project_action_path=project_action_path
                                , project_type=cc.py_web_site_project
                                , file_list=[
                                    Path.joinpath(project_root_path, "dockerEnv", "BuildImageDeployer.sh")
                                ])

    def __create_python_folders(self
                                , project_root_path: str
                                , project_action_path: str
                                , path_list: list
                                , project_type: str):
        for the_path in path_list:
            # create folder
            the_path[0].mkdir(parents=True, exist_ok=True)
            if the_path[1]:
                # create __init__.py
                Path.joinpath(the_path[0], "__init__.py").touch()

    def __copy_project_files(self
                             , project_root_path: str
                             , project_action_path: str
                             , file_list: list
                             , project_type: str):
        for template_obj in file_list:
            with open(template_obj[0], "w") as w_FH:
                w_FH.write(template_obj[1])

    def __create_project_files(self
                               , project_root_path: str
                               , project_action_path: str
                               , file_list: list
                               , project_type: str):
        j_env = jinja2.Environment()
        for template_obj in file_list:
            with open(template_obj[0], "w") as w_FH:
                w_FH.write(j_env.from_string(template_obj[1]).render(project_name=self._project_name
                                                                     ))

    def __enable_execution(self
                           , project_root_path: str
                           , project_action_path: str
                           , file_list: list
                           , project_type: str):
        for file_name in file_list:
            st = os.stat(file_name)
            os.chmod(file_name, st.st_mode | stat.S_IEXEC)
