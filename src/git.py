import os, re, subprocess

GIT_REPO_URL_PATTERN = '^((https|ssh)://|git@).*/(?P<repo>.*)\.git'
ICONS_PATH = 'icons'

def is_a_valid_git_url(url):
    return re.match(GIT_REPO_URL_PATTERN, url)

def get_repo_name_from_url(url):
    return re.search(GIT_REPO_URL_PATTERN, url).group('repo')

def dir_is_a_git_repo(path):
    with open(os.devnull, 'w') as devnull:
        git_cmd = "git rev-parse --is-inside-work-tree"
        p = subprocess.Popen(git_cmd.split(), cwd=os.path.expanduser(path),
                             stdout=devnull, stderr=devnull)
        p.wait()
        return p.returncode == 0

def get_remote_url(path):
    with open(os.devnull, 'w') as devnull:
        git_cmd = "git config --get remote.origin.url"
        p = subprocess.Popen(git_cmd.split(), cwd=os.path.expanduser(path),
                             stdout=subprocess.PIPE, stderr=devnull)
        stdout, stderr = p.communicate()
        return stdout

def icon(name):
    return os.path.join(ICONS_PATH, name + '.png')

def get_icon_from_url(url):
    if 'github.com' in url:
        return icon('github')
    elif 'bitbucket' in url:
        return icon('bitbucket')
    elif 'gitlab' in url:
        return icon('gitlab')
    else:
        return icon('repo')
