import argparse
import projectmanager.internal.observability.log_helper as lh
import projectmanager.internal.projectCreator.pythonCreator as pc
import projectmanager.internal.projectCreator.cppCreator as cc
import projectmanager.internal.projectCreator.k8sCreator as kc
import projectmanager.internal.projectCreator.projectCreatorBase as pcb
import projectmanager.internal.projectUpdater.cppUpdater as cu
import projectmanager.internal.projectUpdater.projectUpdaterBase as pub
import logging

def init_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Project Manager Help Message")
    parser.add_argument("-a", "--action", required=True)
    parser.add_argument("-l", "--lang", required=True)
    parser.add_argument("-pt", "--projectType", required=True)
    parser.add_argument("-pn", "--projectName", default="")
    parser.add_argument("-mn", "--moduleName", default="")
    parser.add_argument("-pp", "--projectPath", required=True)
    return parser.parse_args()

def create_project(args: argparse.Namespace, logger: logging.Logger) -> None:
    # validation
    if args.projectName == "":
        raise ValueError("Please provide project name when you want to create a project")

    project_creator: pcb.projectCreatorBase = None
    if args.lang == "Python":
        project_creator = pc.pythonCreator(project_name=args.projectName
                                           , project_path=args.projectPath
                                           , logger=logger)
    elif args.lang == "Cpp":
        project_creator = cc.cppCreator(project_name=args.projectName
                                        , project_path=args.projectPath
                                        , logger=logger)
    elif args.lang == "Kubernetes":
        project_creator = kc.k8sCreator(project_name=args.projectName
                                        , project_path=args.projectPath
                                        , logger=logger)
    else:
        raise ValueError(f"Not support language: {args.lang}")

    project_creator.create_project(project_type=args.projectType)

def update_project(args: argparse.Namespace, logger: logging.Logger) -> None:
    # validation
    if args.moduleName == "":
        raise ValueError("Please provide module name when you want to update a project")

    project_updater: pub.projectUpdaterBase = None
    if args.lang == "Cpp":
        project_updater = cu.cppUpdater(module_name=args.moduleName
                                        , project_path=args.projectPath
                                        , logger=logger)
    else:
        raise ValueError(f"Not support language: {args.lang}")

    project_updater.update_project(project_type=args.projectType)

def main():
    logger = lh.init_logger(logger_name="project_manager", is_json_output=False)
    args = init_argparse()
    logger.info(f"We get args: {args}")

    if args.action == "Create Project":
        create_project(args, logger)
    elif args.action == "Update Project":
        update_project(args, logger)

if __name__ == "__main__":
    main()
