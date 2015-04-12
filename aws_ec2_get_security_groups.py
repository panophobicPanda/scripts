#!/usr/bin/python
#bsmith@the408.com 2015-04-12
#https://github.com/akabdog/scripts
 
import boto.ec2
 
def security_groups ( str ):
    conn = boto.ec2.connect_to_region("us-west-1", profile_name = str)
    groups = conn.get_all_security_groups()
    for group in groups:
        print "%s %s %s" % (group.name, group.vpc_id, group.id)
        print "\tPROTOCOL\tFROM PORT\tTO PORT\t\tGRANTS"
        for rule in group.rules:
            print "\t%s\t\t%s\t\t%s\t\t%s" % (rule.ip_protocol, rule.from_port, rule.to_port, rule.grants)
 
#
# MAIN
#
security_groups("aws-prod")
