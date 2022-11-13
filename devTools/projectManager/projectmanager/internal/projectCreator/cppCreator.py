from projectmanager.internal.projectCreator.projectCreatorBase import *
import projectmanager.internal.projectCreator.cppFiles.template_CMakeLists as tc
import projectmanager.internal.projectCreator.cppFiles.template_Preparevcpkg as tp
import projectmanager.internal.projectCreator.cppFiles.template_readme as tr
import projectmanager.internal.projectCreator.cppFiles.template_gitignore as tg
import projectmanager.internal.projectCreator.cppFiles.debug.template_CCMake as dtc
import projectmanager.internal.projectCreator.cppFiles.release.template_CCMake as rtc
import projectmanager.internal.projectCreator.cppFiles.app.template_main as tm
import projectmanager.internal.projectCreator.cppFiles.app.template_CMakeLists as atc
import projectmanager.internal.projectCreator.cppFiles.test.template_test_h as tth
import projectmanager.internal.projectCreator.cppFiles.test.template_test_cpp as ttc
import projectmanager.internal.projectCreator.cppFiles.test.template_CMakeLists as ttcm
import projectmanager.internal.commonConst as cc

class cppCreator(projectCreatorBase):
    def __init__(self, project_name: str, project_path: str, logger: logging.Logger):
        super().__init__(project_name, project_path, logger)

    # virtual
    def create_project(self, project_type: str):
        if cc.cpp_qt_project == project_type:
            self.__create_qt_project()
        elif cc.cpp_general_project == project_type:
            self.__create_general_project()
        else:
            raise ValueError(f"Not support project type: {project_type}")

    def __create_qt_project(self):
        self._logger.info("Here")

    def __create_general_project(self):
        self._logger.info(f"Creating project in folder: {self._project_path}")

        # create folders
        project_root = Path.joinpath(self._project_path, self._project_name)
        project_root.mkdir(parents=True, exist_ok=True)
        for path_name in ["release", "debug", "install", "app", "internal", "external", "test"]:
            Path.joinpath(project_root, path_name).mkdir(parents=True, exist_ok=True)

        # handle normal tempalte files
        j_env = jinja2.Environment()
        for template_obj in [[Path.joinpath(project_root, "readme.md"), tr.content_st]
                             , [Path.joinpath(project_root, ".gitignore"), tg.content_st]
                             , [Path.joinpath(project_root, "Preparevcpkg.sh"), tp.content_st]
                             , [Path.joinpath(project_root, "debug", "CCMake.sh"), dtc.content_st]
                             , [Path.joinpath(project_root, "release", "CCMake.sh"), rtc.content_st]]:
            with open(template_obj[0], "w") as w_FH:
                w_FH.write(j_env.from_string(template_obj[1]).render())

        # handle special tempalte files
        for template_obj in [[Path.joinpath(project_root, "CMakeLists.txt"), tc.content_st]
                             , [Path.joinpath(project_root, "app", "main.cpp"), tm.content_st]
                             , [Path.joinpath(project_root, "app", "CMakeLists.txt"), atc.content_st]
                             , [Path.joinpath(project_root, "test", "CMakeLists.txt"), ttcm.content_st]
                             , [Path.joinpath(project_root, "test", f"{self._project_name}_Test.h"), tth.content_st]
                             , [Path.joinpath(project_root, "test", f"{self._project_name}_Test.cpp"), ttc.content_st]]:
            with open(template_obj[0], "w") as w_FH:
                w_FH.write(j_env.from_string(template_obj[1]).render(project_name=self._project_name))

        # enable execution
        for file_name in [Path.joinpath(project_root, "Preparevcpkg.sh")
                          , Path.joinpath(project_root, "debug", "CCMake.sh")
                          , Path.joinpath(project_root, "release", "CCMake.sh")]:
            st = os.stat(file_name)
            os.chmod(file_name, st.st_mode | stat.S_IEXEC)

        # show how to init the project
        self._logger.info(f"Please run the script Preparevcpkg.sh to init your project")
