#!/usr/bin/python
#bsmith@the408.com  2015-04-06 
#https://github.com/akabdog/scripts

import boto.ec2
 
def volumes ( str ):
    conn = boto.ec2.connect_to_region("us-west-1", profile_name = str)
    volumes = conn.get_all_volumes()
    for volume in volumes:
	if 'snapme' in volume.tags:
		print "%s has snapme tag, snapshotting volume" % (volume.id)
		volume.create_snapshot(description="created for by script aws_ec2_snap_preprod_volumes.py")
		
#	else:
#		print "%s %s %s %s" % (instance.vpn_id, instance.instance_type, instance.state, instance.id)
 
#
# MAIN
#
volumes("aws-prod")
