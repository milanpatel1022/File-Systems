
from pathlib import Path
from pathlib import PurePosixPath
import os
import shutil

def dir_or_subdir() -> list:
    """ Asks user for valid path to directory and calls the 'D' or 'R' function & checks for errors in formatting of input"""
    what_files = str(input())
    p = what_files[2:]
    path = Path(p)
    #check if format of input is correct
    while what_files == '' or (what_files[0] != 'D' and what_files[0] != 'R') or path.is_dir() != True:
        print('ERROR')
        what_files = str(input())
        p = what_files[2:]
        path = Path(p)
    #print the result of the call to the 'only_directories' function that handles only the first directory and returns a list of the files within it
    if what_files[0] == 'D':
        print_files(only_directories(path))
        return only_directories(path)
    #print the result of the call to the 'also_subdirectories' function that handles the directory and its subdirectories and returns a list of the files within it
    elif what_files[0] == 'R':
        print_files(also_subdirectories(path))
        return also_subdirectories(path)


def which_files(list_of_files: list) -> None:
    """ ASKS FOR SECOND USER INPUT to decide which files should be filtered as interesting & checks for errors in formatting of input"""
    interesting_files = str(input())
    #depending on what the user inputs, call a certain function
    if len(interesting_files) == 1 and interesting_files == 'A':
        all_files(list_of_files)
    elif len(interesting_files) > 1 and interesting_files[0] == 'N':
        certain_name_files(interesting_files, list_of_files)
    elif len(interesting_files) > 1 and interesting_files[0] == 'E':
        file_extension(interesting_files, list_of_files)
    elif len(interesting_files) > 1 and interesting_files[0] == 'T':
        text_file_search(interesting_files, list_of_files)
    elif len(interesting_files) > 1 and interesting_files[0] == '<':
        max_file_size = interesting_files[2:]
        if max_file_size.isdigit() is False or int(max_file_size) < 0:
            print('ERROR')
            which_files(list_of_files)
        else:
            file_less_than(max_file_size, list_of_files)
    elif len(interesting_files) > 1 and interesting_files[0] == '>':
        min_file_size = interesting_files[2:]
        if min_file_size.isdigit() is False or int(min_file_size) < 0:
            print('ERROR')
            which_files(list_of_files)
        else:
            file_greater_than(min_file_size, list_of_files)
    #if none of the above are user inputs, print 'Error' and keep calling the function until the user enters valid info.
    else:
        print('ERROR')
        which_files(list_of_files)


def action_on_files(narrowed_down_files: list) -> None:
    """ 3RD USER INPUT that asks what action user wants to take on the interesting files & checks for errors in formatting of input"""
    what_action = str(input())
    #check if input is valid. if it's not print error and keep asking for input.
    while len(what_action) != 1 or (what_action[0] != 'F' and what_action[0] != 'D' and what_action[0] != 'T'):
        print('ERROR')
        what_action = str(input())
    #depending on the letter in input, call the corresponding function
    if what_action[0] == 'F':
        print_first_line(narrowed_down_files)
    elif what_action[0] == 'D':
        duplicate_file(narrowed_down_files)
    elif what_action[0] == 'T':
        modify_timestamp(narrowed_down_files)


def all_files(list_of_files: list) -> list:
    """ All files are considered interesting and are sent to another function to be printed """
    interesting_files = list_of_files
    print_files(interesting_files)
    action_on_files(interesting_files)
    return interesting_files


def certain_name_files(interesting_files: str, list_of_files: list) -> list:
    """ Files with same name provided are considered interesting & printed again """
    same_name_files = [ ]
    filepath = interesting_files[2:]
    #File paths are different on windows and Mac/Linux, so convert all files to the same format and then check for the name
    for file in list_of_files:
        convertedfile = file.as_posix()
        convertedfile = PurePosixPath(convertedfile)
        if PurePosixPath(convertedfile).name == filepath:
            same_name_files.append(file)
    #if there are matching files, call print function and 3rd user input to continue the program
    if len(same_name_files) > 0:
        print_files(same_name_files)
        action_on_files(same_name_files)
    return same_name_files


def file_extension(interesting_files: str, list_of_files: list) -> list:
    """ Files with same extension are considered interesting & printed again """
    files_with_extension = [ ]
    extension = interesting_files[2:]
    for file in list_of_files:
        filename, file_ext = os.path.splitext(file)
        noperiod = file_ext[1:]
        if extension == noperiod or extension == file_ext:
            files_with_extension.append(file)
    if len(files_with_extension) > 0:
        print_files(files_with_extension)
        action_on_files(files_with_extension)
    return files_with_extension


def text_file_search(interesting_files: str, list_of_files: list) -> list:
    """ Text files that have the same text provided by user input are considered interesting"""
    files_with_text = [ ]
    text_to_be_read = interesting_files[2:]
    for item in list_of_files:
        #set file = None so if its value changes we know it has been opened and know to close it
        file = None
        try:
            file = open(item, 'r')
            if text_to_be_read in file.read():
                files_with_text.append(item)
        #exception for jpg files or others that aren't text files
        except UnicodeDecodeError:
            pass
        finally:
            if file is not None:
                file.close()
    if len(files_with_text) > 0:
        print_files(files_with_text)
        action_on_files(files_with_text)
    return files_with_text


def file_less_than(max_file_size: str, list_of_files: list) -> list:
    """ Files smaller in size than the number provided in the second user input are considered interesting & printed again """
    smaller_files = [ ]
    max_file_size = int(max_file_size)
    for file in list_of_files:
        fileinfo = Path.stat(file)
        if fileinfo.st_size < max_file_size:
            smaller_files.append(file)
    if len(smaller_files) > 0:
        print_files(smaller_files)
        action_on_files(smaller_files)
    return smaller_files


def file_greater_than(min_file_size: str, list_of_files: list) -> list:
    """ Files greater in size than the number provided in the second user input are considered interesting & printed again """
    larger_files = [ ]
    min_file_size = int(min_file_size)
    for file in list_of_files:
        fileinfo = Path.stat(file)
        if fileinfo.st_size > min_file_size:
            larger_files.append(file)
    if len(larger_files) > 0:
        print_files(larger_files)
        action_on_files(larger_files)
    return larger_files


def print_first_line(narrowed_down_files: list) -> list:
    """ Prints first line of each text file """
    linelist = [ ]
    for file in narrowed_down_files:
        the_file = None
        try:
            the_file = open(file, 'r')
            #get a list containing each line in the file; the first index is the first line
            list_of_lines = the_file.read().splitlines()
            linelist.append(list_of_lines[0])
        #exception for a file that is not a text file
        except ValueError:
            linelist.append('NOT TEXT')
        finally:
            if the_file != None:
                the_file.close()
    print_files(linelist)
    return linelist


def duplicate_file(narrowed_down_files: list) -> None:
    """ Makes a duplicate copy of each file and stores it in the same directory as the original"""
    for file in narrowed_down_files:
        root, ext = os.path.splitext(file)
        shutil.copy(file, root + ext + ".dup")


def modify_timestamp(narrowed_down_files: list) -> None:
    """ Updates the file's last modification to the current date/time """
    for file in narrowed_down_files:
        Path.touch(file)


def only_directories(path) -> list:
    """ Returns list of all files in directory when given path """
    list_of_files = [ ]
    for object in path.iterdir():
        if not object.is_dir():
            list_of_files.append(object)
    list_of_files.sort()
    return list_of_files


def also_subdirectories(path) -> list:
    """ Returns list of all files in directory and its subdirectories when given path """
    list_of_files = [ ]
    for object in path.iterdir():
        if not object.is_dir():
            list_of_files.append(object)
    #sort after each directory and extend the subdirectories so the sorting is not mixed up between directories
    list_of_files.sort()
    for object in path.iterdir():
        if object.is_dir():
            list_of_files.extend(also_subdirectories(object))
    return list_of_files


def print_files(lst: list) -> None:
    """ Prints files in a list """
    for file in lst:
        print(file)


if __name__ == '__main__':
    list_of_files = dir_or_subdir()
    which_files(list_of_files)
