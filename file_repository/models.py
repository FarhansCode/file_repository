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
