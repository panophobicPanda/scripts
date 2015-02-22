#!/bin/bash
#
# bsmith@the408.com 2014-01-14
#
#
#This script takes two arguements, the source folder of all the updates and the xenserver you want to patch
#e.g. xen_updater.sh ~/Downloads/xen_updates 172.20.10.74

if [ $# -eq 2 ]; then

source_directory=$1
destination_directory=/var/tmp/`date -I`
destination_host=$2

#first we unzip the files
for i in `ls $source_directory/*.zip`; do unzip -n -d $source_directory $i; done

#then we copy the files to the xenserver
echo "Files will be copied to $destination_host in the directory $destination_directory"
ssh root@$destination_host "mkdir -p $destination_directory"
scp $source_directory/*.xsupdate root@$destination_host:$destination_directory/

#time to apply the patches
patches=$(ssh root@$destination_host "ls $destination_directory/*.xsupdate")
echo "patches to be applied:"
echo "$patches"

for i in $patches; do
	uuid=$(ssh root@${destination_host} "/opt/xensource/bin/xe patch-upload file-name=${i} 2>&1 | grep uuid")
	uuid_fixed=$(echo $uuid | awk '{print $2}')
	echo "installing: $i uuid:$uuid_fixed"
	ssh root@$destination_host "/opt/xensource/bin/xe patch-pool-apply uuid=${uuid_fixed} 2>&1"
	done

else
	echo "This script takes two arguements, the source folder of all the updates and the xenserver you want to patch \n e.g. xen_updater.sh ~/Downloads/xen_updates 172.20.10.74"
fi
