#!/bin/bash

out_file=$1
shift

if [ -e "$out_file" ]; then
    # get initial value
    last_value=$(sed -n '${s/ .*$//;p}' "$out_file")
    initial_value=$((last_value + 1))
else
    initial_value=3
fi

for (( i = initial_value;; ++i )); do
    ./b_and_c2.py --func c --min-m $i --max-m $i
done | tee -a "$out_file"
