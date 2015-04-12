#!/bin/bash

vmName=$1
xenServer=sjc-xen-p1
tempPort=5900

#first lets login and find out what port its running on
vmID=$(ssh $xenServer "xe vm-list params=dom-id,resident-on name-label=$vmName | grep dom-id | sed -r 's/^.{23}//' ") 
vncPort=$(ssh $xenServer "xenstore-read /local/domain/$vmID/console/vnc-port")

#then we setup local port forwarding and connect to local VNC port
ssh -L $tempPort:localhost:$vncPort -N -f sjc-xen-p1
ssvncviewer 127.0.0.1:$tempPort
kill `pgrep -f '$tempPort'`
