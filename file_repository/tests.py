from django.test import TestCase
from file_repository.models import Inode

# Create your tests here.

class CreateRootTestCase(TestCase):
    def test_create_root(self):
        root = Inode.methods.createroot('testapp')
        self.assertEqual(root.name, '/')
        self.assertEqual(root.rootname, 'testapp')
        self.assertEqual(root.is_directory, True)

class GetRootTestCase(TestCase):
    def setUp(self):
        root = Inode.methods.createroot(rootname='testapp')
    def test_get_root(self):
        root = Inode.methods.getroot('testapp')

class BuildUponRootTestCase(TestCase):
    def setUp(self):
        root = Inode.methods.createroot('testapp')
    def test_create_directory_on_root(self):
        root = Inode.methods.getroot('testapp')

        newdirectory = root.create_directory('new_directory')
        self.assertEqual(newdirectory.name, 'new_directory')
        newdirectory.inode_set.get(id=root.id)
    def test_create_file_on_root(self):
        root = Inode.objects.get(name='/')

        newfile = root.create_file('testfile', 'Junk Content')
        self.assertEqual(newfile.name, 'testfile')
        newfile.inode_set.get(id=root.id)

class DeleteNodeTestCase(TestCase):
    def setUp(self):
        root = Inode.methods.createroot('testapp')
        newdirectory = root.create_directory('new_directory')
        subdirectory = newdirectory.create_directory('subdirectory')
        lastdirectory = subdirectory.create_directory('lastdirectory')
    def test_delete_node(self):
        root = Inode.methods.getroot('testapp') 
        newdirectory = root.inodes.get()

        self.assertEqual(root.inodes.count(), 1)
        self.assertEqual(Inode.objects.count(), 4)

        newdirectory.deletenode()

        self.assertEqual(root.inodes.count(), 0)
        self.assertEqual(Inode.objects.count(), 1)

class GetInodeTestCase(TestCase):
    def setUp(self):
        root = Inode.methods.createroot('testapp')
        newdirectory = root.create_directory('new_directory')
        subdirectory = newdirectory.create_directory('subdirectory')
        self.lastdirectory = subdirectory.create_directory('lastdirectory')

    def test_get_inode_with_slash(self):
        root = Inode.methods.getroot('testapp')
        i = Inode.methods.getinode('new_directory/subdirectory/lastdirectory/', 'testapp')
        self.assertEqual(self.lastdirectory, i)
    def test_get_node_without_slash(self):
        root = Inode.methods.getroot('testapp')
        try:
            i = Inode.methods.getinode('new_directory/subdirectory/lastdirectory',
                          'testapp')
        except Inode.Redirect302 as e:
            self.assertEqual(e.newpath,
                             'new_directory/subdirectory/lastdirectory/')
    def test_nonexistent_node(self):
        root = Inode.methods.getroot('testapp')
        try:
            i = Inode.methods.getinode('lkasjdfklajsfkljasklf', 'testapp')
        except Inode.Error404:
            self.assertTrue(True)

    def test_nonexistent_root(self):
        try:
            i = Inode.methods.getinode('alskdfj', 'does-not-exist')
        except Inode.Error500:
            self.assertTrue(True)
