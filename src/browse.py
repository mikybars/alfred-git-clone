#!/usr/bin/python
# encoding: utf-8

import os, sys
from base64 import b64encode
import git, history

from workflow import Workflow3, ICON_WARNING, ICON_ERROR, ICON_CLOCK


log = None

def isdir(d):
    return os.path.isdir(os.path.expanduser(d))

def by_repo_name(item):
    return item['title']

def join_dirs(dir1, dir2):
    joint_path = os.path.join(dir1, dir2)
    return os.path.join(joint_path, '')  #  append the trailing slash if necessary

def hidden(dir):
    return dir.startswith('.')

def make_wf_item(parent_dir, subdir):
    full_path = join_dirs(parent_dir, subdir)

    item = { 'title': subdir,
             'autocomplete': full_path,
             'icon': 'public.folder',
             'icontype': 'filetype' }

    if git.dir_is_a_git_repo(full_path):
        remote_url = git.get_remote_url(full_path)
        item['subtitle'] = remote_url
        item['icon'] = git.get_icon_from_url(remote_url)
        item['icontype'] = None

    return item

def listdir(dir):
    canonical_path = os.path.expanduser(dir)  # handle ~
    root, subdirs, files = next(os.walk(canonical_path))
    return [make_wf_item(dir, subdir)
            for subdir in sorted(subdirs, key=lambda s: s.lower())
            if not hidden(subdir)]

def listdir_cached(wf, dir):
    canonical_path = os.path.expanduser(dir)  # handle ~
    cache_key = b64encode(canonical_path)
    return wf.cached_data(cache_key, lambda: listdir(dir), max_age=30)

def split_path_and_submatch(input):
    separator = input.rindex('/')
    return input[:separator], input[separator+1:]

def check_workspace_dir(wf):
    if os.getenv('workspace_undefined', default='0') == '1':
        wf.add_item(title='Workspace not defined', 
                    subtitle="Set the 'workspace_dir' in the workflow configuration sheet",
                    icon=ICON_WARNING)
    elif os.getenv('workspace_doesnt_exist', default='0') == '1':
        wf.add_item(title='Workspace not valid',
                    subtitle="Path '{}' does not exist or is not a directory".format(os.getenv('workspace_dir')),
                    icon=ICON_ERROR)

def add_result(wf, target_dir, title, icon=None, subtitle='', autocomplete=None, icontype=None):
    item = wf.add_item(title=title, subtitle=subtitle, autocomplete=autocomplete, icon=icon, icontype=icontype, valid=True)
    item.setvar('target_dir', target_dir)
    item.setvar('clone_path', os.path.join(os.path.expanduser(target_dir), os.getenv('repo_name')))

def check_history(wf):
    max_recent_items = int(os.getenv('max_recent_items', 2))
    for recent_dir in history.get_top_ranked(wf, max_recent_items):
        add_result(wf, recent_dir, title=recent_dir, icon=ICON_CLOCK)

def first_run_checks(wf):
    if 'rerun' not in os.environ:
        check_workspace_dir(wf)
        check_history(wf)
    wf.setvar('rerun', 'true')

def main(wf):
    first_run_checks(wf)

    query = wf.args[0]
    wf_items = []
    if isdir(query):
        add_result(wf, target_dir=query, title='Clone here', icon=None, subtitle=query)
        wf_items = listdir_cached(wf, query)
    elif '/' in query:
        path, submatch = split_path_and_submatch(query)
        wf_items = listdir_cached(wf, path)
        wf_items = wf.filter(submatch, wf_items, by_repo_name)

    for item in wf_items:
        add_result(wf, target_dir=item['autocomplete'], **item)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
