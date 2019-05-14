#!/usr/bin/env python
__author__ = "Yadollah Shahryary Dizaji"
__title__ = "setup.py"
__description__ = "Setup file for Pipeline."
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "shahryary@gmail.com"

from globalParameters import *
from part_trimmomatic import run_trimmomatic
from part_fastq import run_fastQC
from part_bismark import run_bimark_mapper
from part_bismark_dedup import run_bimark_dedup
from part_methimpute import info_methimpute

def run_quick():

    try:
        preparing_part()
        '''
        pipeline.conf
        0: not yet run 
        1: bug during run 
        2: successfully run  
        '''

        if confirm_run():

            if int(read_config("STATUS", "st_trim")) != 2:
                print "==" * 40
                print qucolor("Running Trimmomatic Part...")
                run_trimmomatic(True)

            if int(read_config("STATUS", "st_fastq")) != 2:
                print "==" * 40
                print qucolor("Running FastQC Part...")
                run_fastQC(True)

            if int(read_config("STATUS", "st_bismark")) != 2:
                print "==" * 40
                print qucolor("Running Bismark Part...")
                run_bimark_mapper(True)

            if int(read_config("STATUS", "st_bisdedup")) != 2:
                print "==" * 40
                print qucolor("Running Bismark-deduplicate Part...")
                run_bimark_dedup(True)

            # if ==2 that's mean sorted
            if int(read_config("STATUS", "st_bissort")) == 2:
                print "==" * 40
                print qucolor("Running Methimpute Part...")
                replace_config("GENERAL", "parallel_mode", "false")
                subprocess.call(['./src/bash/gen-rdata.sh'])
                print(info_methimpute())
                subprocess.call(['./src/bash/methimpute-bam.sh'])

            message(0, "Processing files are finished, results are in :"
                    + read_config("Others", "tmp_meth_out"))
    except Exception as e:
        logging.error(traceback.format_exc())
        print(rcolor(e.message))
        message(2, "something is going wrong... please run again. ")
        # set 1 to resuming
        replace_config("STATUS", "st_methimpute", "1")
    return