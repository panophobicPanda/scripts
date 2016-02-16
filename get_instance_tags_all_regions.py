#!/bin/env python
#bsmith@the408.com 2016-02-16  
#https://github.com/akabdog/scripts

import boto.ec2

for region in boto.ec2.regions():
    try:
        conn = region.connect(profile_name = "profile1")
        instances = conn.get_only_instances()
        for instance in instances:
            if 'Name' in instance.tags:
                    #print "%s %s %s %s" % (instance.instance_type, instance.state, instance.id, instance.tags['Name'])
                    print "%s %s %s %s" % (instance.instance_type, instance.state, instance.id, instance.tags)
            else:
                    print "%s %s %s" % (instance.instance_type, instance.state, instance.id)
    except:
        print "something went wrong, probably 401 for that region"
