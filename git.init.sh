#!/bin/bash


while true ; do
    pushd out
    git add .
    git commit -m update
    git push
    popd
    sleep 5m
done
