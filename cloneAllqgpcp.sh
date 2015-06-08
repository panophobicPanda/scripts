#!/bin/bash
# this machine will clone and migrate all VMs from the answer file vmNames.txt
# https://github.com/akabdog 2012
#
API_User=bsmith
API_Password=
URL=https://10.60.1.220/sdk/vimService
answerFile=./vmNames.txt
#
#
/usr/lib/vmware-vcli/apps/general/vidiscovery_modified.pl  --username $API_User --password $API_Password --url $URL --managedentity host --entityname qscapvm7.ops.example.com > ./vmNames.txt

for VMNAME in `cat $answerFile`
do
#
/usr/lib/vmware-vcli/apps/vm/vmclone.pl --username $API_User --password $API_Password --url $URL --vmhost qscapvm7.ops.example.com --vmname $VMNAME --vmname_destination "$VMNAME-" --datastore qscapvm7:datastore1
#
/usr/lib/vmware-vcli/apps/vm/vmmigrate.pl --username $API_User --password $API_Password --url $URL --sourcehost qscapvm7.ops.example.com --targetdatastore qscapvm8:datastore1 --targethost qscapvm8.ops.example.com --targetpool qgpcp-v1.0-copy1 --vmname "$VMNAME-"

done
exit
