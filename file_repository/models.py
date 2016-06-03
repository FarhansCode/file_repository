from __future__ import unicode_literals
from django.db import models
import os, re

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

    def create_file(self, name, content):
        try:
            exists = self.inodes.get(name=name)
            raise Inode.NameConflict(name)
        except Inode.DoesNotExist:
            pass

        new_file = Inode(is_directory=False)
        new_file.content = content
        new_file.name = name
        new_file.save()
        self.inodes.add(new_file)
        return new_file

    def create_directory(self, name):
        try:
            exists = self.inodes.get(name=name)
            raise Inode.NameConflict(name)
        except Inode.DoesNotExist:
            pass

        new_directory = Inode(is_directory=True)
        new_directory.name = name
        new_directory.save()
        self.inodes.add(new_directory)
        return new_directory

    def deletenode(self):
        if self.is_directory == False:
            os.remove(self.content.path)
            self.delete()
        else:
            # Recursively go through all subdirectories
            directories = self.inodes.filter(is_directory = True)
            for dir_inode in directories:
                dir_inode.deletenode()
            # Now delete them all
            directories.all().delete()
            # And then wipe out the files
            files = self.inodes.filter(is_directory = False)
            for subfile in files:
                subfile.deletenode()
            self.delete()

    class methods:
        def createroot(rootname):
            newroot = Inode(name='/', rootname=rootname, is_directory=True)
            newroot.save()
            return newroot

        def getroot(rootname):
            root = Inode.objects.get(name='/',
                                     rootname=rootname,
                                     is_directory=True)
            return root

        def getinode(filedir, rootname):

            try: # Get the root or die
                rootdirectory = Inode.objects.get(rootname=rootname,
                                                  name='/',
                                                  is_directory=True)
            except Inode.DoesNotExist:
                raise Inode.Error500('rootname %s does not exist' % rootname)

            if filedir == '' or filedir == '/':
                return rootdirectory # Quit if its just the root

            current_directory = rootdirectory
            tempurl = filedir
            while tempurl:
                lastnode = re.match('^(\/)?([\w\.]+)?(\/?)$', tempurl)
                if lastnode is not None:
                    try:
                        if lastnode.group(1) is '/' and \
                           lastnode.group(2) is None:
                            return current_directory
                        elif lastnode.group(2) is not None:
                            inode = current_directory.inodes.get(
                                                name=lastnode.group(2))
                            if inode.is_directory == True and \
                              lastnode.group(3) is not '/':
                                raise Inode.Redirect302(filedir+'/')
                            return inode
                    except Inode.DoesNotExist:
                        raise Inode.Error404

                response = re.match('^([\w\-\.\ ]+)\/([\w\-\.\ \/]+)', tempurl)
                if response == None: # Its the last node, kick it back up
                    continue
                tree, tempurl = response.groups()
                if tree: # This is a directory
                    current_directory = current_directory.inodes.get(name=tree,
                                                             is_directory=True)
                    continue

    class Error404(Exception):
        def __str__(self):
            return repr("Inode does not exist")
    class Error500(Exception):
        def __init__(self, msg):
            self.msg = msg
        def __str__(self):
            return repr(self.msg)
    class Redirect302(Exception):
        def __init__(self, path):
            self.newpath = path
    class NameConflict(Exception):
        def __init__(self, name):
            self.name = name
        def __str__(self):
            return repr("Inode %s already exists" % self.name)
