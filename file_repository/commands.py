from file_repository.models import Inode
import re

def create_root(rootname):
    new_root = Inode(name='/', rootname=rootname, is_directory=True)
    new_root.save()
    return new_root

def get_root(rootname):
    root = Inode.objects.get(name='/', rootname=rootname, is_directory=True)
    return root

def get_inode(filedir, rootname):

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
                if lastnode.group(1) is '/' and lastnode.group(2) is None:
                    return current_directory
                elif lastnode.group(2) is not None:
                    inode = current_directory.inodes.get(name=lastnode.group(2))
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
