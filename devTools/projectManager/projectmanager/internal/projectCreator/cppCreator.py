from projectmanager.internal.projectCreator.projectCreatorBase import *
import projectmanager.internal.projectCreator.cppFiles.template_CMakeLists as tc
import projectmanager.internal.projectCreator.cppFiles.script.template_Preparevcpkg as tp
import projectmanager.internal.projectCreator.cppFiles.script.template_PrepareSpacemacsTags as tpst
import projectmanager.internal.projectCreator.cppFiles.script.template_CCMake_Debug as dtc
import projectmanager.internal.projectCreator.cppFiles.script.template_CCMake_Release as rtc
import projectmanager.internal.projectCreator.cppFiles.script.template_Active_Core_Dump_sh as rtacd
import projectmanager.internal.projectCreator.cppFiles.script.template_View_Test_Coverage_sh as tvtc
import projectmanager.internal.projectCreator.cppFiles.script.template_BuildImageRunner_sh as tbir
import projectmanager.internal.projectCreator.cppFiles.script.template_BuildImageBuilder_sh as tbib
import projectmanager.internal.projectCreator.cppFiles.script.template_Start_CPP_Servers_sh as tscss
import projectmanager.internal.projectCreator.cppFiles.template_readme as tr
import projectmanager.internal.projectCreator.cppFiles.diagrams.template_readme_puml as trpu
import projectmanager.internal.projectCreator.cppFiles.template_gitignore as tg
import projectmanager.internal.projectCreator.cppFiles.install.template_gitkeep as tgk
import projectmanager.internal.projectCreator.cppFiles.app.template_Mainpage as tmd
import projectmanager.internal.projectCreator.cppFiles.test.template_test_h as tth
import projectmanager.internal.projectCreator.cppFiles.test.template_test_cpp as ttc
import projectmanager.internal.projectCreator.cppFiles.test.template_CMakeLists as ttcm
import projectmanager.internal.projectCreator.cppFiles.user_benchmark.template_CMakeLists as ttcm_bm
import projectmanager.internal.projectCreator.cppFiles.user_benchmark.template_benchmark_cpp as ttc_bm
import projectmanager.internal.projectCreator.cppFiles.template_Dockerfile as td
import projectmanager.internal.projectCreator.cppFiles.template_Dockerfile_Run as tdr
import projectmanager.internal.projectCreator.cppFiles.template_Doxyfile as tdf
import projectmanager.internal.projectCreator.cppFiles.template_gitlab_ci_yml as tgcy
import projectmanager.internal.projectCreator.cppFiles.dockerEnv.uat.template_env as ute
import projectmanager.internal.projectCreator.cppFiles.dockerEnv.uat.template_docker_compose_yml as utdc
import projectmanager.internal.projectCreator.cppFiles.dockerEnv.prod.template_env as pte
import projectmanager.internal.projectCreator.cppFiles.dockerEnv.prod.template_docker_compose_yml as ptdc
import projectmanager.internal.projectCreator.cppFiles.dockerEnv.dev.template_env as dte
import projectmanager.internal.projectCreator.cppFiles.dockerEnv.dev.template_docker_compose_yml as dtdc
import projectmanager.internal.projectCreator.cppFiles.dockerEnv.dev.template_start_dev_container_sh as dtsdc
import projectmanager.internal.projectCreator.cppFiles.chart.template_chart_yaml as ctcy
import projectmanager.internal.projectCreator.cppFiles.chart.template_helmignore as cth
import projectmanager.internal.projectCreator.cppFiles.chart.template_values_dev_yaml as ctvdy
import projectmanager.internal.projectCreator.cppFiles.chart.template_values_prod_yaml as ctvpy
import projectmanager.internal.projectCreator.cppFiles.chart.templates.template_workload_yaml as cttwy
import projectmanager.internal.commonConst as cc
import projectmanager.internal.commonConst as cc

class cppCreator(projectCreatorBase):
    def __init__(self, project_name: str, project_path: str, logger: logging.Logger):
        super().__init__(project_name, project_path, logger)

    # virtual
    def create_project(self, project_type: str):
        if cc.cpp_general_project == project_type:
            self.__create_general_project()
        else:
            raise ValueError(f"Not support project type: {project_type}")

    def __create_general_project(self):
        self._logger.info(f"Creating project in folder: {self._project_path}")

        # create folders
        project_root = Path.joinpath(self._project_path, self._project_name)
        project_sub_root = Path.joinpath(project_root, "project")
        project_root.mkdir(parents=True, exist_ok=True)
        for path_name in [Path.joinpath(project_root, "scripts")
                          , Path.joinpath(project_sub_root, "app")
                          , Path.joinpath(project_sub_root, "internal")
                          , Path.joinpath(project_sub_root, "external")
                          , Path.joinpath(project_sub_root, "test")
                          , Path.joinpath(project_sub_root, "benchmark")
                          , Path.joinpath(project_root, "dockerEnv")
                          , Path.joinpath(project_root, "dockerEnv", "dev")
                          , Path.joinpath(project_root, "diagrams")
                          # k8s chart folders
                          , Path.joinpath(project_root, "chart")
                          , Path.joinpath(project_root, "chart", "templates")
                          ]:
            path_name.mkdir(parents=True, exist_ok=True)

        # handle normal tempalte files
        j_env = jinja2.Environment()
        # handle special tempalte files
        for template_obj in [[Path.joinpath(project_root, "README.md"), tr.content_st]
                             , [Path.joinpath(project_root, "diagrams", "readme.puml"), trpu.content_st]
                             , [Path.joinpath(project_root, ".gitignore"), tg.content_st]
                             , [Path.joinpath(project_root, ".gitlab-ci.yml"), tgcy.content_st]
                             , [Path.joinpath(project_root, "scripts", "Preparevcpkg.sh"), tp.content_st]
                             , [Path.joinpath(project_root, "scripts", "PrepareSpacemacsTags.sh"), tpst.content_st]
                             , [Path.joinpath(project_root, "scripts", "CCMake_Debug.sh"), dtc.content_st]
                             , [Path.joinpath(project_root, "scripts", "Start_CPP_Servers.sh"), tscss.content_st]
                             , [Path.joinpath(project_root, "scripts", "CCMake_Release.sh"), rtc.content_st]
                             , [Path.joinpath(project_root, "scripts", "Active_Core_Dump.sh"), rtacd.content_st]
                             , [Path.joinpath(project_root, "scripts", "View_Test_Coverage.sh"), tvtc.content_st]
                             # , [Path.joinpath(project_root, "install", ".gitkeep"), tgk.content_st]
                             , [Path.joinpath(project_sub_root, "CMakeLists.txt"), tc.content_st]
                             , [Path.joinpath(project_sub_root, "app", "Mainpage.dox"), tmd.content_st]
                             , [Path.joinpath(project_sub_root, "external", ".gitkeep"), tgk.content_st]
                             , [Path.joinpath(project_sub_root, "internal", ".gitkeep"), tgk.content_st]
                             , [Path.joinpath(project_sub_root, "benchmark", "CMakeLists.txt"), ttcm_bm.content_st]
                             , [Path.joinpath(project_sub_root, "benchmark", f"{self._project_name}_Benchmark.cpp"), ttc_bm.content_st]
                             , [Path.joinpath(project_sub_root, "test", "CMakeLists.txt"), ttcm.content_st]
                             , [Path.joinpath(project_sub_root, "test", f"{self._project_name}_Test.h"), tth.content_st]
                             , [Path.joinpath(project_sub_root, "test", f"{self._project_name}_Test.cpp"), ttc.content_st]
                             , [Path.joinpath(project_sub_root, "Doxyfile"), tdf.content_st]
                             # , [Path.joinpath(project_root, "dockerEnv", "uat", ".env"), ute.content_st]
                             # , [Path.joinpath(project_root, "dockerEnv", "uat", "docker-compose.yml"), utdc.content_st]
                             # , [Path.joinpath(project_root, "dockerEnv", "prod", ".env"), pte.content_st]
                             # , [Path.joinpath(project_root, "dockerEnv", "prod", "docker-compose.yml"), ptdc.content_st]
                             , [Path.joinpath(project_root, "dockerEnv", "Dockerfile.Dev"), td.content_st]
                             , [Path.joinpath(project_root, "dockerEnv", "Dockerfile.Run"), tdr.content_st]
                             , [Path.joinpath(project_root, "dockerEnv", "BuildImageRunner.sh"), tbir.content_st]
                             , [Path.joinpath(project_root, "dockerEnv", "BuildImageDev.sh"), tbib.content_st]
                             , [Path.joinpath(project_root, "dockerEnv", "dev", ".env"), dte.content_st]
                             , [Path.joinpath(project_root, "dockerEnv", "dev", "start_dev_container.sh"), dtsdc.content_st]
                             # k8s chart files
                             , [Path.joinpath(project_root, "chart", "Chart.yaml"), ctcy.content_st]
                             , [Path.joinpath(project_root, "chart", ".helmsignore"), cth.content_st]
                             , [Path.joinpath(project_root, "chart", "values.dev.yaml"), ctvdy.content_st]
                             , [Path.joinpath(project_root, "chart", "values.prod.yaml"), ctvpy.content_st]
                             , [Path.joinpath(project_root, "chart", "templates", "workload.yaml"), cttwy.content_st]
                             ]:
            with open(template_obj[0], "w") as w_FH:
                w_FH.write(j_env.from_string(template_obj[1]).render(project_name=self._project_name
                                                                     , project_name_hyphen=self._project_name.replace("_", "-")
                                                                     , cur_name=pwd.getpwuid(os.getuid()).pw_name
                                                                     , cur_uid=pwd.getpwuid(os.getuid()).pw_uid
                                                                     , cur_gid=pwd.getpwuid(os.getuid()).pw_gid))

        # enable execution
        for file_name in [Path.joinpath(project_root, "scripts", "Preparevcpkg.sh")
                          , Path.joinpath(project_root, "scripts", "PrepareSpacemacsTags.sh")
                          , Path.joinpath(project_root, "scripts", "CCMake_Debug.sh")
                          , Path.joinpath(project_root, "scripts", "CCMake_Release.sh")
                          , Path.joinpath(project_root, "scripts", "Start_CPP_Servers.sh")
                          , Path.joinpath(project_root, "scripts", "Active_Core_Dump.sh")
                          , Path.joinpath(project_root, "scripts", "View_Test_Coverage.sh")
                          , Path.joinpath(project_root, "dockerEnv", "BuildImageRunner.sh")
                          , Path.joinpath(project_root, "dockerEnv", "BuildImageDev.sh")
                          , Path.joinpath(project_root, "dockerEnv", "dev", "start_dev_container.sh")
                          ]:
            st = os.stat(file_name)
            os.chmod(file_name, st.st_mode | stat.S_IEXEC)

        # show how to init the project
        self._logger.info(f"Please run the script Preparevcpkg.sh to init your project")
