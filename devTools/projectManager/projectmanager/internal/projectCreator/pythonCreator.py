from projectmanager.internal.projectCreator.projectCreatorBase import *
import projectmanager.internal.projectCreator.pythonFiles.template_main as tm
import projectmanager.internal.projectCreator.pythonFiles.template_test as tt
import subprocess
import jinja2
import shutil

class pythonCreator(projectCreatorBase):
    def __init__(self, project_name: str, project_path: str, logger: logging.Logger):
        super().__init__(project_name, project_path, logger)

    # virtual
    def create_project(self, project_type: str):
        if "Python Web Project" == project_type:
            self.__create_web_project()
        elif "Python General Project" == project_type:
            self.__create_general_project()
        else:
            raise ValueError(f"Not support project type: {project_type}")

    def __create_web_project(self):
        self._logger.info("Here")

    def __create_general_project(self):
        self._logger.info(f"Creating project in folder: {self._project_path}")

        # create project by poetry
        subprocess.run(["poetry", "new", f"{self._project_name}"], cwd=self._project_path)

        project_action_path = Path.joinpath(self._project_path
                                            , self._project_name
                                            , self._project_name)
        for folder_name in ["app", "internal"]:
            # create folders
            Path.joinpath(project_action_path
                          , folder_name).mkdir(parents=True
                                               , exist_ok=True)

            # create init python file
            Path.joinpath(project_action_path
                          , folder_name
                          , "__init__.py").touch()

        # create app file
        j_env = jinja2.Environment()
        template_main = j_env.from_string(tm.content_st)
        with open(Path.joinpath(project_action_path
                                , "app"
                                , "main.py"), "w") as w_FH:
            w_FH.write(template_main.render(description=f"{self._project_name} Inputs"
                                            , project_name=self._project_name))

        # copy git ignore
        shutil.copyfile(Path.joinpath(Path(__file__).parent, "..", "..", "..", ".gitignore")
                        , Path.joinpath(project_action_path
                                        , ".."
                                        , ".gitignore"))

        # add observability module
        subprocess.run(["poetry", "install"], cwd=Path.joinpath(self._project_path, self._project_name))
        subprocess.run(["poetry", "add", "sfdevtools"], cwd=Path.joinpath(self._project_path, self._project_name))

        is_copy_directly = False
        if is_copy_directly:
            shutil.copytree(Path.joinpath(Path(__file__).parent, "..", "observability")
                            , Path.joinpath(project_action_path
                                            , "internal"
                                            , "observability"))
        # add test file
        template_test = j_env.from_string(tt.content_st)
        with open(Path.joinpath(project_action_path
                                , ".."
                                , "tests"
                                , f"test_{self._project_name}.py"), "w") as w_FH:
            w_FH.write(template_test.render(project_name=self._project_name))

