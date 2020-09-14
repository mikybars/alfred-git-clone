HISTORY_HITS_THRESHOLD = 2

from collections import defaultdict
from pprint import pformat
from workflow import Workflow
import os, sys

def get_top_ranked(wf, max_results):
    log = wf.logger
    history = wf.stored_data('history')
    if history == None:
        return []
    rank_by_use = [dir for dir in sorted(history, key=history.get, reverse=True) 
                   if history[dir] >= HISTORY_HITS_THRESHOLD]

    log.debug("Rank by use:\n" + pformat({dir:history[dir] for dir in rank_by_use[:10]}))

    return rank_by_use[:max_results]

def increment(wf, dir):
    log = wf.logger
    history = wf.stored_data('history')
    if history == None:
        history = defaultdict(int)

    history[dir] += 1
    wf.store_data('history', history)

    log.debug("New usage of '{}' ({})".format(dir, history[dir]))

def update(wf):
    target_dir = os.getenv('target_dir')
    increment(wf, target_dir)


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(update))
