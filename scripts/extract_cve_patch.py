#!/usr/bin/env python

import sh
import os
import multiprocessing
import argparse


def print_help():
    print("This script is used to extract CVE related commits")
    print("OPTIONS:")
    print("  -r/--repo <value> Specify the directory of the target repository")
    print("  -t/--target <value> Specify the location to write the target file")
    print("$ python extract_cve_patch.py -r ./linux -t ./vuln")


def parse_repo(soure, target):
    try:
        target_git = sh.git.bake("--no-pager", _cwd=source)
        cve_related = target_git.log("--grep='CVE'", "--format='%h'")
        cve_commit_list = str(cve_related.stdout)[2:-3].split('\\n')
        # remove str(b'')
        only_modified = target_git.diff("--diff-filter=M","--name-only", )
    
    except Exception:
        print(Exception)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="scripts to extract CVE related commits")
    parser.add_argument('-r', '--repo', help="repository's location")
    parser.add_argument('-t', '--target', help="where to store the target file")

    args = parser.parse_args()

    if os.path.isdir(args.repo):
        print("[-] Repo is Not a valid Dir")
        print_help()
        exit(-1)

    parse_repo(args.repo, args.target)
