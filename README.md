# Github Traffic Information

[![GitHub issues](https://img.shields.io/github/issues/miykael/traffic_info_github.svg)](https://github.com/miykael/traffic_info_github/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/miykael/traffic_info_github.svg)](https://github.com/miykael/traffic_info_github/pulls/)
[![GitHub contributors](https://img.shields.io/github/contributors/miykael/traffic_info_github.svg)](https://GitHub.com/miykael/traffic_info_github/graphs/contributors/)
[![GitHub Commits](https://github-basic-badges.herokuapp.com/commits/miykael/traffic_info_github.svg)](https://github.com/miykael/traffic_info_github/commits/master)
[![GitHub size](https://github-size-badge.herokuapp.com/miykael/traffic_info_github.svg)](https://github.com/miykael/traffic_info_github/archive/master.zip)
[![GitHub HitCount](http://hits.dwyl.io/miykael/traffic_info_github.svg)](http://hits.dwyl.io/miykael/traffic_info_github)

The script ``traffic_info_github.py`` extracts the current traffic information of a specific or all of your repos. Github only provides information about view and clone count for the last 14 days. This script tries to bypass this restrictuion by accumulating the traffic information in a local tsv file. Therefore, if you run the script at least once every 14 days you can store the full traffic information.

Once all new traffic information are collected, an overview graph for the whole tracking period will be generated for each repo:

<img src="results/traffic_info_nipype_tutorial.png">

**Note**: The script is based on [nchah's github-traffic-stats.py](https://github.com/nchah/github-traffic-stats), and I want to thank him for his work!


# How to run the script

The script expects two mandatory and one optional input:

    1. `username`: Github username (mandatory)
    2. `password`: Github password (mandatory)
    3. `reponame`: Name of repo (optional, default: ALL)

So, if you want to collect tracking information for all of your repos, use:

    python traffic_info_github.py username password

If you want to only track one specific repo use:

    python traffic_info_github.py username password reponame


# Set up weekly collection

The script is setup on TravisCI in such a way, that it's run every week. The collected data is directly pushed to this repo.

To visualize the results, you can use the `visualize_github_traffic.py` script, that is still under development.
