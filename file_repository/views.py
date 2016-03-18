from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from file_repository.models import Inode

import re

def get_inode(filedir, rootname):

   # Get rid of //'s, do a redirection if necessary
   if filedir != None:
      tempurl = filedir
      while True:
         newtempurl = tempurl.replace('//', '/')
         if newtempurl == tempurl:
            break
         tempurl = newtempurl
      if filedir != tempurl:
         return (301, None, None, ('' if tempurl[:1]=='/' else '/') + tempurl)
      ### End of the block
      filedir = tempurl
   else:
      tempurl = filedir
   # End of redirection block

   # Set their default values, starting at the root directory
   current_directory = Inode.objects.get(rootname=rootname)
   current_file = None

   ### Find the path
   while tempurl:
      # Check if its the last node
      lastnode = re.match('^([\w|\-|\.]+)\/?$', tempurl)
      if lastnode: #
         if current_directory.inodes.filter( name=lastnode.group(1), is_directory=True ).count() == 1:
            # We've found that its a directory, keep going
            current_directory = current_directory.inodes.get(name=lastnode.group(1), is_directory=True)
         elif current_directory.inodes.filter( name=lastnode.group(1), is_directory=False ).count() == 1:
            # Its a file, send back the file
            current_file = current_directory.inodes.get(name=lastnode.group(1), is_directory=False) 
            return (200, current_directory, current_file, None)
         else:
            return (404, None, None, None)
         break

      tree = re.match('^([\w|\-|\.]+)\/(.+)', tempurl)
      # Not the last node, then its a Directory
      if tree: # This is a directory
         new_subdir = tree.group(1)
         tempurl = tree.group(2)
         try:
            current_directory = current_directory.inodes.get(name=new_subdir, is_directory=True)
         except Inode.DoesNotExist:
            return (404, None, None, None)
      else:
         break
   ### End of finding the path

   ### If its a directory, put in trailing /
   if current_file == None: # Its a directory
      if filedir != None and filedir[-1:] != '/':
         return (301, None, None, filedir + '/')
   ### Accept final trialing /

   # Send back the local directory
   return (200, current_directory, None, None)
