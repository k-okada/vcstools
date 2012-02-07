        self.root_directory = tempfile.mkdtemp()
        # helpful when setting tearDown to pass
        print "mock directory", self.root_directory
        self.directories = dict(setUp=self.root_directory)
        self.remote_path = os.path.join(self.root_directory, "remote")
        os.makedirs(self.remote_path)
        subprocess.check_call(["git", "init"], cwd=self.remote_path)
        subprocess.check_call(["touch", "fixed.txt"], cwd=self.remote_path)
        subprocess.check_call(["git", "add", "*"], cwd=self.remote_path)
        subprocess.check_call(["git", "commit", "-m", "initial"], cwd=self.remote_path)
        subprocess.check_call(["git", "tag", "test_tag"], cwd=self.remote_path)
        # other branch
        subprocess.check_call(["git", "branch", "test_branch"], cwd=self.remote_path)
        po = subprocess.Popen(["git", "log", "-n", "1", "--pretty=format:\"%H\""], cwd=self.remote_path, stdout=subprocess.PIPE)
        subprocess.check_call(["touch", "modified.txt"], cwd=self.remote_path)
        subprocess.check_call(["touch", "modified-fs.txt"], cwd=self.remote_path)
        subprocess.check_call(["git", "add", "*"], cwd=self.remote_path)
        subprocess.check_call(["git", "commit", "-m", "initial"], cwd=self.remote_path)
        po = subprocess.Popen(["git", "log", "-n", "1", "--pretty=format:\"%H\""], cwd=self.remote_path, stdout=subprocess.PIPE)
        subprocess.check_call(["touch", "deleted.txt"], cwd=self.remote_path)
        subprocess.check_call(["touch", "deleted-fs.txt"], cwd=self.remote_path)
        subprocess.check_call(["git", "add", "*"], cwd=self.remote_path)
        subprocess.check_call(["git", "commit", "-m", "modified"], cwd=self.remote_path)
        po = subprocess.Popen(["git", "log", "-n", "1", "--pretty=format:\"%H\""], cwd=self.remote_path, stdout=subprocess.PIPE)
        

        subprocess.check_call(["git", "tag", "last_tag"], cwd=self.remote_path)
        
    
        local_path = os.path.join(self.root_directory, "ros")
        url = self.remote_path
        client = GitClient(local_path)
        self.assertFalse(client.path_exists())
        self.assertFalse(client.detect_presence())
        self.assertTrue(client.checkout(url))
        self.assertTrue(client.path_exists())
        self.assertTrue(client.detect_presence())
        self.assertEqual(client.get_url(), self.remote_path)
        self.assertEqual(client.get_version(), self.readonly_version)
        self.assertEqual(client.get_version(self.readonly_version_init[0:6]), self.readonly_version_init)
        self.assertEqual(client.get_version("test_tag"), self.readonly_version_init)
        # private functions
        self.assertFalse(client.is_local_branch("test_branch"))
        self.assertTrue(client.is_remote_branch("test_branch"))
        self.assertTrue(client.is_tag("test_tag"))
        self.assertFalse(client.is_remote_branch("test_tag"))
        self.assertFalse(client.is_tag("test_branch"))
        client = GitClient(local_path)
        self.assertEqual(client.get_vcs_type_name(), 'git')
        local_path = os.path.join(self.root_directory, "ros")
        url = self.remote_path
        client = GitClient(local_path)
        self.assertFalse(client.path_exists())
        self.assertFalse(client.detect_presence())
        self.assertTrue(client.checkout(url))
        self.assertTrue(client.path_exists())
        self.assertTrue(client.detect_presence())
        self.assertEqual(client.get_path(), local_path)
        self.assertEqual(client.get_url(), url)
        self.assertEqual(client.get_branch(), "master")
        self.assertEqual(client.get_branch_parent(), "master")
        #self.assertEqual(client.get_version(), '-r*')

        local_path = os.path.join(self.root_directory, "ros")
        url = self.remote_path
        client = GitClient(local_path)
        self.assertFalse(client.path_exists())
        self.assertFalse(client.detect_presence())
        self.assertTrue(client.checkout(url, version))
        self.assertTrue(client.path_exists())
        self.assertTrue(client.detect_presence())
        self.assertEqual(client.get_path(), local_path)
        self.assertEqual(client.get_url(), url)
        self.assertEqual(client.get_version(), version)
        self.assertTrue(client.update(new_version))
        self.assertEqual(client.get_version(), new_version)


    def test_checkout_master_branch_and_update(self):
        from vcstools.git import GitClient
        subdir = "checkout_specific_version_test"
        local_path = os.path.join(self.root_directory, "ros")
        url = self.remote_path
        branch = "master"
        client = GitClient(local_path)
        self.assertFalse(client.path_exists())
        self.assertFalse(client.detect_presence())
        self.assertTrue(client.checkout(url, branch))
        self.assertTrue(client.path_exists())
        self.assertTrue(client.detect_presence())
        self.assertEqual(client.get_path(), local_path)
        self.assertEqual(client.get_url(), url)
        self.assertEqual(client.get_branch_parent(), branch)
        self.assertTrue(client.update(branch))
        self.assertEqual(client.get_branch_parent(), branch)

        local_path = os.path.join(self.root_directory, "ros")
        url = self.remote_path
        branch = "test_branch"
        client = GitClient(local_path)
        self.assertFalse(client.path_exists())
        self.assertFalse(client.detect_presence())
        self.assertTrue(client.checkout(url, branch))
        self.assertTrue(client.path_exists())
        self.assertTrue(client.detect_presence())
        self.assertTrue(client.is_local_branch(branch))
        self.assertEqual(client.get_path(), local_path)
        self.assertEqual(client.get_url(), url)
        self.assertEqual(client.get_version(), self.readonly_version_init)
        self.assertEqual(client.get_branch(), branch)
        self.assertEqual(client.get_branch_parent(), branch)

        self.assertTrue(client.update())# no arg
        self.assertEqual(client.get_branch(), branch)
        self.assertEqual(client.get_version(), self.readonly_version_init)
        self.assertEqual(client.get_branch_parent(), branch)

        self.assertTrue(client.update(branch))# same branch arg
        self.assertEqual(client.get_branch(), branch)
        self.assertEqual(client.get_version(), self.readonly_version_init)
        self.assertEqual(client.get_branch_parent(), branch)
        self.assertTrue(client.update(new_branch))
        self.assertEqual(client.get_branch(), new_branch)
        self.assertEqual(client.get_branch_parent(), new_branch)


    def test_checkout_specific_tag_and_update(self):
        from vcstools.git import GitClient
        local_path = os.path.join(self.root_directory, "ros")
        url = self.remote_path
        tag = "last_tag"
        client = GitClient(local_path)
        self.assertFalse(client.path_exists())
        self.assertFalse(client.detect_presence())
        self.assertTrue(client.checkout(url, tag))
        self.assertTrue(client.path_exists())
        self.assertTrue(client.detect_presence())
        self.assertEqual(client.get_path(), local_path)
        self.assertEqual(client.get_url(), url)
        self.assertEqual(client.get_branch_parent(), None)
        tag = "test_tag"
        self.assertTrue(client.update(tag))
        self.assertEqual(client.get_branch_parent(), None)
        new_branch = 'master'
        self.assertTrue(client.update(new_branch))
        self.assertEqual(client.get_branch_parent(), new_branch)
        tag = "test_tag"
        self.assertTrue(client.update(tag))

    def test_fast_forward(self):
        from vcstools.git import GitClient
        local_path = os.path.join(self.root_directory, "ros")
        url = self.remote_path
        client = GitClient(local_path)
        self.assertTrue(client.checkout(url, "master"))
        subprocess.check_call(["git", "reset", "--hard", "test_tag"], cwd=local_path)
        self.assertTrue(client.update())

class GitClientDanglingCommitsTest(GitClientTestSetups):

    def setUp(self):
        GitClientTestSetups.setUp(self)
        self.local_path = os.path.join(self.root_directory, "ros")
        from vcstools.git import GitClient
        client = GitClient(self.local_path)
        self.assertTrue(client.checkout(self.remote_path))
        # Create some local untracking branch
        subprocess.check_call(["git", "checkout", "test_tag", "-b", "localbranch"], cwd=self.local_path)
        subprocess.check_call(["touch", "local.txt"], cwd=self.local_path)
        subprocess.check_call(["git", "add", "*"], cwd=self.local_path)
        subprocess.check_call(["git", "commit", "-m", "my_branch"], cwd=self.local_path)
        subprocess.check_call(["git", "tag", "my_branch_tag"], cwd=self.local_path)
        po = subprocess.Popen(["git", "log", "-n", "1", "--pretty=format:\"%H\""], cwd=self.local_path, stdout=subprocess.PIPE)
        self.untracked_version = po.stdout.read().rstrip('"').lstrip('"')
        
        # Go detached to create some dangling commits
        subprocess.check_call(["git", "checkout", "test_tag"], cwd=self.local_path)
        # create a commit only referenced by tag
        subprocess.check_call(["touch", "tagged.txt"], cwd=self.local_path)
        subprocess.check_call(["git", "add", "*"], cwd=self.local_path)
        subprocess.check_call(["git", "commit", "-m", "no_branch"], cwd=self.local_path)
        subprocess.check_call(["git", "tag", "no_br_tag"], cwd=self.local_path)
        # create a dangling commit
        subprocess.check_call(["touch", "dangling.txt"], cwd=self.local_path)
        subprocess.check_call(["git", "add", "*"], cwd=self.local_path)
        subprocess.check_call(["git", "commit", "-m", "dangling"], cwd=self.local_path)

        po = subprocess.Popen(["git", "log", "-n", "1", "--pretty=format:\"%H\""], cwd=self.local_path, stdout=subprocess.PIPE)
        self.dangling_version = po.stdout.read().rstrip('"').lstrip('"')

        # go back to master to make head point somewhere else
        subprocess.check_call(["git", "checkout", "master"], cwd=self.local_path)

        
    def test_protect_dangling(self):
        from vcstools.git import GitClient
        client = GitClient(self.local_path)
        url = self.remote_path
        self.assertEqual(client.get_branch(), "master")
        tag = "no_br_tag"
        self.assertTrue(client.update(tag))
        self.assertEqual(client.get_branch(), None)
        self.assertEqual(client.get_branch_parent(), None)

        tag = "test_tag"
        self.assertTrue(client.update(tag))
        self.assertEqual(client.get_branch(), None)
        self.assertEqual(client.get_branch_parent(), None)

        # to dangling commit
        sha = self.dangling_version
        self.assertTrue(client.update(sha))
        self.assertEqual(client.get_branch(), None)
        self.assertEqual(client.get_version(), self.dangling_version)
        self.assertEqual(client.get_branch_parent(), None)

        # now HEAD protects the dangling commit, should not be allowed to move off.
        new_branch = 'master'
        self.assertFalse(client.update(new_branch))

    def test_detached_to_branch(self):
        from vcstools.git import GitClient
        client = GitClient(self.local_path)
        url = self.remote_path
        self.assertEqual(client.get_branch(), "master")
        tag = "no_br_tag"
        self.assertTrue(client.update(tag))
        self.assertEqual(client.get_branch(), None)
        self.assertEqual(client.get_branch_parent(), None)
        
        tag = "test_tag"
        self.assertTrue(client.update(tag))
        self.assertEqual(client.get_branch(), None)
        self.assertEqual(client.get_version(), self.readonly_version_init)
        self.assertEqual(client.get_branch_parent(), None)

        #update should not change anything
        self.assertTrue(client.update()) #no arg
        self.assertEqual(client.get_branch(), None)
        self.assertEqual(client.get_version(), self.readonly_version_init)
        self.assertEqual(client.get_branch_parent(), None)
        new_branch = 'master'
        self.assertTrue(client.update(new_branch))
        self.assertEqual(client.get_branch(), new_branch)
        self.assertEqual(client.get_version(), self.readonly_version)
        self.assertEqual(client.get_branch_parent(), new_branch)

        
    def test_checkout_untracked_branch_and_update(self):
        # difference to tracked branches is that branch parent is None, and we may hop outside lineage
        from vcstools.git import GitClient
        client = GitClient(self.local_path)
        url = self.remote_path
        branch = "localbranch"
        self.assertEqual(client.get_branch(), "master")
        self.assertTrue(client.path_exists())
        self.assertTrue(client.detect_presence())
        self.assertTrue(client.is_local_branch(branch))
        self.assertEqual(client.get_path(), self.local_path)
        self.assertEqual(client.get_url(), url)
        self.assertTrue(client.update(branch))
        self.assertEqual(client.get_version(), self.untracked_version)
        self.assertEqual(client.get_branch(), branch)
        self.assertEqual(client.get_branch_parent(), None)

        self.assertTrue(client.update())# no arg
        self.assertEqual(client.get_branch(), branch)
        self.assertEqual(client.get_version(), self.untracked_version)
        self.assertEqual(client.get_branch_parent(), None)

        self.assertTrue(client.update(branch))# same branch arg
        self.assertEqual(client.get_branch(), branch)
        self.assertEqual(client.get_version(), self.untracked_version)
        self.assertEqual(client.get_branch_parent(), None)

        # to master
        new_branch = 'master'
        self.assertTrue(client.update(new_branch))
        self.assertEqual(client.get_branch(), new_branch)
        self.assertEqual(client.get_version(), self.readonly_version)
        self.assertEqual(client.get_branch_parent(), new_branch)

        # and back
        self.assertTrue(client.update(branch))# same branch arg
        self.assertEqual(client.get_branch(), branch)
        self.assertEqual(client.get_version(), self.untracked_version)
        self.assertEqual(client.get_branch_parent(), None)

        # to dangling commit
        sha = self.dangling_version
        self.assertTrue(client.update(sha))
        self.assertEqual(client.get_branch(), None)
        self.assertEqual(client.get_version(), self.dangling_version)
        self.assertEqual(client.get_branch_parent(), None)

        #should not work to protect commits from becoming dangled
        # to commit outside lineage
        tag = "test_tag"
        self.assertFalse(client.update(tag))



        self.readonly_path = os.path.join(self.root_directory, "readonly")
        from vcstools.git import GitClient
        client = GitClient(self.readonly_path)
        self.assertTrue(client.checkout(self.remote_path, self.readonly_version))


