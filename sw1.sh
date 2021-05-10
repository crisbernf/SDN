#!/bin/bash

ovs-vsctl set port sw1-eth24 trunks=8,10,11,12,13,14,15,55
#4 ports to tag
for i in {1..5} do ovs-vsctl set port $i sw1-eth$d tag=11
