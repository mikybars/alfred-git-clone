#!/usr/bin/python
# encoding: utf-8

import os, sys
import git

from pprint import pformat
from workflow import Workflow3


log = None


def clipboard_items():
    return [os.getenv(clip(x))
            for x in range(0, 100)
            if clip(x) in os.environ]

def clip(x):
    return 'clip' + str(x)

def make_wf_item(repo_url):
    repo = git.get_repo_name_from_url(repo_url)
    return {'title': repo,
            'subtitle': repo_url,
            'autocomplete': repo,
            'icon': git.get_icon_from_url(repo_url),
            'valid': True}

def main(wf):
    wf_items = [make_wf_item(clip_item)
               for clip_item in clipboard_items()
               if git.is_a_valid_git_url(clip_item)]

    log.debug('Git repos from clipboard:\n' + pformat(wf_items))

    for item in wf_items:
        wf_item = wf.add_item(**item)
        wf_item.setvar('repo_name', item['title'])
        wf_item.setvar('repo_url', item['subtitle'])

    wf.warn_empty('No git repos found in the clipboard')
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
