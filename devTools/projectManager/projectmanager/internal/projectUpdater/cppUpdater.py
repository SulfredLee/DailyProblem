from projectmanager.internal.projectUpdater.projectUpdaterBase import *
import projectmanager.internal.projectUpdater.cppFiles.internal.template_static_lib.template_CMakeLists as tsc
import projectmanager.internal.projectUpdater.cppFiles.internal.template_static_lib.template_static_lib_h as slh
import projectmanager.internal.projectUpdater.cppFiles.internal.template_static_lib.template_static_lib_cpp as slc
import projectmanager.internal.projectUpdater.cppFiles.internal.template_dynamic_lib.template_CMaketLists as tdc
import projectmanager.internal.projectUpdater.cppFiles.internal.template_CMakeLists as itc
import projectmanager.internal.projectUpdater.cppFiles.external.template_external_cmake as tec
import projectmanager.internal.commonConst as cc
import parse_cmake.parsing as cmpr

class cppUpdater(projectUpdaterBase):
    def __init__(self, module_name: str, project_path: str, logger: logging.Logger):
        super().__init__(module_name, project_path, logger)

    # virtual
    def update_project(self, project_type: str) -> None:
        if cc.cpp_add_static_lib == project_type:
            self.__add_static_lib()
        elif cc.cpp_add_dynamic_lib == project_type:
            self.__add_dynamic_lib()
        elif cc.cpp_add_external_project == project_type:
            self.__add_external_project()
        else:
            raise ValueError(f"Not support project type: {project_type}")

    def __add_static_lib(self) -> None:
        self.__add_lib(module_cmake=tsc.content_st)

    def __add_dynamic_lib(self) -> None:
        self.__add_lib(module_cmake=tdc.content_st)

    def __add_external_project(self) -> None:
        self._logger.info(f"Project in folder: {self._project_path}")
        self._logger.info(f"Module name: {self._module_name}")

        # create folders
        module_root = Path.joinpath(self._project_path, "external")

        # handle normal tempalte files
        j_env = jinja2.Environment()

        for template_obj in [[Path.joinpath(module_root, f"external_{self._module_name}.cmake"), tec.content_st]
                             ]:
            with open(template_obj[0], "w") as w_FH:
                w_FH.write(j_env.from_string(template_obj[1]).render(module_name=self._module_name))

        # include external project to CMakeLists.txt
        self.__append_external_project(Path.joinpath(self._project_path, "CMakeLists.txt"))

    def __append_external_project(self, cmake_file_name: Path) -> None:
        target_cmd: cmpr.Comment = cmpr.Comment("# Add External Project")
        # read cmake file
        cmake_file_parsed: cmpr.File = self.__read_cmake_file(cmake_file_name)
        for idx, cm_line in enumerate(cmake_file_parsed):
            if target_cmd == cm_line:
                self._logger.info("Found a good place to insert command for external modules")
                # insert command in a better place
                cmake_file_parsed.insert(idx, cmpr.Command("include"
                                                           , [cmpr.Arg(f"external/external_{self._module_name}.cmake")]))
                # cmake_file_parsed.insert(idx, cm_line)
                # del cmake_file_parsed[idx + 2]

                # output cmake file
                self.__write_cmake_file(cmake_file_name, cmake_file_parsed)

                return
            else:
                continue

        # insert command in a better place
        cmake_file_parsed.append(cmpr.Command("include", [cmpr.Arg(f"external/external_{self._module_name}.cmake")]))
        # output cmake file
        self.__write_cmake_file(cmake_file_name, cmake_file_parsed)

    def __add_lib(self, module_cmake: str) -> None:
        self._logger.info(f"Project in folder: {self._project_path}")
        self._logger.info(f"Module name: {self._module_name}")

        # create folders
        module_root = Path.joinpath(self._project_path, "internal")
        Path.joinpath(module_root, self._module_name).mkdir(parents=True, exist_ok=True)

        # handle normal tempalte files
        j_env = jinja2.Environment()

        for template_obj in [[Path.joinpath(module_root, self._module_name, "CMakeLists.txt"), module_cmake]
                             , [Path.joinpath(module_root, self._module_name, f"{self._module_name}.h"), slh.content_st]
                             , [Path.joinpath(module_root, self._module_name, f"{self._module_name}.cpp"), slc.content_st]
                             ]:
            with open(template_obj[0], "w") as w_FH:
                w_FH.write(j_env.from_string(template_obj[1]).render(module_name=self._module_name))

        if Path.joinpath(module_root, "CMakeLists.txt").is_file():
            # append new moduel to internal root CMakeLists.txt
            ## Read CMakeLists.txt
            cmake_file_parsed: cmpr.File = self.__read_cmake_file(Path.joinpath(module_root, "CMakeLists.txt"))
            ## append new command
            cmake_file_parsed.append(cmpr.Command("add_subdirectory", [cmpr.Arg(self._module_name)]))
            ## Write CMakeLists.txt
            self.__write_cmake_file(Path.joinpath(module_root, "CMakeLists.txt"), cmake_file_parsed)
        else:
            # create a new file
            with open(Path.joinpath(module_root, "CMakeLists.txt"), "w") as w_FH:
                w_FH.write(j_env.from_string(itc.content_st).render(module_name=self._module_name))

        # include internal folder to the root CMakeLists.txt
        self.__append_internal_folder(Path.joinpath(self._project_path, "CMakeLists.txt"))

    def __append_internal_folder(self, cmake_file_name: Path) -> None:
        target_cmd: cmpr.Command = cmpr.Command("add_subdirectory", [cmpr.Arg("internal")])
        # read cmake file
        cmake_file_parsed: cmpr.File = self.__read_cmake_file(cmake_file_name)
        for cm_line in cmake_file_parsed:
            if target_cmd == cm_line:
                # command already included, return and do nothing
                return
            else:
                continue

        for idx, cm_line in enumerate(cmake_file_parsed):
            if cmpr.Command("add_subdirectory", [cmpr.Arg("test")]) == cm_line:
                self._logger.info("Found a good place to insert command for internal modules")
                # insert command in a better place
                cmake_file_parsed.insert(idx, target_cmd)
                # output cmake file
                self.__write_cmake_file(cmake_file_name, cmake_file_parsed)

                return
            else:
                continue

        # append command at the bottom
        cmake_file_parsed.append(target_cmd)
        # output cmake file
        self.__write_cmake_file(cmake_file_name, cmake_file_parsed)

    def __read_cmake_file(self, cmake_file_name: Path) -> cmpr.File:
        with open(cmake_file_name, "r") as r_FH:
            cmake_file: str = r_FH.read()
            cmake_file_parsed: cmpr.File = cmpr.parse(cmake_file)

            return cmake_file_parsed

    def __write_cmake_file(self, cmake_file_name: Path, cmake_file_parsed: cmpr.File) -> None:
        with open(cmake_file_name, "w") as w_FH:
            w_FH.write(cmake_file_parsed.pretty_print())
