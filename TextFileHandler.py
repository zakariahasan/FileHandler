import os
import hashlib
import shutil

class TextFileComparator:
    """
    A class to search recursively and compare text files with MD5 hashes.
    Saves the matching and non-matching files in separate directories.

    Attributes:
    - root_dir (str): The root directory to search.
    - matching_dir (str): The directory to save matching files.
    - non_matching_dir (str): The directory to save non-matching files.
    """

    def __init__(self, root_dir, dest_dir_1, dest_dir_2):
        """
        Initializes a TextFileComparator object with the specified directories.

        Args:
        - root_dir (str): The root directory to search.
        - matching_dir (str): The directory to save matching files.
        - non_matching_dir (str): The directory to save non-matching files.
        """
        self.root_dir:str = root_dir
        self.matching_dir:str = dest_dir_1
        self.non_matching_dir:str = dest_dir_2

    def md5_hash(self, file_path):
        """
        Computes the MD5 hash of a file.

        Args:
        - file_path (str): The path of the file to hash.

        Returns:
        - The MD5 hash of the file as a string.
        """
        with open(file_path, 'rb') as file:
            return hashlib.md5(file.read()).hexdigest()

    def compare_files(self, file1, file2):
        """
        Compares two files using their MD5 hashes.

        Args:
        - file1 (str): The path of the first file to compare.
        - file2 (str): The path of the second file to compare.

        Returns:
        - True if the files have the same MD5 hash, False otherwise.
        """
        return self.md5_hash(file1) == self.md5_hash(file2)
    def create_directory(path):
        """
        Creates a directory at the given path.
        If the directory already exists, does nothing.

        Args:
        path (str): The path to the directory to be created.
        """
        try:
            os.makedirs(path)
            print(f"Directory created at {path}")
        except FileExistsError:
            print(f"Directory already exists at {path}")
    def search_and_compare(self):
        """
        Searches recursively for text files in the root directory and compares them using MD5 hashes.
        Saves the matching and non-matching files in separate directories.
        """
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            for filename in filenames:
                if filename.endswith('.txt'):
                    file_path = os.path.join(dirpath, filename)
                    matching_path = os.path.join(dirpath.replace(self.root_dir, self.matching_dir), filename)
                    non_matching_path = os.path.join(dirpath.replace(self.root_dir, self.non_matching_dir), filename)
                    #create_directory(os.path.dirname(non_matching_path))
                    if os.path.exists(matching_path) or os.path.exists(non_matching_path):
                        continue
                    for dirpath2, dirnames2, filenames2 in os.walk(self.root_dir):
                        for filename2 in filenames2:
                            if filename2.endswith('.txt'):
                                file_path2 = os.path.join(dirpath2, filename2)
                                if file_path != file_path2:
                                    if self.compare_files(file_path, file_path2):
                                        create_directory(os.path.dirname(matching_path))
                                        shutil.copy2(file_path, matching_path)
                                        shutil.copy2(file_path2, matching_path)
                                        break
                        else:
                            continue
                        break
                    else:
                        create_directory(os.path.dirname(non_matching_path))
                        shutil.copy2(file_path, non_matching_path)
                        
                        
    def remove_duplicates(self):
        """
        Searches for matching files in the matching directory and removes duplicates based on MD5 hash.
        """
        for dirpath, dirnames, filenames in os.walk(self.matching_dir):
            for filename in filenames:
                if filename.endswith('.txt'):
                    file_path = os.path.join(dirpath, filename)
                    for dirpath2, dirnames2, filenames2 in os.walk(self.matching_dir):
                        for filename2 in filenames2:
                            if filename2.endswith('.txt'):
                                file_path2 = os.path.join(dirpath2, filename2)
                                if file_path != file_path2:
                                    if self.compare_files(file_path, file_path2):
                                        os.remove(file_path2)
                                        print(f"Removed duplicate file {file_path2}")
                                        


    def generate_hashes(self):
            
        """
        Generate MD5 hashes for all files in the root directory and its subdirectories.
        Returns:
        A dictionary of dictionaries, where each key represents a subdirectory
        (relative to the root directory), and each value is a dictionary of file names
        and their corresponding MD5 hashes.

        Example:
        {
            'subdir1': {
                'file1.txt': '3f3fc807b26a4e87d4f28e4f80ee46b4',
                'file2.txt': 'c30110b0278f1db88c0b1e98d6c29014',
            },
            'subdir2': {
                'file3.txt': '6d3c1b2664a4a2024fb4b4ab46d6f510',
            },
        }
        """   
        hashes = {}
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
                subfolder = os.path.relpath(dirpath, self.root_dir)
                if subfolder not in hashes:
                    hashes[subfolder] = {}
                hashes[subfolder][filename] = file_hash
        return hashes


    def remove_duplicate_values(self):
        # Iterate through the keys of the dictionary
        d=self.generate_hashes()
        print(d)
        for key1 in list(d.keys()):
            # Iterate through the keys of the dictionary again
            for key2 in list(d.keys()):
                # Compare the values of the keys
                if key1 != key2 and d[key1] == d[key2]:
                    # Delete the key if there is a match
                    del d[key1]
                    break
        print(d)
        return d

    def copy_only_original_directory(self):
        folders = list(self.remove_duplicate_values())
        print(folders)
        logging.debug(f'{folders}')
        for i in range(len(folders)):
            src = os.path.join(self.root_dir,folders[i])
            #logging.debug('src',src)
            dest = os.path.join(self.matching_dir,folders[i])
            #self.create_directory(os.path.dirname(dest))
            logging.debug(f'dest: {dest}')
            shutil.copytree(src, dest,dirs_exist_ok=True)
            #logging.debug(f'copying {src}')
