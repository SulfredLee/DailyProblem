# Imports
import argparse
import logging
import os
import requests
import pandas as pd
import time
from pathlib import Path
from bs4 import BeautifulSoup # poetry add beautifulsoup4

import sfdevtools.observability.log_helper as lh

def Get_Verb_Table(verb_inputs: Path
                   , logger: logging.Logger):
    verbs: pd.DataFrame = pd.read_csv(verb_inputs)
    converted_verb_table_row_list: List[List[str]] = list()
    for idx, row in verbs.iterrows():
        logger.info(f"processing verb: {row['verb']}")

        url = f"https://konjugator.reverso.net/konjugation-deutsch-verb-{row['verb']}.html" # "https://konjugator.reverso.net/konjugation-deutsch-verb-besitzen.html"
        payload={}
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'
            , 'Cookie': 'reverso.net._conj_de=de; verb=besitzen'
           }
        response = requests.request("GET", url, headers=headers, data=payload)

        # logger.info(response.text)
        soup = BeautifulSoup(response.text, "html.parser")

        converted_verb_table_row: List[str] = list()
        converted_verb_table_row.append(row["verb"]) # add infinitive
        # converted_verb_table_row.append(row["translate"])
        # converted_verb_table_row.append(row["level"])
        for each_div in soup.find_all("div", {"class": "blue-box-wrap"}):
            if "Indikativ" not in each_div["mobile-title"]:
                continue
            for each_p in each_div.find_all("p"):
                if each_p.getText() == "Präsens":
                    verb_list = each_div.find_all("li")
                    for i in range(0,6):
                        if i < len(verb_list):
                            all_i = verb_list[i].find_all("i")
                            if len(all_i) == 2:
                                converted_verb_table_row.append(all_i[1].getText())
                            elif len(all_i) == 3:
                                converted_verb_table_row.append(f"{all_i[1].getText()} {all_i[2].getText()}")
                        else:
                            converted_verb_table_row.append("N/A")
                elif each_p.getText() == "Präteritum":
                    verb_list = each_div.find_all("li")
                    for i in range(0,6):
                        if i < len(verb_list):
                            all_i = verb_list[i].find_all("i")
                            if len(all_i) == 2:
                                converted_verb_table_row.append(all_i[1].getText())
                            elif len(all_i) == 3:
                                converted_verb_table_row.append(f"{all_i[1].getText()} {all_i[2].getText()}")
                        else:
                            converted_verb_table_row.append("N/A")
                elif each_p.getText() == "Perfekt":
                    verb_list = each_div.find_all("li")
                    for i in range(0,6):
                        all_i = verb_list[i].find_all("i")
                        if len(all_i) == 3:
                            converted_verb_table_row.append(f"{all_i[1].getText()} {all_i[2].getText()}")
                        elif len(all_i) == 4:
                            converted_verb_table_row.append(f"{all_i[1].getText()} {all_i[2].getText()}{all_i[3].getText()}")
                        elif len(all_i) == 5:
                            converted_verb_table_row.append(f"{all_i[1].getText()} {all_i[2].getText()}{all_i[3].getText()}{all_i[4].getText()}")
                        else:
                            converted_verb_table_row.append("N/A")

        time.sleep(0.3) # sleep 300 msec
        converted_verb_table_row_list.append(converted_verb_table_row)

    header_list: List[str] = list()
    header_list.append("Infinitive")
    # header_list.append("translate")
    # header_list.append("level")
    for i in range(0,6):
        header_list.append(f"present_{i+1}")
    for i in range(0,6):
        header_list.append(f"past_{i+1}")
    for i in range(0,6):
        header_list.append(f"perfect_{i+1}")
    converted_verb_df: pd.DataFrame = pd.DataFrame(data=converted_verb_table_row_list, columns=header_list)

    return converted_verb_df

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

def main() -> None:
    """! german_learning_tools main function

    @return None
    """
    logger = lh.init_logger(logger_name="german_learning_tools_logger", is_json_output=False)
    args = init_argparse(description="german_learning_tools Inputs")
    logger.info(f"We get args: {args}")

    # Here put your logic
    verb_table = Get_Verb_Table(verb_inputs=Path(os.path.expanduser("~")
                                                 , "Downloads"
                                                 , "german_verbs.csv")
                                , logger=logger)

    verb_table.to_csv(Path(os.path.expanduser("~"), "Downloads", "converted_german_verbs.csv"))

if __name__ == "__main__":
    main()
