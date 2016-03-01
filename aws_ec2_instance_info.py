#!/usr/bin/python
#bsmith@the408.com  2015-04-06
#https://github.com/akabdog/scripts


from __future__ import print_function

import boto.ec2
import pprint

def instances ( str ):
    conn = boto.ec2.connect_to_region("us-east-1", profile_name = str)
    instances = conn.get_only_instances()
    for instance in instances:
        print(instance.private_ip_address, instance.ip_address, instance.instance_type, instance.state, instance.id, instance.tags, end="")
        for group in instance.groups:
                print(" "+group.id, end="")
	print("")
#
# MAIN
#
instances("prod")
