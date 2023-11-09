import os
import argparse
import logging
import time

def folder_sync(source, replica, log, time_frame):
    # check if directory exists
    if not os.path.isdir(replica):
        os.makedirs(replica)
    if not os.path.source.isdir(source):
        raise argparse.ArgumentError(None, "The source folder doesn't exist.")
    
    logging.info(f"Start with parameters:\nsource:{source}\nreplica:{replica}\nlog:{log}\ntime_interval:{time_frame}\n")
    
    while True:
        try:
            folder_comparison(source, replica)
            time.sleep(time_frame)
        except KeyboardInterrupt:
            print("The Program is terminated manually!")
            raise SystemExit
        
        def folder_comparison():
            pass
        
        