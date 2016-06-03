from file_repository.models import Inode
import os, re

# Recursive function to delete both files and directories
def del_inode(inode):
    # Recursively go through all subdirectories
    directories = inode.inodes.filter(is_directory = True)
    for dir_inode in directories:
        del_inode(dir_inode) 
    # Now delete them all
    directories.all().delete()
    # And then wipe out the files
    files = inode.inodes.filter(is_directory = False)
    for subfile in files:
        os.remove(subfile.name) # Delete files from the HD
    # Now delete the inode links from the DB
    files.all().delete()

def create_root(rootname):
    new_root = Inode(name='', rootname=rootname, is_directory=True)
    new_root.save()
    return new_root

def create_file(parent, name, content):
    new_file = Inode(is_directory=False)
    new_file.content = content
    new_file.name = name
    new_file.save()
    parent.inodes.add(new_file)
    return new_file

def create_directory(parent, name):
    new_directory = Inode(is_directory=True)
    new_directory.name = name
    new_directory.save()
    parent.inodes.add(new_directory)
    return new_directory

def get_inode(filedir, rootname):

    try: # Get the root or die
        rootdirectory = Inode.objects.get(rootname=rootname,
                                          name='/',
                                          is_directory=True)
    except Inode.DoesNotExist:
        error_inode = Inode(rootname=rootname, name='/', is_directory=True)
        error_inode.error = 500 
        return error_inode

    if filedir == '' or filedir == '/':
        return rootdirectory # Quit if its just the root

    current_directory = rootdirectory
    tempurl = filedir
    while tempurl:
        lastnode = re.match('^(\/)?([\w\.]+)?(\/?)$', tempurl)
        if lastnode is not None:
            try:
                if lastnode.group(1) is '/' and lastnode.group(2) is None:
                    return current_directory
                elif lastnode.group(2) is not None:
                    return current_directory.inodes.get(name=lastnode.group(2)) 
            except Inode.DoesNotExist:
                current_directory.error = 404
                return current_directory

        response = re.match('^([\w\-\.\ ]+)\/([\w\-\.\ \/]+)', tempurl)
        if response == None: # Its the last node, kick it back up
            continue
        tree, tempurl = response.groups()
        if tree: # This is a directory
            current_directory = current_directory.inodes.get(name=tree, is_directory=True)
            continue
