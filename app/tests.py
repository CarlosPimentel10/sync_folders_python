import os 
from sync import folder_sync

def test_folder_sync():
    source = 'source_folder'
    replica = 'replica_folder'
    log = 'log_file'
    time_frame = 5

    os.makedirs(source, exist_ok=True)
    with open(os.path.join(source, 'test.txt'), 'w') as f:
        f.write("LOREM IPSUM LOREM IPSUM")
    try:
        folder_sync(source=source, replica=replica, log=log, time_frame=time_frame)

        assert os.path.isdir(replica)
        assert os.path.isfile(os.path.join(replica, 'test_file.txt'))
    finally:
        os.remove(os.path.join(source, 'test.txt'))
        os.rmdir(source)
        os.rmdir(replica)