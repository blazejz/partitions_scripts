#!/bin/bash

basedir=$(dirname "$(readlink -f "$0")")
pushd "$basedir" > /dev/null

function start() {
    local script=$1
    shift

    out_file="out/$(echo "$script" | sed 's/\.init\.sh$/.txt/')"
    session_name="blazejz_$(echo "$script" | sed 's/^.*\///' | sed 's/\.init\.sh$//' | sed 's/\./_/g')"

    # start 
    echo "$script"
    screen -ls | grep "\.$session_name\s" > /dev/null
    if (( $? )); then
        nice screen -md -S "$session_name" /bin/bash "$script" "$out_file"
    fi
}

for script in ./*.init.sh; do
    if [ -x "$script" ]; then
        start "$script"
    fi
done

popd > /dev/null
