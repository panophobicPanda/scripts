#!/usr/bin/python
#github akabdog

import boto.ec2
import time

INSTANCE_ID = "i-axc35731"
DRY_RUN = True 

print "WARNING, this script will shutdown the instance you are reverting : " + INSTANCE_ID
print "REMINDER, disable auto-healing on the Opsworks layer to allow instance shutdowns."
 
def revert ( str ):
	conn = boto.ec2.connect_to_region("us-west-1", profile_name = str)
	instance = conn.get_only_instances(instance_ids=[ INSTANCE_ID ])
	if 'Name' in instance[0].tags: print "instance name :" + instance[0].tags['Name']
	PLACEMENT = instance[0].placement
	if DRY_RUN == False: instance[0].stop(force=True)
#TODO: instead of a sleep, add a loop to check for when the instance is finally shutdown, then proceed
	if DRY_RUN == False: time.sleep(50)
	volumes = conn.get_all_volumes(filters={'attachment.instance-id': INSTANCE_ID }) 
	for v in volumes:
		snapshots = v.snapshots()
		a = v.attach_data
		MOUNTPOINT = a.device
		if DRY_RUN == False: v.detach()
		SNAPSHOT = snapshots[0]
		if DRY_RUN == False: VOLUME = SNAPSHOT.create_volume(PLACEMENT)
		if DRY_RUN == False: conn.attach_volume (VOLUME.id, INSTANCE_ID, MOUNTPOINT)
		print "original volume : "+ v.id 
		print "original mountpoint : "+ MOUNTPOINT
		print "snapshot : "+ SNAPSHOT.id
		if DRY_RUN == False: print "new volume : "+ VOLUME.id
	print "instance id : "+ INSTANCE_ID 
	print "zone : "+ PLACEMENT
	print "if this script completed without errors, your instance is ready to be started in Opsworks, do that manually"
			
#
# MAIN
#
revert("aws-prod")
