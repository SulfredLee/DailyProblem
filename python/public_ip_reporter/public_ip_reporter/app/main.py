
# Imports
import argparse
import logging

import sfdevtoolslight.observability.log_helper as lh

import subprocess
import json
import traceback
import Email_Writer as ew
from typing import Union, Set, List, Any
from pathlib import Path
from discord_webhook import DiscordWebhook

# Functions
def init_argparse(description: str = "") -> argparse.Namespace:
    """! initial argument parser

    @param description Argument parser description

    @return argument parser
    """
    parser = argparse.ArgumentParser(description=description)
    # parser.add_argument("-a", "--action", required=True)
    # parser.add_argument("-l", "--lang", required=True)
    # parser.add_argument("-pn", "--projectName", default="")
    return parser.parse_args()

def get_current_public_ip(logger: logging.Logger) -> Union[str, str]:
    p = subprocess.Popen(["curl", "https://ipinfo.io/ip"]
                         , stdout=subprocess.PIPE
                         , stderr=subprocess.PIPE)
    out, err = p.communicate()
    logger.info(f"the public ip: {out}")
    logger.error(f"other information: {err}")

    return [out.decode("utf-8")
            , err.decode("utf-8")]

def get_old_public_ip(json_file: Path
                      , logger: logging.Logger) -> str:
    try:
        with open(json_file) as FH:
            ip_json = json.load(FH)

            return ip_json["public_ip"]
    except:
        logger.error(traceback.format_exc())
        logger.info("cannot get old public ip. continue process.")
        return ""

def Get_Sender_Info(info_file: Path) -> Union[str, str]:
    with open(info_file) as FH:
        user = json.load(FH)

        return [user["user_name"], user["pw"]]

    raise TypeError(f"cannot get sender information from: {info_file}")

def main() -> None:
    """! public_ip_reporter main function

    @return None
    """
    logger = lh.init_logger(logger_name="public_ip_reporter_logger", is_json_output=False)
    args = init_argparse(description="public_ip_reporter Inputs")
    logger.info(f"We get args: {args}")

    # Here put your logic
    try:
        ip_storage = Path(Path.home(), "Documents", "public_ip_reporter")
        ip_storage.mkdir(parents=True, exist_ok=True)
        ip_file = Path(ip_storage, "public_ip.json")

        cur_public_ip, other_returns = get_current_public_ip(logger=logger)
        is_new_public_ip: bool = True
        if ip_file.is_file():
            old_public_ip = get_old_public_ip(json_file=ip_file, logger=logger)
            if old_public_ip == cur_public_ip:
                is_new_public_ip = False
                logger.info(f"same public ip found: {cur_public_ip}")
            else:
                is_new_public_ip = True
                logger.info("new public ip found")
                logger.info(f"old public ip: {old_public_ip}")
                logger.info(f"new public ip: {cur_public_ip}")

        if is_new_public_ip:
            # update old_public_ip
            logger.info(f"save json file to: {ip_file}")
            with open(ip_file, "w", encoding="utf-8") as FH:
                j_data = {"public_ip": cur_public_ip
                          , "other_message": other_returns}
                json.dump(j_data, FH, ensure_ascii=False, indent=4)
            webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/1207249883963068457/_s82tKlFrzKZgH-ZeDyd7yFJj3wfyJu8-8gPhWCR9AByhH_78V4wlXzKvlOdvaDwjl9T", content=cur_public_ip)
            with open(ip_file, "rb") as FH:
                webhook.add_file(file=FH.read(), filename="pip.json")
            response = webhook.execute()
    except:
        logger.error(traceback.format_exc())
        logger.error("stop process")


if __name__ == "__main__":
    main()
