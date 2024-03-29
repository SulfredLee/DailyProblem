from projectmanager.internal.projectCreator.projectCreatorBase import *
import projectmanager.internal.projectCreator.pythonFiles.template_main as tm
import projectmanager.internal.projectCreator.pythonFiles.template_app as ta
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_app as twsa
import projectmanager.internal.projectCreator.pythonFiles.template_flask_env as tfe
import projectmanager.internal.projectCreator.pythonFiles.template_db as tdb
import projectmanager.internal.projectCreator.pythonFiles.template_web_site_db as twsdb
import projectmanager.internal.projectCreator.pythonFiles.template_item as tit
import projectmanager.internal.projectCreator.pythonFiles.template_hc as thc
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
import projectmanager.internal.projectCreator.pythonFiles.diagrams.template_readme_puml as trpu
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
import projectmanager.internal.projectCreator.pythonFiles.grpc_api_imp.template_greet_proto as gatgpi
import projectmanager.internal.projectCreator.pythonFiles.grpc_api_imp.template_greet_client as gatgci
import projectmanager.internal.projectCreator.pythonFiles.grpc_api_imp.template_greet_server as gatgsi
import projectmanager.internal.projectCreator.pythonFiles.grpc_api_imp.template_hc_client as gathcci
import projectmanager.internal.projectCreator.pythonFiles.grpc_api.template_greet_proto as gatgp
import projectmanager.internal.projectCreator.pythonFiles.grpc_api.template_greet_client as gatgc
import projectmanager.internal.projectCreator.pythonFiles.grpc_api.template_greet_server as gatgs
import projectmanager.internal.projectCreator.pythonFiles.grpc_api.template_hc_client as gathcc
import projectmanager.internal.projectCreator.pythonFiles.grpc_api.template_healthcheck_sh as gathsh
import projectmanager.internal.projectCreator.pythonFiles.scripts.template_install_vscode_sh as tiv
import projectmanager.internal.projectCreator.pythonFiles.scripts.template_start_py_servers_sh as tspss
import projectmanager.internal.projectCreator.pythonFiles.scripts.template_start_py_servers_grpc_sh as tspsgs
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
           and not cc.py_web_site_project == project_type\
           and not cc.py_grpc_project == project_type:
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

        # create the base project
        self.__create_python_project(project_root_path=project_root_path
                                     , project_action_path=project_action_path
                                     , project_type=project_type)
        # add application
        if cc.py_restful_api_project == project_type:
            self.create_restful_api_project(project_root_path=project_root_path
                                            , project_action_path=project_action_path)
        elif cc.py_tensorflow_project == project_type:
            self.create_tensorflow_project(project_root_path=project_root_path
                                           , project_action_path=project_action_path)
        elif cc.py_general_project == project_type:
            self.create_general_project(project_root_path=project_root_path
                                        , project_action_path=project_action_path)
        elif cc.py_qc_project == project_type:
            self.create_qc_project(project_root_path=project_root_path
                                   , project_action_path=project_action_path)
        elif cc.py_web_site_project == project_type:
            self.create_web_site_project(project_root_path=project_root_path
                                         , project_action_path=project_action_path)
        elif cc.py_grpc_project == project_type:
            self.create_grpc_project(project_root_path=project_root_path
                                     , project_action_path=project_action_path)
        else:
            raise ValueError(f"Not support project type: {project_type}")

        is_copy_directly = False
        if is_copy_directly:
            shutil.copytree(Path.joinpath(Path(__file__).parent, "..", "observability")
                            , Path.joinpath(project_action_path
                                            , "internal"
                                            , "observability"))

    def create_qc_project(self, project_root_path: str, project_action_path: str):
        # create project files
        self.__create_project_files(project_root_path=project_root_path
                                    , project_action_path=project_action_path
                                    , project_type=cc.py_qc_project
                                    , file_list=[
                                        [Path.joinpath(project_root_path, ".gitlab-ci.yml"), tgcyqc.content_st]
                                    ])

        # add observability module
        subprocess.run(["poetry", "install"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "sfdevtoolslight"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "lean"], cwd=Path.joinpath(self._project_path, self._project_name))

    def create_tensorflow_project(self, project_root_path: str, project_action_path: str):
        # create project files
        self.__create_project_files(project_root_path=project_root_path
                                    , project_action_path=project_action_path
                                    , project_type=cc.py_general_project
                                    , file_list=[
                                        [Path.joinpath(project_action_path, "app", "main.py"), tm.content_st]
                                    ])

        # add observability module
        subprocess.run(["poetry", "install"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "scikit-learn"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "tensorflow"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "matplotlib"], cwd=Path.joinpath(self._project_path, self._project_name))

    def create_general_project(self, project_root_path: str, project_action_path: str):
        # create project files
        self.__create_project_files(project_root_path=project_root_path
                                    , project_action_path=project_action_path
                                    , project_type=cc.py_general_project
                                    , file_list=[
                                        [Path.joinpath(project_action_path, "app", "main.py"), tm.content_st]
                                    ])

        # add observability module
        subprocess.run(["poetry", "install"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "sfdevtoolslight"], cwd=Path.joinpath(self._project_path, self._project_name))

    def create_grpc_project(self, project_root_path: str, project_action_path: str, is_replace_file: bool = True):
        # create python folders
        self.__create_python_folders(project_root_path=project_root_path
                                     , project_action_path=project_action_path
                                     , project_type=cc.py_grpc_project
                                     , path_list=[
                                         # example
                                         [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc), True]
                                         , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc, "protos"), True]
                                         # implement version
                                         , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc_imp), True]
                                         , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc_imp, "protos"), True]
                                     ])

        # create project files
        # example
        self.__create_project_files(project_root_path=project_root_path
                                    , project_action_path=project_action_path
                                    , project_type=cc.py_grpc_project
                                    , app_subfolder=cc.py_app_subfolder_grpc
                                    , is_replace_file=is_replace_file
                                    , file_list=[
                                        [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc, "greet_server.py"), gatgs.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc, "greet_client.py"), gatgc.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc, "protos", "greet.proto"), gatgp.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc, "main_manager.py"), tmm.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc, "healthcheck.sh"), gathsh.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc, "hc_client.py"), gathcc.content_st]
                                    ])
        # implement version
        self.__create_project_files(project_root_path=project_root_path
                                    , project_action_path=project_action_path
                                    , project_type=cc.py_grpc_project
                                    , app_subfolder=cc.py_app_subfolder_grpc_imp
                                    , is_replace_file=is_replace_file
                                    , file_list=[
                                         [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc_imp, f"{self._project_name}_grpc_server.py"), gatgsi.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc_imp, f"{self._project_name}_grpc_client.py"), gatgci.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc_imp, "protos", f"{self._project_name}.proto"), gatgpi.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc_imp, "main_manager.py"), tmm.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc_imp, "healthcheck.sh"), gathsh.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc_imp, "hc_client.py"), gathcci.content_st]
                                        , [Path.joinpath(project_root_path, "scripts", "start.py.servers.sh"), tspsgs.content_st]
                                    ])

        # enable execution
        self.__enable_execution(project_root_path=project_root_path
                                , project_action_path=project_action_path
                                , project_type=cc.py_grpc_project
                                , file_list=[
                                    Path.joinpath(project_root_path, "scripts", "start.py.servers.sh")
                                    , Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc, "healthcheck.sh")
                                    , Path.joinpath(project_action_path, "app", cc.py_app_subfolder_grpc_imp, "healthcheck.sh")
                                ])

        # add observability module
        subprocess.run(["poetry", "install"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "sfdevtoolslight"], cwd=Path.joinpath(self._project_path, self._project_name))
        # grpcio-tools and grpcio will be depends on sfdevtoolslight
        # subprocess.run(["poetry", "add", "grpcio-tools"], cwd=Path.joinpath(self._project_path, self._project_name))
        # subprocess.run(["poetry", "add", "grpcio"], cwd=Path.joinpath(self._project_path, self._project_name))
        # $ poetry run python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/greet.proto
        subprocess.run(["poetry"
                        , "run"
                        , "python"
                        , "-m"
                        , "grpc_tools.protoc"
                        , "-I"
                        , "protos"
                        , "--python_out=."
                        , "--grpc_python_out=."
                        , "protos/greet.proto"], cwd=Path.joinpath(self._project_path, self._project_name, self._project_name, "app", cc.py_app_subfolder_grpc))

    def create_web_site_project(self, project_root_path: str, project_action_path: str, is_replace_file: bool = True):
        # create python folders
        self.__create_python_folders(project_root_path=project_root_path
                                     , project_action_path=project_action_path
                                     , project_type=cc.py_web_site_project
                                     , path_list=[
                                         [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web), True]
                                         , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "schemas"), True]
                                         , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "routes"), True]
                                         , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "db"), True]
                                         , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "static"), False]
                                         , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "static", "css"), False]
                                         , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "templates"), False]
                                     ])

        # create project files
        self.__create_project_files(project_root_path=project_root_path
                                    , project_action_path=project_action_path
                                    , project_type=cc.py_web_site_project
                                    , app_subfolder=cc.py_app_subfolder_web
                                    , is_replace_file=is_replace_file
                                    , file_list=[
                                        [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "app.py"), twsa.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "main_manager.py"), twsmm.content_st]
                                        # , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, ".flaskenv"), tfe.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "schemas", "schemas.py"), twssch.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "routes", "authen.py"), twsau.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "routes", "home.py"), twsh.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "routes", "bootstrap_example.py"), twsbt.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "routes", "healthcheck.py"), thc.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "db", "db.py"), twsdb.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "static", "logo.svg"), twslo.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "static", "css", "styles.css"), twsst.content_st]
                                        , [Path.joinpath(project_root_path, "scripts", "start.py.servers.sh"), tspss.content_st]
                                    ])

        # create project files without jinja2
        self.__copy_project_files(project_root_path=project_root_path
                                  , project_action_path=project_action_path
                                  , project_type=cc.py_web_site_project
                                  , file_list=[
                                      [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "templates", "base.html"), twsb.content_st]
                                      , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "templates", "home.html"), twshm.content_st]
                                      , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "templates", "login.html"), twslg.content_st]
                                      , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "templates", "protected.html"), twsp.content_st]
                                      , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "templates", "signup.html"), twsu.content_st]
                                      , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_web, "templates", "bootstrap_example.html"), twsbth.content_st]
                                  ])

        # enable execution
        self.__enable_execution(project_root_path=project_root_path
                                , project_action_path=project_action_path
                                , project_type=cc.py_web_site_project
                                , file_list=[
                                    Path.joinpath(project_root_path, "scripts", "start.py.servers.sh")
                                ])

        # add observability module
        subprocess.run(["poetry", "install"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "sfdevtoolslight"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "flask"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "flask-smorest"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "python-dotenv"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "marshmallow"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "pymongo"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "flask-wtf"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "passlib"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "flask_bootstrap"], cwd=Path.joinpath(self._project_path, self._project_name))

    def create_restful_api_project(self, project_root_path: str, project_action_path: str, is_replace_file: bool = True):
        # create python folders
        self.__create_python_folders(project_root_path=project_root_path
                                     , project_action_path=project_action_path
                                     , project_type=cc.py_restful_api_project
                                     , path_list=[
                                         [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_api), True]
                                         , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_api, "schemas"), True]
                                         , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_api, "routes"), True]
                                         , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_api, "db"), True]
                                     ])

        # create project files
        self.__create_project_files(project_root_path=project_root_path
                                    , project_action_path=project_action_path
                                    , project_type=cc.py_restful_api_project
                                    , app_subfolder=cc.py_app_subfolder_api
                                    , is_replace_file=is_replace_file
                                    , file_list=[
                                        [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_api, "app.py"), ta.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_api, "main_manager.py"), tmm.content_st]
                                        # , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_api, ".flaskenv"), tfe.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_api, "schemas", "schemas.py"), tsch.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_api, "routes", "store.py"), tst.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_api, "routes", "item.py"), tit.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_api, "routes", "healthcheck.py"), thc.content_st]
                                        , [Path.joinpath(project_action_path, "app", cc.py_app_subfolder_api, "db", "db.py"), tdb.content_st]
                                        , [Path.joinpath(project_root_path, "scripts", "start.py.servers.sh"), tspss.content_st]
                                    ])

        # enable execution
        self.__enable_execution(project_root_path=project_root_path
                                , project_action_path=project_action_path
                                , project_type=cc.py_restful_api_project
                                , file_list=[
                                    Path.joinpath(project_root_path, "scripts", "start.py.servers.sh")
                                ])

        # add observability module
        subprocess.run(["poetry", "install"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "sfdevtoolslight"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "flask"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "flask-smorest"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "python-dotenv"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "marshmallow"], cwd=Path.joinpath(self._project_path, self._project_name))

    def __create_python_project(self, project_root_path: str, project_action_path: str, project_type: str):
        # create project folders
        self.__create_python_folders(project_root_path=project_root_path
                                     , project_action_path=project_action_path
                                     , project_type=project_type
                                     , path_list=[
                                         [Path.joinpath(project_action_path, "app"), True]
                                         , [Path.joinpath(project_action_path, "internal"), True]
                                         , [Path.joinpath(project_root_path, "dockerEnv"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv", "uat"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv", "dev"), False]
                                         , [Path.joinpath(project_root_path, "dockerEnv", "prod"), False]
                                         , [Path.joinpath(project_root_path, "scripts"), False]
                                         , [Path.joinpath(project_root_path, "diagrams"), False]
                                         # k8s chart folders
                                         , [Path.joinpath(project_root_path, "chart"), False]
                                         , [Path.joinpath(project_root_path, "chart", "templates"), False]
                                     ])

        # create project files
        self.__create_project_files(project_root_path=project_root_path
                                    , project_action_path=project_action_path
                                    , project_type=project_type
                                    , app_subfolder=""
                                    , file_list=[
                                        [Path.joinpath(project_action_path, "app", "Mainpage.dox"), tmp.content_st]
                                        , [Path.joinpath(project_root_path, ".gitignore"), tg.content_st]
                                        , [Path.joinpath(project_root_path, "README.md"), trm.content_st]
                                        , [Path.joinpath(project_root_path, "diagrams", "readme.puml"), trpu.content_st]
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
                                , project_type=project_type
                                , file_list=[
                                    Path.joinpath(project_root_path, "dockerEnv", "BuildImageDev.sh")
                                    , Path.joinpath(project_root_path, "dockerEnv", "BuildImageRunner.sh")
                                    , Path.joinpath(project_root_path, "dockerEnv", "BuildImageDeployer.sh")
                                    , Path.joinpath(project_root_path, "dockerEnv", "dev", "start_dev_container.sh")
                                    , Path.joinpath(project_root_path, "ExportPythonEnv.sh")
                                    , Path.joinpath(project_root_path, "scripts", "install.vscode.sh")
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
                               , project_type: str
                               , app_subfolder: str = None
                               , is_replace_file: bool = True):
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
            if not is_replace_file and os.path.isfile(template_obj[0]):
                self._logger.warning(f"File {template_obj[0]} is already exist. Skip creation.")
                continue

            with open(template_obj[0], "w") as w_FH:
                w_FH.write(j_env.from_string(template_obj[1]).render(project_name=self._project_name
                                                                     , project_name_hyphen=self._project_name.replace("_", "-")
                                                                     , project_name_capitalize=self._project_name.capitalize()
                                                                     , description=f"{self._project_name} Inputs"
                                                                     , cur_uid=pwd.getpwuid(os.getuid()).pw_uid
                                                                     , cur_gid=pwd.getpwuid(os.getuid()).pw_gid
                                                                     , cur_name=pwd.getpwuid(os.getuid()).pw_name
                                                                     , is_need_port_mapping=is_need_port_mapping
                                                                     , app_subfolder=app_subfolder
                                                                     ))

    def __enable_execution(self
                           , project_root_path: str
                           , project_action_path: str
                           , file_list: list
                           , project_type: str):
        for file_name in file_list:
            st = os.stat(file_name)
            os.chmod(file_name, st.st_mode | stat.S_IEXEC)
