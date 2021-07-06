import os
import multiprocessing
import numpy as np
import pandas as pd


def extract_function(input_path):
    dirs = os.listdir(input_path)
    pool = multiprocessing.Pool()
    pool.map(parse_commit,dirs)
    pass

def extract_features(adds,decs):
    pass

def parse_commit(commit_path):
    with open(os.path.join(commit_path, 'patch'), 'r') as pf:
        cnt = pf.read()
        # diff_str = 'diff --git a(/[a-zA-Z0-9_]+)+\.c b(/[a-zA-Z0-9_]+)+\.c'
        # diff_pattern = re.compile(diff_str)

        diff_str = 'diff --git'
        separator = [cnt.index(diff_str)]
        # separator is where "diff --git xxxxx xxxx" separate each file log

        sep = 0
        flag = True
        while flag:
            if cnt.index(diff_str, sep) != cnt.rindex(diff_str):
                sep = cnt.index(diff_str, sep + 1)
                separator.append(sep)
            else:
                if cnt.rindex(diff_str) in separator:
                    flag = False
                else:
                    separator.append(cnt.rindex(diff_str))

        last = separator.pop()
        commit_size = len(cnt)

        diff = cnt[last:commit_size]
        lines = diff.rstrip().split('\n')
        adds = []
        decs = []

        # The first four lines look like:
        # 
        # diff --git a/fs/stat.c b/fs/stat.c
        # index 29c5fe4f8b6..d712a0dfb50f 100644
        # --- a/fs/stat.c
        # +++ b/fs/stat.c
        # 
        # we just start from the fifth line
        for line in lines[4:]:
            if line[0]=='+':
                adds.append(line[1:])
            elif line[0]=='-':
                decs.append(line[1:])

        vec = extract_features(adds,decs)