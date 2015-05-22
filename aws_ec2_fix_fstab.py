#!/usr/bin/python
#https://github.com/akabdog 2015-05-19
#
#this script will mount the volume from a broken instance and fix fstab by removing all entries except the entry for "/", identified by variable FSTAB_GREP_STATEMENT 
#the broken instances must be stopped and the WORKSPACE instance is just any instance which is running and supports SSH and mounting
import boto.ec2
import os
import distutils.util
import time
import sys

#these variables will need to be updated whenever you use this script:
BROKEN_INSTANCE_ROOT_VOLUME_ID = "vol-fd08xxx"
BROKEN_INSTANCE_ID = "i-39dcxxx" 
BROKEN_INSTANCE_ROOT_DEVICE = "/dev/sda1"

#make sure this workspaces is in the same zone and aws account as the broken instance
FSTAB_GREP_STATEMENT = "rootfs"
WORKSPACE_INSTANCE = "i-1271xxxx"
WORKSPACE_MOUNTPOINT = "/fstab_fix"
WORKSPACE_DEVICE = "/dev/sdx"
WORKSPACE_DEVICE_LOCAL = "/dev/xvdx"
WORKSPACE_SSH_NAME = "dev-workspace-instance-1"

#this function will be used to later to get user input
def user_yes_no_query(question):
	sys.stdout.write('%s [y/n]\n' % question)
	while True:
		try:
			return distutils.util.strtobool(raw_input().lower())
		except ValueError:
			sys.stdout.write('Please respond with \'y\' or \'n\'.\n')

def fix ( str ):
	print "connecting to ec2 via profile %s" % (str)
	conn = boto.ec2.connect_to_region("us-west-1", profile_name = str)
#detach volume from broken instance
	print "detaching volume from original instance..."
	conn.detach_volume(BROKEN_INSTANCE_ROOT_VOLUME_ID)	
	time.sleep(10)	
#attach volume to temporary workspace instance
	print "attaching volume to workspace instance..."
	conn.attach_volume (BROKEN_INSTANCE_ROOT_VOLUME_ID, WORKSPACE_INSTANCE, WORKSPACE_DEVICE) 
	time.sleep(10)	
#make sure directory exists on workspace 
	print "creating directory for mounting..."
	command = "ssh %s \"mkdir -p %s \" " % (WORKSPACE_SSH_NAME, WORKSPACE_MOUNTPOINT)
	os.system(command)
#mount device on workspace instance
	print "mounting volume on workspace instance..."
	command = "ssh %s \"sudo mount %s %s \" " % (WORKSPACE_SSH_NAME, WORKSPACE_DEVICE_LOCAL, WORKSPACE_MOUNTPOINT)
	os.system(command)
#print out original fstab
	print "#####fstab before changes:#####"
	command = "ssh %s \"cat %s/etc/fstab \" " % (WORKSPACE_SSH_NAME, WORKSPACE_MOUNTPOINT)
	os.system(command)
	print "##############################"
#backup original fstab
	print "creating backup at fstab.DATE.bak..."	
	command = "ssh %s \"sudo cp %s/etc/fstab %s/etc/fstab.`date -I`.bak \" " % (WORKSPACE_SSH_NAME, WORKSPACE_MOUNTPOINT, WORKSPACE_MOUNTPOINT)
	os.system(command)
#remove all lines from fstab except the root device (usually it will have "LABEL=cloudimg-rootfs" or something similar)
	print "modifying fstab to only include root mount..."
	command = "ssh %s \"grep %s %s/etc/fstab > /tmp/fstab; sudo cp /tmp/fstab %s/etc/fstab \"" % (WORKSPACE_SSH_NAME, FSTAB_GREP_STATEMENT, WORKSPACE_MOUNTPOINT, WORKSPACE_MOUNTPOINT)
	os.system(command)
#print out new fstab and check if it looks good 
	print "#####here is the new fstab:#####"
	command = "ssh %s \"cat %s/etc/fstab\"" % (WORKSPACE_SSH_NAME, WORKSPACE_MOUNTPOINT)
	os.system(command)
	print "##############################"
	if user_yes_no_query('Does this fstab look good?'):	
#detach volume from workstapce
		print "thanks, continuing with the new fstab..."
	else:
#revert changes
		print "restoring fstab from backup, detaching from workspace and attaching to original..."
		command = "ssh %s \"sudo cp %s/etc/fstab.`date -I`.bak %s/etc/fstab \" " % (WORKSPACE_SSH_NAME, WORKSPACE_MOUNTPOINT, WORKSPACE_MOUNTPOINT)
		print "hint: if the fstab was blank, you may want to check out the variable FSTAB_GREP_STATEMENT in the script"
#umount and detach volume
	print "detaching volume from workspace instance ..."
	command = "ssh %s \"sudo umount %s\"" % (WORKSPACE_SSH_NAME, WORKSPACE_MOUNTPOINT)
	os.system(command)
	conn.detach_volume(BROKEN_INSTANCE_ROOT_VOLUME_ID)
	time.sleep(10)	
#attach volume back to original instance
	print "attaching volume back to original instance %s . Start the instance manually to test your new fstab..." % (BROKEN_INSTANCE_ID)
	conn.attach_volume (BROKEN_INSTANCE_ROOT_VOLUME_ID, BROKEN_INSTANCE_ID, BROKEN_INSTANCE_ROOT_DEVICE) 
	time.sleep(10)	
# 
# MAIN
#
fix("aws-dev")
