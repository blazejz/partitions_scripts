#!/bin/bash

out_file=$1
shift

if [ -e "$out_file" ]; then
    # clean non-complete results
    sed -i '/:\s*$/d' "$out_file"

    # get initial value
    last_value=$(sed -n '${s/:.*$//;p}' "$out_file")
    initial_value=$((last_value + 1))
else
    initial_value=3
fi

for (( i = initial_value;; ++i )); do
    echo -n "$i: "
    ./syf2.py --mod $i --levels 9 --arity 3
done | tee -a "$out_file"
