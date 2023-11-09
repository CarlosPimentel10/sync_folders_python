import os
import argparse
import logging
import time
import hashlib
import shutil

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def compare_files(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        return hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()

def copy_or_update_file(source_path, replica_path):
    if os.path.exists(replica_path):
        if compare_files(source_path, replica_path):
            return f'{source_path} is already up to date.'
        else:
            os.remove(replica_path)
            shutil.copy2(source_path, replica_path)
            return f'{source_path} has been updated.'
    else:
        shutil.copy2(source_path, replica_path)
        return f'{source_path} has been copied to the replica.'

def folder_sync(source_folder, replica_folder, log_file, time_interval):
    create_folder_if_not_exists(replica_folder)
    
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')
    
    while True:
        try:
            logging.info(f"Start synchronization from {source_folder} to {replica_folder} every {time_interval} seconds.")
            source_files = os.listdir(source_folder)
            replica_files = os.listdir(replica_folder)
            
            for file in source_files:
                source_file_path = os.path.join(source_folder, file)
                replica_file_path = os.path.join(replica_folder, file)
                
                log_message = copy_or_update_file(source_file_path, replica_file_path)
                logging.info(log_message)
                print(log_message)
            
            time.sleep(time_interval)
        except KeyboardInterrupt:
            print("The program has been terminated manually.")
            raise SystemExit

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Folder synchronization program')
    parser.add_argument('--source', type=str, default="source", help='Source folder path')
    parser.add_argument('--replica', type=str, default="replica", help='Replica folder path')
    parser.add_argument('--log-file', type=str, default='log.txt', help='Log file path')
    parser.add_argument('--time-interval', type=int, default=60, help='Time interval for synchronization in seconds')
    args = parser.parse_args()

    folder_sync(args.source, args.replica, args.log_file, args.time_interval)
