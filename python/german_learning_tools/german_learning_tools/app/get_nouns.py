# Imports
import argparse
import logging
import os
import requests
import pandas as pd
import time
import traceback
import sys
from pathlib import Path
from bs4 import BeautifulSoup # poetry add beautifulsoup4

import sfdevtools.observability.log_helper as lh

def Get_Noun_Table(noun_inputs: Path
                   , logger: logging.Logger):
    nouns: pd.DataFrame = pd.read_csv(noun_inputs)
    converted_nouns_table_row_list: List[List[str]] = list()
    for idx, row in nouns.iterrows():
        logger.info(f"processing noun: {row['noun']}")

        try:
            url = f"https://de.wiktionary.org/wiki/{row['noun']}" # "https://de.wiktionary.org/wiki/Buch"
            payload={}
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'
                , 'Cookie': 'reverso.net._conj_de=de; verb=besitzen'
               }
            response = requests.request("GET", url, headers=headers, data=payload)

            # logger.info(response.text)
            soup = BeautifulSoup(response.text, "html.parser")

            converted_noun_table_row: List[str] = list()
            converted_noun_table_row.append(row["level"])
            converted_noun_table_row.append("n")
            converted_noun_table_row.append(row["noun"]) # add infinitive
            converted_noun_table_row.append(row["translate"])
            for each_table in soup.find_all("table", {"class": "wikitable"}):
                all_th = each_table.find_all("th")

                # check if the target table
                is_noun_found: int = -1 # -1: not found, 1: Singular,Plural, 2: Singular,..,Plural 3: Singular,..,..,Plural
                all_th = each_table.find_all("th")
                if "Singular" in all_th[1].getText() and "Plural" in all_th[2].getText():
                    is_noun_found = 1
                elif "Singular" in all_th[1].getText() and "Plural" in all_th[3].getText():
                    is_noun_found = 2
                elif "Singular" in all_th[1].getText() and "Plural" in all_th[4].getText():
                    is_noun_found = 3
                else:
                    logger.warn(f"not support format. skip noun: {row['noun']}")
                    continue

                all_td = [each_td for each_td in each_table.find_all("td")]
                converted_noun_table_row.append(all_td[0].getText().replace("\n", ""))
                if is_noun_found == 1:
                    converted_noun_table_row.append(all_td[1].getText().replace("\n", ""))
                elif is_noun_found == 2:
                    converted_noun_table_row.append(all_td[2].getText().replace("\n", ""))
                elif is_noun_found == 3:
                    converted_noun_table_row.append(all_td[3].getText().replace("\n", ""))

                # DONE, not need to look for the next table in the same page
                break

            logger.info(f"done noun: {row['noun']}")
            time.sleep(0.3) # sleep 300 msec
            converted_nouns_table_row_list.append(converted_noun_table_row)
        except Exception:
            logger.error(traceback.format_exc())
            logger.error(f"fail noun: {row['noun']}")


    header_list: List[str] = list()
    header_list.append("level")
    header_list.append("type")
    header_list.append("Infinitive")
    header_list.append("translate")
    header_list.append("singular")
    header_list.append("plural")

    try:
        converted_nouns_df: pd.DataFrame = pd.DataFrame(data=converted_nouns_table_row_list, columns=header_list)
        return converted_nouns_df
    except Exception:
        logger.error(traceback.format_exc())

        logger.info("converted_nouns_table_row_list:")
        logger.info(converted_nouns_table_row_list)

        return None


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
    """! german_get_nouns main function

    @return None
    """
    logger = lh.init_logger(logger_name="german_get_nouns_logger", is_json_output=False)
    args = init_argparse(description="german_get_nouns Inputs")
    logger.info(f"We get args: {args}")

    # Here put your logic
    noun_table = Get_Noun_Table(noun_inputs=Path(os.path.expanduser("~")
                                                 , "Downloads"
                                                 , "german_nouns.csv")
                                , logger=logger)

    if noun_table is not None:
        noun_table.to_csv(Path(os.path.expanduser("~"), "Downloads", "converted_german_nouns.csv"))
        logger.info(f"output csv success")
    else:
        logger.warn(f"no csv output")

if __name__ == "__main__":
    main()
