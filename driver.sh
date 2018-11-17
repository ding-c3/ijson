#!/usr/bin/env bash
declare -a files=("data/ds_1000" "data/ds_1000000" "data/ds_10000000" "data/ds_50000000" "data/ds_100000000" "data/ds_500000000")
declare -a d_types=("short" "long")


## now loop through the above array
for f in "${files[@]}"
do
  for t in "${d_types[@]}"
  do
    echo "----${f}_${t}----"
     echo "ijson"
     cat "${f}_${t}.json" | python profile_action.py ijson time
     cat "${f}_${t}.json" | python profile_action.py ijson mem
     echo ""
    echo "json"
    cat "${f}_${t}.json" | python profile_action.py json time
    cat "${f}_${t}.json" | python profile_action.py json mem
    echo ""
    echo "msgpack"
    cat "${f}_${t}.msgpack" | python profile_action.py msgpack time
    cat "${f}_${t}.msgpack" | python profile_action.py msgpack mem
    echo ""
   done
# or do whatever with individual element of the array
done
