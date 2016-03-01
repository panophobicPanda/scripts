#!/usr/bin/python
#bsmith@the408.com  2015-04-06
#https://github.com/akabdog/scripts


from __future__ import print_function

import boto.ec2

def instances ( str ):
    conn = boto.ec2.connect_to_region("us-east-1", profile_name = str)
    instances = conn.get_only_instances()
    for instance in instances:
        if 'Name' in instance.tags:
                print(instance.instance_type, instance.state, instance.id, instance.tags['Name'], end="")
        else:
                print(instance.instance_type, instance.state, instance.id, end="")
        for group in instance.groups:
                print(" "+group.id, end="")
	print("")
#
# MAIN
#
instances("prod")
