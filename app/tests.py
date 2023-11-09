import os
import pytest
import shutil
from sync import folder_sync, create_folder_if_not_exists, compare_files, copy_or_update_file

# Create a temporary test directory
@pytest.fixture(scope="module")
def test_directory(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("test_directory")
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_create_folder_if_not_exists(tmp_path):
    test_folder = os.path.join(tmp_path, "test_folder")

    # Test creating a folder that doesn't exist
    create_folder_if_not_exists(test_folder)
    assert os.path.isdir(test_folder)

    # Test creating a folder that already exists
    create_folder_if_not_exists(test_folder)
    assert os.path.isdir(test_folder)

def test_compare_files():
    # Create temporary test files
    with open("file1.txt", "w") as f1, open("file2.txt", "w") as f2:
        f1.write("content")
        f2.write("content")

    with open("file3.txt", "w") as f1, open("file4.txt", "w") as f2:
        f1.write("different_content")
        f2.write("different_content")

    assert compare_files("file1.txt", "file2.txt")  # Identical files
    assert not compare_files("file1.txt", "file3.txt")  # Different files

def test_copy_or_update_file(tmp_path):
    source_folder = tmp_path / "source"
    replica_folder = tmp_path / "replica"

    # Create source and replica folders
    create_folder_if_not_exists(source_folder)
    create_folder_if_not_exists(replica_folder)

    source_file = source_folder / "file.txt"
    replica_file = replica_folder / "file.txt"

    # Test copying a file
    with open(source_file, "w") as f:
        f.write("content")
    log_message = copy_or_update_file(source_file, replica_file)
    assert os.path.exists(replica_file)
    assert log_message == f'{source_file} has been copied to the replica.'

    # Test updating an identical file
    log_message = copy_or_update_file(source_file, replica_file)
    assert log_message == f'{source_file} is already up to date.'

    # Test updating a different file
    with open(source_file, "w") as f:
        f.write("new_content")
    log_message = copy_or_update_file(source_file, replica_file)
    assert log_message == f'{source_file} has been updated.'

def test_folder_sync(tmp_path, capsys):
    source_folder = tmp_path / "source"
    replica_folder = tmp_path / "replica"
    log_file = "test_log.txt"

    create_folder_if_not_exists(source_folder)
    create_folder_if_not_exists(replica_folder)

    with open(source_folder / "file1.txt", "w") as f1, open(replica_folder / "file1.txt", "w") as f2:
        f1.write("content")
        f2.write("content")

    capsys.readouterr()  # Clear captured output

    # Run folder_sync with a short time interval for testing
    folder_sync(source_folder, replica_folder, log_file, 1)
    captured = capsys.readouterr()

    # Verify that the program runs and outputs synchronization messages
    assert os.path.exists(replica_folder / "file1.txt")
    assert "The program has been terminated manually." not in captured.out
