from django.test import TestCase
from file_repository.models import Inode
from file_repository.commands import create_root, get_root, get_inode

# Create your tests here.

class CreateRootTestCase(TestCase):
    def test_create_root(self):
        root = create_root('testapp')
        self.assertEqual(root.name, '/')
        self.assertEqual(root.rootname, 'testapp')
        self.assertEqual(root.is_directory, True)

class GetRootTestCase(TestCase):
    def setUp(self):
        root = create_root('testapp')
    def test_get_root(self):
        root = get_root('testapp')

class BuildUponRootTestCase(TestCase):
    def setUp(self):
        root = create_root('testapp')
    def test_create_directory_on_root(self):
        root = get_root('testapp')

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
        root = create_root('testapp')
        newdirectory = root.create_directory('new_directory')
        subdirectory = newdirectory.create_directory('subdirectory')
        lastdirectory = subdirectory.create_directory('lastdirectory')
    def test_delete_node(self):
        root = get_root('testapp') 
        newdirectory = root.inodes.get()

        self.assertEqual(root.inodes.count(), 1)
        self.assertEqual(Inode.objects.count(), 4)

        newdirectory.deletenode()

        self.assertEqual(root.inodes.count(), 0)
        self.assertEqual(Inode.objects.count(), 1)

class GetInodeTestCase(TestCase):
    def setUp(self):
        root = create_root('testapp')
        newdirectory = root.create_directory('new_directory')
        subdirectory = newdirectory.create_directory('subdirectory')
        self.lastdirectory = subdirectory.create_directory('lastdirectory')

    def test_get_inode_with_slash(self):
        root = get_root('testapp')
        i = get_inode('new_directory/subdirectory/lastdirectory/', 'testapp')
        self.assertEqual(self.lastdirectory, i)
    def test_get_node_without_slash(self):
        root = get_root('testapp')
        try:
            i = get_inode('new_directory/subdirectory/lastdirectory',
                          'testapp')
        except Inode.Redirect302 as e:
            self.assertEqual(e.newpath,
                             'new_directory/subdirectory/lastdirectory/')
    def test_nonexistent_node(self):
        root = get_root('testapp')
        try:
            i = get_inode('lkasjdfklajsfkljasklf', 'testapp')
        except Inode.Error404:
            self.assertTrue(True)

    def test_nonexistent_root(self):
        try:
            i = get_inode('alskdfj', 'does-not-exist')
        except Inode.Error500:
            self.assertTrue(True)
