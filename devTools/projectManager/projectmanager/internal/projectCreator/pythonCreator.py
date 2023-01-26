from projectmanager.internal.projectCreator.projectCreatorBase import *
import projectmanager.internal.projectCreator.pythonFiles.template_main as tm
import projectmanager.internal.projectCreator.pythonFiles.template_app as ta
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_app as twsa
import projectmanager.internal.projectCreator.pythonFiles.template_flask_env as tfe
import projectmanager.internal.projectCreator.pythonFiles.template_db as tdb
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_db as twsdb
import projectmanager.internal.projectCreator.pythonFiles.template_item as tit
import projectmanager.internal.projectCreator.pythonFiles.template_store as tst
import projectmanager.internal.projectCreator.pythonFiles.template_schemas as tsch
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_schemas as twssch
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_authen as twsau
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_home as twsh
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_bootstrap_example as twsbt
import projectmanager.internal.projectCreator.pythonFiles.template_main_manager as tmm
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_main_manager as twsmm
import projectmanager.internal.projectCreator.pythonFiles.template_RestoreUserGroup_sh as trug
import projectmanager.internal.projectCreator.pythonFiles.template_Export_Python_Env_sh as tepe
import projectmanager.internal.projectCreator.pythonFiles.template_test as tt
import projectmanager.internal.projectCreator.pythonFiles.template_gitignore as tg
import projectmanager.internal.projectCreator.pythonFiles.template_Mainpage as tmp
import projectmanager.internal.projectCreator.pythonFiles.template_readme_md as trm
import projectmanager.internal.projectCreator.pythonFiles.template_Dockerfile as td
import projectmanager.internal.projectCreator.pythonFiles.template_Dockerfile_Runner as tdr
import projectmanager.internal.projectCreator.pythonFiles.template_Dockerfile_Deploy as tdd
import projectmanager.internal.projectCreator.pythonFiles.template_gitlab_ci_yml as tgcy
import projectmanager.internal.projectCreator.pythonFiles.template_gitlab_ci_yml_qc as tgcyqc
import projectmanager.internal.projectCreator.pythonFiles.template_Doxyfile as tdf
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_logo as twslo
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_styles as twsst
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_base as twsb
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_home_html as twshm
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_bootstrap_example_html as twsbth
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_login as twslg
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_protected as twsp
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_signup as twsu
import projectmanager.internal.projectCreator.pythonFiles.scripts.template_install_vscode_sh as tiv
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.template_BuildImageBuilder_sh as tbbs
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.template_BuildImageRunner_sh as tbrs
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.template_BuildImageDeployer_sh as tbds
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.dev.template_env as dte
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.dev.template_start_dev_container_sh as dtsdc
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.uat.template_env as ute
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.uat.template_docker_compose_yml as utdcy
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.prod.template_env as pte
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.prod.template_docker_compose_yml as ptdcy
import projectmanager.internal.projectCreator.pythonFiles.chart.template_chart_yaml as ctcy
import projectmanager.internal.projectCreator.pythonFiles.chart.template_helmignore as cth
import projectmanager.internal.projectCreator.pythonFiles.chart.template_values_dev_yaml as ctvdy
import projectmanager.internal.projectCreator.pythonFiles.chart.template_values_prod_yaml as ctvpy
import projectmanager.internal.projectCreator.pythonFiles.chart.templates.template_workload_yaml as cttwy
import projectmanager.internal.commonConst as cc
import subprocess

class pythonCreator(projectCreatorBase):
    def __init__(self, project_name: str, project_path: str, logger: logging.Logger):
        super().__init__(project_name, project_path, logger)

    # virtual
    def create_project(self, project_type: str):
        # check project type
        if not cc.py_restful_api_project == project_type\
           and not cc.py_general_project == project_type\
           and not cc.py_qc_project == project_type\
           and not cc.py_web_site_project == project_type:
            raise ValueError(f"Not support project type: {project_type}")

        # start project create
        self._logger.info(f"Creating project in folder: {self._project_path}")

        # get paths
        project_root_path = Path.joinpath(self._project_path, self._project_name)
        project_action_path = Path.joinpath(self._project_path
                                            , self._project_name
                                            , self._project_name)

        if project_root_path.is_dir():
            # create project if folder already exist
            # we have this case when we initial the project from gitlab/github
            temp_project_root_path = Path.joinpath(self._project_path, "temp_project_python")
            temp_project_root_path.mkdir(parents=True, exist_ok=True)
            subprocess.run(["poetry", "new", f"{self._project_name}"], cwd=temp_project_root_path)
            shutil.copytree(Path.joinpath(temp_project_root_path, self._project_name), project_root_path, dirs_exist_ok=True)
            shutil.rmtree(temp_project_root_path)
        else:
            # create project by poetry
            subprocess.run(["poetry", "new", f"{self._project_name}"], cwd=self._project_path)

        # start to create different projects
        if cc.py_restful_api_project == project_type:
            self.__create_restful_api_project(project_root_path=project_root_path
                                              , project_action_path=project_action_path)
        elif cc.py_general_project == project_type:
            self.__create_general_project(project_root_path=project_root_path
                                          , project_action_path=project_action_path)
        elif cc.py_qc_project == project_type:
            self.__create_qc_project(project_root_path=project_root_path
                                     , project_action_path=project_action_path)
        elif cc.py_web_site_project == project_type:
            self.__create_web_site_project(project_root_path=project_root_path
                                           , project_action_path=project_action_path)
        else:
            raise ValueError(f"Not support project type: {project_type}")

        is_copy_directly = False
        if is_copy_directly:
            shutil.copytree(Path.joinpath(Path(__file__).parent, "..", "observability")
                            , Path.joinpath(project_action_path
                                            , "internal"
                                            , "observability"))

    def __create_web_site_project(self, project_root_path: str, project_action_path: str):
        # create python folders
        self.__create_python_folders(project_root_path=project_root_path
                                     , project_action_path=project_action_path
                                     , project_type=cc.py_web_site_project
                                     , path_list=[
                                         [Path.joinpath(project_action_path, "app"), True]
                                         , [Path.joinpath(project_action_path, "app", "schemas"), True]
                                         , [Path.joinpath(project_action_path, "app", "routes"), True]
                                         , [Path.joinpath(project_action_path, "internal"), True]
                                         , [Path.joinpath(project_action_path, "internal", "db"), True]
                                         , [Path.joinpath(project_action_path, "app", "static"), False]
                                         , [Path.joinpath(project_action_path, "app", "static", "css"), False]
                                         , [Path.joinpath(project_action_path, "app", "templates"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv", "uat"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv", "dev"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv", "prod"), False]
                                         , [Path.joinpath(project_root_path, "scripts"), False]
                                         # k8s chart folders
                                         , [Path.joinpath(project_root_path, "chart"), False]
                                         , [Path.joinpath(project_root_path, "chart", "templates"), False]
                                     ])

        # create project files
        self.__create_project_files(project_root_path=project_root_path
                                    , project_action_path=project_action_path
                                    , project_type=cc.py_web_site_project
                                    , file_list=[
                                        [Path.joinpath(project_action_path, "app", "app.py"), twsa.content_st]
                                        , [Path.joinpath(project_action_path, "app", "main_manager.py"), twsmm.content_st]
                                        , [Path.joinpath(project_action_path, "app", ".flaskenv"), tfe.content_st]
                                        , [Path.joinpath(project_action_path, "app", "Mainpage.dox"), tmp.content_st]
                                        , [Path.joinpath(project_action_path, "app", "schemas", "schemas.py"), twssch.content_st]
                                        , [Path.joinpath(project_action_path, "app", "routes", "authen.py"), twsau.content_st]
                                        , [Path.joinpath(project_action_path, "app", "routes", "home.py"), twsh.content_st]
                                        , [Path.joinpath(project_action_path, "app", "routes", "bootstrap_example.py"), twsbt.content_st]
                                        , [Path.joinpath(project_action_path, "internal", "db", "db.py"), twsdb.content_st]
                                        , [Path.joinpath(project_action_path, "app", "static", "logo.svg"), twslo.content_st]
                                        , [Path.joinpath(project_action_path, "app", "static", "css", "styles.css"), twsst.content_st]
                                        , [Path.joinpath(project_root_path, ".gitignore"), tg.content_st]
                                        , [Path.joinpath(project_root_path, "README.md"), trm.content_st]
                                        # , [Path.joinpath(project_root_path, "RestoreUserGroup.sh"), trug.content_st]
                                        , [Path.joinpath(project_root_path, "ExportPythonEnv.sh"), tepe.content_st]
                                        , [Path.joinpath(project_root_path, ".gitlab-ci.yml"), tgcy.content_st]
                                        , [Path.joinpath(project_root_path, "Doxyfile"), tdf.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "Dockerfile.Dev"), td.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "Dockerfile.Run"), tdr.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "Dockerfile.Deploy"), tdd.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "BuildImageRunner.sh"), tbrs.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "BuildImageDev.sh"), tbbs.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "BuildImageDeployer.sh"), tbds.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "uat", ".env"), ute.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "uat", "docker-compose.yml"), utdcy.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "dev", ".env"), dte.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "dev", "start_dev_container.sh"), dtsdc.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "prod", ".env"), pte.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "prod", "docker-compose.yml"), ptdcy.content_st]
                                        , [Path.joinpath(project_root_path, "tests", f"test_{self._project_name}.py"), tt.content_st]
                                        , [Path.joinpath(project_root_path, "scripts", "install.vscode.sh"), tiv.content_st]
                                        # k8s chart files
                                        , [Path.joinpath(project_root_path, "chart", "Chart.yaml"), ctcy.content_st]
                                        , [Path.joinpath(project_root_path, "chart", ".helmsignore"), cth.content_st]
                                        , [Path.joinpath(project_root_path, "chart", "values.dev.yaml"), ctvdy.content_st]
                                        , [Path.joinpath(project_root_path, "chart", "values.prod.yaml"), ctvpy.content_st]
                                        , [Path.joinpath(project_root_path, "chart", "templates", "workload.yaml"), cttwy.content_st]
                                    ])

        # create project files without jinja2
        self.__copy_project_files(project_root_path=project_root_path
                                  , project_action_path=project_action_path
                                  , project_type=cc.py_web_site_project
                                  , file_list=[
                                      [Path.joinpath(project_action_path, "app", "templates", "base.html"), twsb.content_st]
                                      , [Path.joinpath(project_action_path, "app", "templates", "home.html"), twshm.content_st]
                                      , [Path.joinpath(project_action_path, "app", "templates", "login.html"), twslg.content_st]
                                      , [Path.joinpath(project_action_path, "app", "templates", "protected.html"), twsp.content_st]
                                      , [Path.joinpath(project_action_path, "app", "templates", "signup.html"), twsu.content_st]
                                      , [Path.joinpath(project_action_path, "app", "templates", "bootstrap_example.html"), twsbth.content_st]
                                  ])

        # enable execution
        self.__enable_execution(project_root_path=project_root_path
                                , project_action_path=project_action_path
                                , project_type=cc.py_web_site_project
                                , file_list=[
                                    Path.joinpath(project_root_path, "dockerEnv", "BuildImageDev.sh")
                                    , Path.joinpath(project_root_path, "dockerEnv", "BuildImageRunner.sh")
                                    , Path.joinpath(project_root_path, "dockerEnv", "BuildImageDeployer.sh")
                                    , Path.joinpath(project_root_path, "dockerEnv", "dev", "start_dev_container.sh")
                                    , Path.joinpath(project_root_path, "ExportPythonEnv.sh")
                                    , Path.joinpath(project_root_path, "scripts", "install.vscode.sh")
                                ])

        # add observability module
        subprocess.run(["poetry", "install"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "sfdevtools"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "flask"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "flask-smorest"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "python-dotenv"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "marshmallow"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "pymongo"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "flask-wtf"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "passlib"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "flask_bootstrap"], cwd=Path.joinpath(self._project_path, self._project_name))

    def __create_restful_api_project(self, project_root_path: str, project_action_path: str):
        # create python folders
        self.__create_python_folders(project_root_path=project_root_path
                                     , project_action_path=project_action_path
                                     , project_type=cc.py_restful_api_project
                                     , path_list=[
                                         [Path.joinpath(project_action_path, "app"), True]
                                         , [Path.joinpath(project_action_path, "app", "schemas"), True]
                                         , [Path.joinpath(project_action_path, "app", "routes"), True]
                                         , [Path.joinpath(project_action_path, "internal"), True]
                                         , [Path.joinpath(project_action_path, "internal", "db"), True]
                                         , [Path.joinpath(project_root_path, "dockerEnv"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv", "uat"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv", "dev"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv", "prod"), False]
                                         , [Path.joinpath(project_root_path, "scripts"), False]
                                         # k8s chart folders
                                         , [Path.joinpath(project_root_path, "chart"), False]
                                         , [Path.joinpath(project_root_path, "chart", "templates"), False]
                                     ])

        # create project files
        self.__create_project_files(project_root_path=project_root_path
                                    , project_action_path=project_action_path
                                    , project_type=cc.py_restful_api_project
                                    , file_list=[
                                        [Path.joinpath(project_action_path, "app", "app.py"), ta.content_st]
                                        , [Path.joinpath(project_action_path, "app", "main_manager.py"), tmm.content_st]
                                        , [Path.joinpath(project_action_path, "app", ".flaskenv"), tfe.content_st]
                                        , [Path.joinpath(project_action_path, "app", "Mainpage.dox"), tmp.content_st]
                                        , [Path.joinpath(project_action_path, "app", "schemas", "schemas.py"), tsch.content_st]
                                        , [Path.joinpath(project_action_path, "app", "routes", "store.py"), tst.content_st]
                                        , [Path.joinpath(project_action_path, "app", "routes", "item.py"), tit.content_st]
                                        , [Path.joinpath(project_action_path, "internal", "db", "db.py"), tdb.content_st]
                                        , [Path.joinpath(project_root_path, ".gitignore"), tg.content_st]
                                        , [Path.joinpath(project_root_path, "README.md"), trm.content_st]
                                        # , [Path.joinpath(project_root_path, "RestoreUserGroup.sh"), trug.content_st]
                                        , [Path.joinpath(project_root_path, "ExportPythonEnv.sh"), tepe.content_st]
                                        , [Path.joinpath(project_root_path, ".gitlab-ci.yml"), tgcy.content_st]
                                        , [Path.joinpath(project_root_path, "Doxyfile"), tdf.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "Dockerfile.Dev"), td.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "Dockerfile.Run"), tdr.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "Dockerfile.Deploy"), tdd.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "BuildImageRunner.sh"), tbrs.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "BuildImageDev.sh"), tbbs.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "BuildImageDeployer.sh"), tbds.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "uat", ".env"), ute.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "uat", "docker-compose.yml"), utdcy.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "dev", ".env"), dte.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "dev", "start_dev_container.sh"), dtsdc.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "prod", ".env"), pte.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "prod", "docker-compose.yml"), ptdcy.content_st]
                                        , [Path.joinpath(project_root_path, "tests", f"test_{self._project_name}.py"), tt.content_st]
                                        , [Path.joinpath(project_root_path, "scripts", "install.vscode.sh"), tiv.content_st]
                                        # k8s chart files
                                        , [Path.joinpath(project_root_path, "chart", "Chart.yaml"), ctcy.content_st]
                                        , [Path.joinpath(project_root_path, "chart", ".helmsignore"), cth.content_st]
                                        , [Path.joinpath(project_root_path, "chart", "values.dev.yaml"), ctvdy.content_st]
                                        , [Path.joinpath(project_root_path, "chart", "values.prod.yaml"), ctvpy.content_st]
                                        , [Path.joinpath(project_root_path, "chart", "templates", "workload.yaml"), cttwy.content_st]
                                    ])

        # enable execution
        self.__enable_execution(project_root_path=project_root_path
                                , project_action_path=project_action_path
                                , project_type=cc.py_restful_api_project
                                , file_list=[
                                    Path.joinpath(project_root_path, "dockerEnv", "BuildImageDev.sh")
                                    , Path.joinpath(project_root_path, "dockerEnv", "BuildImageRunner.sh")
                                    , Path.joinpath(project_root_path, "dockerEnv", "BuildImageDeployer.sh")
                                    , Path.joinpath(project_root_path, "dockerEnv", "dev", "start_dev_container.sh")
                                    , Path.joinpath(project_root_path, "ExportPythonEnv.sh")
                                    , Path.joinpath(project_root_path, "scripts", "install.vscode.sh")
                                ])

        # add observability module
        subprocess.run(["poetry", "install"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "sfdevtools"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "flask"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "flask-smorest"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "python-dotenv"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "marshmallow"], cwd=Path.joinpath(self._project_path, self._project_name))


    def __create_qc_project(self, project_root_path: str, project_action_path: str):
        # create python folders
        self.__create_python_folders(project_root_path=project_root_path
                                     , project_action_path=project_action_path
                                     , project_type=cc.py_qc_project
                                     , path_list=[
                                         [Path.joinpath(project_action_path), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv", "uat"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv", "dev"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv", "prod"), False]
                                         , [Path.joinpath(project_root_path, "scripts"), False]
                                         ])

        # create project files
        self.__create_project_files(project_root_path=project_root_path
                                    , project_action_path=project_action_path
                                    , project_type=cc.py_qc_project
                                    , file_list=[
                                        [Path.joinpath(project_action_path, "Mainpage.dox"), tmp.content_st]
                                        , [Path.joinpath(project_root_path, ".gitignore"), tg.content_st]
                                        , [Path.joinpath(project_root_path, "README.md"), trm.content_st]
                                        , [Path.joinpath(project_root_path, "ExportPythonEnv.sh"), tepe.content_st]
                                        , [Path.joinpath(project_root_path, ".gitlab-ci.yml"), tgcyqc.content_st]
                                        , [Path.joinpath(project_root_path, "Doxyfile"), tdf.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "Dockerfile.Dev"), td.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "Dockerfile.Run"), tdr.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "Dockerfile.Deploy"), tdd.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "BuildImageRunner.sh"), tbrs.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "BuildImageDev.sh"), tbbs.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "BuildImageDeployer.sh"), tbds.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "uat", ".env"), ute.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "uat", "docker-compose.yml"), utdcy.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "dev", ".env"), dte.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "dev", "start_dev_container.sh"), dtsdc.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "prod", ".env"), pte.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "prod", "docker-compose.yml"), ptdcy.content_st]
                                        , [Path.joinpath(project_root_path, "tests", f"test_{self._project_name}.py"), tt.content_st]
                                        , [Path.joinpath(project_root_path, "scripts", "install.vscode.sh"), tiv.content_st]
                                    ])

        # enable execution
        self.__enable_execution(project_root_path=project_root_path
                                , project_action_path=project_action_path
                                , project_type=cc.py_qc_project
                                , file_list=[
                                    Path.joinpath(project_root_path, "dockerEnv", "BuildImageDev.sh")
                                    , Path.joinpath(project_root_path, "dockerEnv", "BuildImageRunner.sh")
                                    , Path.joinpath(project_root_path, "dockerEnv", "BuildImageDeployer.sh")
                                    , Path.joinpath(project_root_path, "dockerEnv", "dev", "start_dev_container.sh")
                                    , Path.joinpath(project_root_path, "ExportPythonEnv.sh")
                                    , Path.joinpath(project_root_path, "scripts", "install.vscode.sh")
                                ])

        # add observability module
        subprocess.run(["poetry", "install"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "sfdevtools"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "lean"], cwd=Path.joinpath(self._project_path, self._project_name))

    def __create_general_project(self, project_root_path: str, project_action_path: str):
        # create python folders
        self.__create_python_folders(project_root_path=project_root_path
                                     , project_action_path=project_action_path
                                     , project_type=cc.py_general_project
                                     , path_list=[
                                         [Path.joinpath(project_action_path, "app"), True]
                                         , [Path.joinpath(project_action_path, "internal"), True]
                                         , [Path.joinpath(project_root_path, "dockerEnv"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv", "uat"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv", "dev"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv", "prod"), False]
                                         , [Path.joinpath(project_root_path, "scripts"), False]
                                         # k8s chart folders
                                         , [Path.joinpath(project_root_path, "chart"), False]
                                         , [Path.joinpath(project_root_path, "chart", "templates"), False]
                                         ])

        # create project files
        self.__create_project_files(project_root_path=project_root_path
                                    , project_action_path=project_action_path
                                    , project_type=cc.py_general_project
                                    , file_list=[
                                        [Path.joinpath(project_action_path, "app", "main.py"), tm.content_st]
                                        , [Path.joinpath(project_action_path, "app", "Mainpage.dox"), tmp.content_st]
                                        , [Path.joinpath(project_root_path, ".gitignore"), tg.content_st]
                                        , [Path.joinpath(project_root_path, "README.md"), trm.content_st]
                                        # , [Path.joinpath(project_root_path, "RestoreUserGroup.sh"), trug.content_st]
                                        , [Path.joinpath(project_root_path, "ExportPythonEnv.sh"), tepe.content_st]
                                        , [Path.joinpath(project_root_path, ".gitlab-ci.yml"), tgcy.content_st]
                                        , [Path.joinpath(project_root_path, "Doxyfile"), tdf.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "Dockerfile.Dev"), td.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "Dockerfile.Run"), tdr.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "Dockerfile.Deploy"), tdd.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "BuildImageRunner.sh"), tbrs.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "BuildImageDev.sh"), tbbs.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "BuildImageDeployer.sh"), tbds.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "uat", ".env"), ute.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "uat", "docker-compose.yml"), utdcy.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "dev", ".env"), dte.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "dev", "start_dev_container.sh"), dtsdc.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "prod", ".env"), pte.content_st]
                                        , [Path.joinpath(project_root_path, "dockerEnv", "prod", "docker-compose.yml"), ptdcy.content_st]
                                        , [Path.joinpath(project_root_path, "tests", f"test_{self._project_name}.py"), tt.content_st]
                                        , [Path.joinpath(project_root_path, "scripts", "install.vscode.sh"), tiv.content_st]
                                        # k8s chart files
                                        , [Path.joinpath(project_root_path, "chart", "Chart.yaml"), ctcy.content_st]
                                        , [Path.joinpath(project_root_path, "chart", ".helmsignore"), cth.content_st]
                                        , [Path.joinpath(project_root_path, "chart", "values.dev.yaml"), ctvdy.content_st]
                                        , [Path.joinpath(project_root_path, "chart", "values.prod.yaml"), ctvpy.content_st]
                                        , [Path.joinpath(project_root_path, "chart", "templates", "workload.yaml"), cttwy.content_st]
                                    ])

        # enable execution
        self.__enable_execution(project_root_path=project_root_path
                                , project_action_path=project_action_path
                                , project_type=cc.py_general_project
                                , file_list=[
                                    Path.joinpath(project_root_path, "dockerEnv", "BuildImageDev.sh")
                                    , Path.joinpath(project_root_path, "dockerEnv", "BuildImageRunner.sh")
                                    , Path.joinpath(project_root_path, "dockerEnv", "BuildImageDeployer.sh")
                                    , Path.joinpath(project_root_path, "dockerEnv", "dev", "start_dev_container.sh")
                                    , Path.joinpath(project_root_path, "ExportPythonEnv.sh")
                                    , Path.joinpath(project_root_path, "scripts", "install.vscode.sh")
                                ])

        # add observability module
        subprocess.run(["poetry", "install"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "sfdevtools"], cwd=Path.joinpath(self._project_path, self._project_name))

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
        # handle port mapping cases
        is_need_port_mapping = False
        if project_type == cc.py_restful_api_project:
            is_need_port_mapping = True
        elif project_type == cc.py_web_site_project:
            is_need_port_mapping = True
        else:
            is_need_port_mapping = False

        j_env = jinja2.Environment()
        for template_obj in file_list:
            with open(template_obj[0], "w") as w_FH:
                w_FH.write(j_env.from_string(template_obj[1]).render(project_name=self._project_name
                                                                     , project_name_hyphen=self._project_name.replace("_", "-")
                                                                     , description=f"{self._project_name} Inputs"
                                                                     , cur_uid=pwd.getpwuid(os.getuid()).pw_uid
                                                                     , cur_gid=pwd.getpwuid(os.getuid()).pw_gid
                                                                     , cur_name=pwd.getpwuid(os.getuid()).pw_name
                                                                     , is_need_port_mapping=is_need_port_mapping
                                                                     ))

    def __enable_execution(self
                           , project_root_path: str
                           , project_action_path: str
                           , file_list: list
                           , project_type: str):
        for file_name in file_list:
            st = os.stat(file_name)
            os.chmod(file_name, st.st_mode | stat.S_IEXEC)
