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
   new_root = Inode(name='root', rootname=rootname, is_directory=True)
   new_root.save()
   return new_root
