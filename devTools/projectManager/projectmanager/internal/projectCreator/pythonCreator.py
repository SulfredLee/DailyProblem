from projectmanager.internal.projectCreator.projectCreatorBase import *
import projectmanager.internal.projectCreator.pythonFiles.template_main as tm
import projectmanager.internal.projectCreator.pythonFiles.template_RestoreUserGroup_sh as trug
import projectmanager.internal.projectCreator.pythonFiles.template_Export_Python_Env_sh as tepe
import projectmanager.internal.projectCreator.pythonFiles.template_test as tt
import projectmanager.internal.projectCreator.pythonFiles.template_gitignore as tg
import projectmanager.internal.projectCreator.pythonFiles.template_Mainpage as tmp
import projectmanager.internal.projectCreator.pythonFiles.template_readme_md as trm
import projectmanager.internal.projectCreator.pythonFiles.template_Dockerfile as td
import projectmanager.internal.projectCreator.pythonFiles.template_gitlab_ci_yml as tgcy
import projectmanager.internal.projectCreator.pythonFiles.template_Doxyfile as tdf
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.template_BuildImageBuilder_sh as tbbs
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.template_BuildImageRunner_sh as tbrs
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.dev.template_env as dte
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.dev.template_start_dev_container_sh as dtsdc
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.uat.template_env as ute
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.uat.template_docker_compose_yml as utdcy
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.prod.template_env as pte
import projectmanager.internal.projectCreator.pythonFiles.dockerEnv.prod.template_docker_compose_yml as ptdcy
import projectmanager.internal.commonConst as cc
import subprocess

class pythonCreator(projectCreatorBase):
    def __init__(self, project_name: str, project_path: str, logger: logging.Logger):
        super().__init__(project_name, project_path, logger)

    # virtual
    def create_project(self, project_type: str):
        if cc.py_web_project == project_type:
            self.__create_web_project()
        elif cc.py_general_project == project_type:
            self.__create_general_project()
        else:
            raise ValueError(f"Not support project type: {project_type}")

    def __create_web_project(self):
        self._logger.info("Here")

    def __create_general_project(self):
        self._logger.info(f"Creating project in folder: {self._project_path}")

        project_root_path = Path.joinpath(self._project_path, self._project_name)
        project_action_path = Path.joinpath(self._project_path
                                            , self._project_name
                                            , self._project_name)
        if project_root_path.is_dir():
            temp_project_root_path = Path.joinpath(self._project_path, "temp_project_python")
            temp_project_root_path.mkdir(parents=True, exist_ok=True)
            subprocess.run(["poetry", "new", f"{self._project_name}"], cwd=temp_project_root_path)
            shutil.copytree(Path.joinpath(temp_project_root_path, self._project_name), project_root_path, dirs_exist_ok=True)
            shutil.rmtree(temp_project_root_path)
        else:
            # create project by poetry
            subprocess.run(["poetry", "new", f"{self._project_name}"], cwd=self._project_path)

        for the_path in [[Path.joinpath(project_action_path, "app"), True]
                         , [Path.joinpath(project_action_path, "internal"), True]
                         , [Path.joinpath(project_root_path, "dockerEnv"), False]
                         , [Path.joinpath(project_root_path, "dockerEnv", "uat"), False]
                         , [Path.joinpath(project_root_path, "dockerEnv", "dev"), False]
                         , [Path.joinpath(project_root_path, "dockerEnv", "prod"), False]
                         ]:
            # create folder
            the_path[0].mkdir(parents=True, exist_ok=True)
            if the_path[1]:
                # create __init__.py
                Path.joinpath(the_path[0], "__init__.py").touch()

        # create template file
        j_env = jinja2.Environment()
        for template_obj in [[Path.joinpath(project_action_path, "app", "main.py"), tm.content_st]
                             , [Path.joinpath(project_action_path, "app", "Mainpage.dox"), tmp.content_st]
                             , [Path.joinpath(project_root_path, ".gitignore"), tg.content_st]
                             , [Path.joinpath(project_root_path, "README.md"), trm.content_st]
                             , [Path.joinpath(project_root_path, "Dockerfile"), td.content_st]
                             # , [Path.joinpath(project_root_path, "RestoreUserGroup.sh"), trug.content_st]
                             , [Path.joinpath(project_root_path, "ExportPythonEnv.sh"), tepe.content_st]
                             , [Path.joinpath(project_root_path, ".gitlab-ci.yml"), tgcy.content_st]
                             , [Path.joinpath(project_root_path, "Doxyfile"), tdf.content_st]
                             , [Path.joinpath(project_root_path, "dockerEnv", "BuildImageRunner.sh"), tbrs.content_st]
                             , [Path.joinpath(project_root_path, "dockerEnv", "BuildImageBuilder.sh"), tbbs.content_st]
                             , [Path.joinpath(project_root_path, "dockerEnv", "uat", ".env"), ute.content_st]
                             , [Path.joinpath(project_root_path, "dockerEnv", "uat", "docker-compose.yml"), utdcy.content_st]
                             , [Path.joinpath(project_root_path, "dockerEnv", "dev", ".env"), dte.content_st]
                             , [Path.joinpath(project_root_path, "dockerEnv", "dev", "start_dev_container.sh"), dtsdc.content_st]
                             , [Path.joinpath(project_root_path, "dockerEnv", "prod", ".env"), pte.content_st]
                             , [Path.joinpath(project_root_path, "dockerEnv", "prod", "docker-compose.yml"), ptdcy.content_st]
                             , [Path.joinpath(project_root_path, "tests", f"test_{self._project_name}.py"), tt.content_st]
                             ]:
            with open(template_obj[0], "w") as w_FH:
                w_FH.write(j_env.from_string(template_obj[1]).render(project_name=self._project_name
                                                                     , description=f"{self._project_name} Inputs"
                                                                     , cur_uid=pwd.getpwuid(os.getuid()).pw_uid
                                                                     , cur_gid=pwd.getpwuid(os.getuid()).pw_gid
                                                                     ))

        # enable execution
        for file_name in [Path.joinpath(project_root_path, "dockerEnv", "BuildImageBuilder.sh")
                          , Path.joinpath(project_root_path, "dockerEnv", "BuildImageRunner.sh")
                          , Path.joinpath(project_root_path, "dockerEnv", "dev", "start_dev_container.sh")
                          # , Path.joinpath(project_root_path, "RestoreUserGroup.sh")
                          , Path.joinpath(project_root_path, "ExportPythonEnv.sh")
                          ]:
            st = os.stat(file_name)
            os.chmod(file_name, st.st_mode | stat.S_IEXEC)

        # add observability module
        subprocess.run(["poetry", "install"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "sfdevtools"], cwd=Path.joinpath(self._project_path, self._project_name))

        is_copy_directly = False
        if is_copy_directly:
            shutil.copytree(Path.joinpath(Path(__file__).parent, "..", "observability")
                            , Path.joinpath(project_action_path
                                            , "internal"
                                            , "observability"))
