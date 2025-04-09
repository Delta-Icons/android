#!/usr/bin/env bash

wd="$(dirname -- "${BASH_SOURCE[0]}";)"
wd="$(realpath -e -- "$wd/../..";)"

cd $wd

latest_tag=$(git tag --sort version:refname | grep -v 'beta' | tail -n 1)

if [[ $latest_tag ]]; then
    echo "Latest tag is $latest_tag; optimizing images since this tag"
    optipng $(git diff --name-only $latest_tag -- "***.png") || true
else
    echo 'No release found, skip optimizing'
fi