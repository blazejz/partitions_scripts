#!/bin/bash

for i in $(screen -ls | grep blazejz_ | cut -d '	' -f 2); do screen -S $i -X quit; done
