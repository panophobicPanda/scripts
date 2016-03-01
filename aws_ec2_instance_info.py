#!/usr/bin/python
#bsmith@the408.com  2015-04-06
#https://github.com/akabdog/scripts


import boto.ec2

def instances ( str ):
    conn = boto.ec2.connect_to_region("us-west-1", profile_name = str)
    instances = conn.get_only_instances()
    for instance in instances:
        if 'Name' in instance.tags:
                print "%s %s %s %s" % (instance.instance_type, instance.state, instance.id, instance.tags['Name'])
        else:
                print "%s %s %s" % (instance.instance_type, instance.state, instance.id)
        for group in instance.groups:
                print(group.id)
#
# MAIN
#
instances("prod")
