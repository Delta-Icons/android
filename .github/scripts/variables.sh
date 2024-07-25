#!/usr/bin/env bash

# for quick access to appfilter/drawables xmls via
# variables with cli utilities like diff, cp, etc.
# just source or eval the output to your interpreter

# source variables.sh
# eval $(bash variables.sh)


wd="$(dirname -- "${BASH_SOURCE[0]}";)"
wd="$(realpath -e -- "$wd/../..";)"

sd=$wd/.github/scripts
id=$wd/app/src/main/res/drawable-nodpi
vd=$wd/resources/vectors
rq=$wd/contribs/requests.yml
a1=$wd/app/src/main/assets/appfilter.xml
a2=$wd/app/src/main/res/xml/appfilter.xml
d1=$wd/app/src/main/assets/drawable.xml
d2=$wd/app/src/main/res/xml/drawable.xml


cat << EOF
wd=$wd
sd=$sd
id=$id
vd=$vd
rq=$rq
a1=$a1
a2=$a2
d1=$d1
d2=$d2
EOF
