from __future__ import unicode_literals
from django.db import models

# Single inode model for both files and directories

class Inode(models.Model):
    # This will only be specified if Inode is a root
    rootname = models.CharField(max_length=10, default='')

    name = models.CharField(max_length=255)
    # True = Directory, False = File
    is_directory = models.BooleanField(default=False)
    # Only makes sense if its a file
    content = models.FileField(upload_to='file_repository/_files')
    # Only makes senes if its a directory
    inodes = models.ManyToManyField('Inode')

    def __str__(self):
        return self.name

    def get_path(self):
        path = ''
        rootpath = self 

        while True:
            if rootpath.inode_set.count() == 1:
                rootpath = rootpath.inode_set.get()
                if rootpath.name is not '/': # Not last element
                    path = rootpath.name + '/' + path
                elif rootpath.name is '/': # Last element
                    path = '/' + path
                    break
            else: # Only for root elements
                path = '/' + path
                break
        return path
