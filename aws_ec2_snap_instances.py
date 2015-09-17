#!/usr/bin/python
# 2015-09-17
# https://github.com/akabdog


####USER_CONFIGURABLE_VARIABLES########
#backup all volumes on all instances which contain this substring in their name tag:
search_name="mysql"
#created snapshots will have this description:
snap_desc="test-deleteme"
####END_CONFIGURABLE_VARIABLES################################


import boto.ec2

def connect ( str ):
        conn = boto.ec2.connect_to_region("us-west-1", profile_name = str)
        return conn

def getInstanceIds ( con, str ):
        a = []
        instances = con.get_only_instances()
        for instance in instances:
                if 'Name' in instance.tags:
                        if str in instance.tags['Name']:
                                print instance.tags['Name']
                                print instance.id
                                a.append(instance.id)
        return a

def snapVolumes ( con, i, desc ):
        instances = con.get_only_instances(instance_ids=i)
        for instance in instances:
                print instance
                volumes = con.get_all_volumes(filters={'attachment.instance-id': instance.id})
                for volume in volumes:
                        print volume
                        volume.create_snapshot(description=desc)

#
# MAIN
#
con=connect("aws-prod")
instances=getInstanceIds(con, search_name)
snapVolumes(con, instances, snap_desc)
