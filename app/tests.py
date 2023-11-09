import os
import pytest
import shutil

from sync import folder_sync,folder_comparison, file_comparison

# Create a temporary test directory
@pytest.fixture(scope="module")
def test_directory(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("test_directory")
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_folder_sync_create_folder(test_directory):
    source = os.path.join(test_directory, "source")
    replica = os.path.join(test_directory, "replica")
    log = os.path.join(test_directory, "log.txt")
    time_frame = 1

    # Create the source folder within the test directory
    os.makedirs(source)

    folder_sync(source, replica, log, time_frame)

    assert os.path.isdir(source)
    assert os.path.isdir(replica)
    assert os.path.isfile(log)

def test_file_comparison():
    file1 = "test_file1.txt"
    file2 = "test_file2.txt"
    file3 = "test_file3.txt"

    with open(file1, "w") as f:
        f.write("content")

    with open(file2, "w") as f:
        f.write("content")

    with open(file3, "w") as f:
        f.write("different_content")

    assert file_comparison(file1, file2)  # Identical files
    assert not file_comparison(file1, file3)  # Different files

def test_folder_comparison(tmp_path):
    test_directory = tmp_path
    source = os.path.join(test_directory, "source")
    replica = os.path.join(test_directory, "replica")

    os.makedirs(source)
    os.makedirs(replica)

    # Create test files
    source_file1 = os.path.join(source, "file1.txt")
    replica_file1 = os.path.join(replica, "file1.txt")
    with open(source_file1, "w") as f:
        f.write("content")

    source_file2 = os.path.join(source, "file2.txt")
    replica_file2 = os.path.join(replica, "file2.txt")
    with open(source_file2, "w") as f:
        f.write("different_content")

    folder_comparison(source, replica)

    assert os.path.isfile(replica_file1)  # File 1 is copied
    assert os.path.isfile(replica_file2)  # File 2 is copied

    # Check if content is the same
    with open(source_file1, "r") as f1, open(replica_file1, "r") as f2:
        assert f1.read() == f2.read()

    with open(source_file2, "r") as f1, open(replica_file2, "r") as f2:
        assert f1.read() == f2.read()
