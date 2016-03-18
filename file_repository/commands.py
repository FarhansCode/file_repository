from file_repository.models import Inode
import os

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

def get_path(inode):
    path = ''
    rootpath = inode

    while True:
        if rootpath.inode_set.count() == 1:
            rootpath = rootpath.inode_set.get()
            if rootpath.name is not '':
                path = rootpath.name + '/' + path
            else:
                break
        else: # This should never happen unless the directory is doubly linked 
            break

    return path
