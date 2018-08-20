#!/usr/bin/env python

# This code is adapted from: https://github.com/nchah/github-traffic-stats
# If run daily (or at least every 14 days), this code will create a backup
# of your github traffic, storing information about git clones and visitors
# in a local TSV file. The creation of an overview visualization is optional
# and can be done with 'visualize_github_traffic.py'.

import os.path as op
from os import makedirs
import time
import argparse
import requests
import numpy as np


def send_request(resource, auth, repo=None):
    """Send request to Github API"""

    if resource == 'traffic':
        # GET /repos/:owner/:repo/traffic/views
        base_url = 'https://api.github.com/repos/'
        base_url += auth[0] + '/' + repo + '/traffic/views'
        response = requests.get(base_url, auth=auth)
        return response.json()

    elif resource == 'clones':
        # GET /repos/:owner/:repo/traffic/views/clones
        base_url = 'https://api.github.com/repos/'
        base_url += auth[0] + '/' + repo + '/traffic/clones'
        response = requests.get(base_url, auth=auth)
        return response.json()

    elif resource == 'repos':
        # GET /user/repos
        base_url = 'https://api.github.com/users/'
        base_url += auth[0] + '/repos'
        response = requests.get(base_url, auth=auth)
        print(response.json())
        repo_names = [r['full_name'] for r in response.json()]

        # GET /user/starred (contains some missing repos)
        base_url = 'https://api.github.com/users/'
        base_url += auth[0] + '/starred'
        response = requests.get(base_url, auth=auth)
        repo_names += [r['full_name'] for r in response.json()]

        # Keep only personal repos
        unique_repos = np.unique(repo_names)
        repos = [r.split('/')[1] for r in unique_repos if auth[0] in r]

        return repos


def get_information(auth_pair, repo):
    """Aggregates traffic, clones, referrers and paths information of a repo"""

    information = []

    information.append(send_request('traffic', auth_pair, repo))
    information.append(send_request('clones', auth_pair, repo))

    return information


def store_results(information, repo):
    """Store traffic and clone stats in one csv file per repo"""

    # Extract traffic information
    traffic = information[0]['views']
    tInfo = []
    for t in traffic:
        tInfo.append([t['timestamp'][:10], t['count'], t['uniques']])
    tInfo = np.asarray(tInfo)

    # Extract clone information
    clones = information[1]['clones']
    cInfo = []
    for c in clones:
        cInfo.append([c['timestamp'][:10], c['count'], c['uniques']])
    cInfo = np.asarray(cInfo)

    # Create null content if no content available
    if tInfo.size == 0:
        tInfo = np.array([[u'%s' % time.strftime("%Y-%m-%d"), u'0', u'0']])
    if cInfo.size == 0:
        cInfo = np.array([[u'%s' % time.strftime("%Y-%m-%d"), u'0', u'0']])

    # Merge traffic and clone information
    timestamps = np.unique(np.hstack((tInfo[:, 0], cInfo[:, 0])))

    # Create result folder
    filepath = op.realpath(__file__)
    path = op.dirname(filepath)

    if not op.exists(op.join(path, 'results')):
        makedirs(op.join(path, 'results'))

    # Create file if not exist
    outputfile = op.join(path, 'results', 'traffic_info_%s.tsv' % repo)

    if not op.exists(outputfile):
        header = 'Date\tView_count\tView_unique\tClone_count\tClone_unique\n'
        with open(outputfile, 'w') as f:
            f.write(header)

    # Find first overlap and start writing new content
    with open(outputfile, 'r+') as f:

        content = f.read()
        if timestamps[0] in content:
            overlapID = content.index(timestamps[0])
            f.seek(overlapID)
            f.truncate()

        for ts in timestamps:
            if ts in tInfo[:, 0]:
                tCounts = [[e[1], e[2]] for e in tInfo if e[0] == ts][0]
            else:
                tCounts = ['0', '0']

            if ts in cInfo[:, 0]:
                cCounts = [[e[1], e[2]] for e in cInfo if e[0] == ts][0]
            else:
                cCounts = ['0', '0']

            newline = '%s\t%s\t%s\n' % (ts,
                                        '\t'.join(tCounts),
                                        '\t'.join(cCounts))
            f.write(newline)


def main(username, pw, repo='ALL'):
    """Executes the script either for ALL or a specified repo"""

    auth_pair = (username, pw)

    if repo == 'ALL':
        # Get list of all repos
        repos = send_request('repos', auth_pair)

        # Get information of each repo
        print(repos)
        for repo_name in repos:
            info = get_information(auth_pair, repo_name)
            store_results(info, repo_name)
    else:

        # Get information of rep
        info = get_information(auth_pair, repo)
        store_results(info, repo)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('username', help='Github username')
    parser.add_argument('pw', help='User\'s Github password')
    parser.add_argument('repo', help='User\'s Github repo',
                        default='ALL', nargs='?')
    args = parser.parse_args()

    # Run main program
    main(args.username, args.pw, args.repo)
