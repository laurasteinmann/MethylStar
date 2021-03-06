#!/usr/bin/env python
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"

from globalParameters import *


def info_cx():
    title("Generating Cytosine Calls")
    s = gcolor("Configuration Summary:\n")+\
        ""+"\n"\
    "- Bismark location: " + mcolor(read_config("Bismark", "bismark_path")) + "\n" \
    "- Parallel mode: " + mcolor(true_false_fields_config(read_config("GENERAL", "parallel_mode"))) + "\n" \

    status = int(read_config("STATUS", "st_cx"))

    if status == 1:
        s += "\n--> Please ensure that folder is empty, otherwise it will overwrite the files ..."

    if status == 2:
        if len(check_empty_dir("cx-reports", "*.txt")) > 0:
            s += "\nIt seems you have results for Generate Cytosine Calls."
            s += "You can re-run this part, but we recommend move the files to another folder and run again. \n"
            s += "WARNING: The directory is not empty,re-running this part might loosing the existing data!"
        else:
            s += "Couldn't find any CX file starting to run the CX reports... "

    return s


def run_cx():

    try:
        preparing_part()
        print(info_cx())
        txt = "Cx generator Part finished."
        if confirm_run():
            print qucolor("\nRunning CX Reports ...")
            subprocess.call(['./src/bash/cx-generator.sh'])
            # running methimpute
            # email part
            if read_config("EMAIL", "active") == "true":
                parmEmail(txt)
            message(0, "Processing files is finished, You can check the logs in Menu, part 'Bismark-log' ")

    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        txt = e.message
        if read_config("EMAIL", "active") == "true":
            parmEmail(txt)
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "st_cx", "1")


    return
