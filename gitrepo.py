from pygit2 import Repository, clone_repository

# pulls repo from url and stores clone
def set_repo():
    try:
        repo = Repository('/home/aj/Workspace/Master-Slave-Code-Complexity/radon')
    except:
        repo_url = 'https://github.com/jakubroztocil/httpie.git'
        repo_path = '/home/aj/Workspace/Master-Slave-Code-Complexity/radon'
        repo = clone_repository(repo_url, repo_path)
    return repo

# walk through commits in the given repo and store in list
def get_commits(repo):
    commits = []
    for commit in repo.walk(repo.head.target):
        commits.append(repo.get(commit.id))
    return commits