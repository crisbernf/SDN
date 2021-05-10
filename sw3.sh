#!/bin/bash

ovs-vsctl set port sw3-eth21 trunks=8,10,11,12,13,14,15,55
ovs-vsctl set port sw3-eth22 trunks=8,10,11,12,13,14,15,55
ovs-vsctl set port sw3-eth23 trunks=8,10,11,12,13,14,15,55
ovs-vsctl set port sw3-eth24 trunks=8,10,11,12,13,14,15,55

