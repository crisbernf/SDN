#!/bin/bash

ovs-vsctl set port sw5-eth24 trunks=8,10,11,12,13,14,15,55
ovs-vsctl set port sw5-eth23 trunks=8,10,11,12,13,14,15,55

