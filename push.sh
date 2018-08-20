#!/usr/bin/env bash

setup_git() {
    git config --global user.email "travis@travis-ci.org"
    git config --global user.name "Travis CI"
}

commit_new_results() {
    git checkout ${TRAVIS_BRANCH}
    git add results/
    git commit -m "Travis results ${TRAVIS_BUILD_NUMBER} [skip ci]"
}

upload_files() {
    git remote add travis https://${TOKEN}@github.com/miykael/traffic_info_github.git > /dev/null 2>&1
    git push --quiet --set-upstream travis ${TRAVIS_BRANCH} > /dev/null 2>&1
}

setup_git
commit_new_results
upload_files
