"""
Create a FileManager class responsible for file-related operations
Creating folders for each post and generating file paths.
"""
import os
import shutil
import pathlib

class FileManager:
    
    def __init__(self, base_directory):
        self.base_directory = base_directory

    def create_directory(self):
        """
        Create the directory to store the info/text files.
        """
        if not os.path.isdir(self.base_directory): 
            pathlib.Path(self.base_directory).mkdir(parents=True, exist_ok=True)    
    
    def directory_exists(self):
        """
        Check if a directory exists.
        """
        return os.path.isdir(self.base_directory)

    def file_exists(self, file_path):
        """
        Check if a file exists at the specified path.
        """
        return os.path.isfile(file_path)

    def move_file(self, source_path, destination_path):
        """
        Move a file from the source path to the destination path.
        """
        shutil.move(source_path, destination_path)

    def delete_file(self, file_path):
        """
        Delete a file at the specified path.
        """
        os.remove(file_path)

    def list_files(self, directory_path):
        """
        List all files in the specified directory.
        """
        return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    def get_file_path_relative(self, current_dir, relative_base_dir, file_name) -> str:
        """
        Get the file_name path given the current dir, a relative_base_dir and the file name inside that relative dir
        """
        return os.path.join(current_dir, relative_base_dir, file_name)

    def get_file_path(self, current_dir, file_name) -> str:
        """
        Get the file_name path given the current dir and a file_name dir
        """
        return os.path.join(current_dir, file_name)
