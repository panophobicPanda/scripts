#!/usr/bin/python
# https://github.com/akabdog  2015-05-13

import boto.ec2
import boto.opsworks
import time
import re

DRY_RUN = True 
PROFILE = "prod"

print "#########################################################"
print "REMINDER, disable auto-healing on the Opsworks layer to allow instance shutdowns."
print "#########################################################"

def dry_run_notify (DRY_RUN):
	if DRY_RUN == True: print "DRY RUN is true, nothing will be modified"
	if DRY_RUN == False: print "DRY RUN is false, things are happening for real"
	print "#########################################################"

def get_instances (): 
	CONN = boto.ec2.connect_to_region("us-west-1", profile_name = PROFILE)
	ALL_SNAPS = CONN.get_all_snapshots()
	INSTANCES = []
	for SNAP in ALL_SNAPS:
		SNAP_NAME = SNAP.description
		if re.search("CPM_job_policy_name_here", SNAP_NAME):
			INSTANCE_ID = SNAP_NAME.split(" ")[6]  
			if INSTANCE_ID not in INSTANCES:
				INSTANCES.append(INSTANCE_ID)
				print "adding this instance to the list : " + INSTANCE_ID
	print "WARNING, this script will shutdown ALL instance you are reverting : "
	print INSTANCES
	return INSTANCES
		

#this function take a list of instances and reverts each one to it's most recent snapshot		
def revert_all (INSTANCES):
	CONN = boto.ec2.connect_to_region("us-west-1", profile_name = PROFILE)
	for ID in INSTANCES:
		print "#########################################################"
		INSTANCE = CONN.get_only_instances(instance_ids=ID)
		print ID
		if 'Name' in INSTANCE[0].tags: print "instance name : " + INSTANCE[0].tags['Name']
		PLACEMENT = INSTANCE[0].placement
		print "Shutting down instance and taking a nap..." 
		if DRY_RUN == False: INSTANCE[0].stop(force=True)
		if DRY_RUN == False: time.sleep(50)
		VOLUMES = CONN.get_all_volumes(filters={'attachment.instance-id': ID }) 
		for V in VOLUMES:
			SNAPSHOTS = V.snapshots()
			A = V.attach_data
			MOUNTPOINT = A.device
			if DRY_RUN == False: V.detach()
			SNAPSHOT = SNAPSHOTS[0]
			if DRY_RUN == False: VOLUME = SNAPSHOT.create_volume(PLACEMENT)
		if DRY_RUN == False: CONN.attach_volume (VOLUME.id, INSTANCE_ID, MOUNTPOINT)
		print "original volume : "+ V.id 
		print "original mountpoint : "+ MOUNTPOINT
		print "snapshot : "+ SNAPSHOT.id
		if DRY_RUN == False: print "new volume : "+ VOLUME.id
		print "instance id : "+ ID 
		print "zone : "+ PLACEMENT
		print "Starting instance..."
		if DRY_RUN == False: INSTANCE[0].start()
		print "#########################################################"
	print "if this script completed without errors, your instance is ready to be started in Opsworks, do that manually"
	print "#########################################################"

#
# MAIN
#

dry_run_notify ( DRY_RUN )
revert_all ( get_instances() )

