#!/usr/bin/python
# https://github.com/akabdog 2015-06-12
#
# This script will check the WAN ip from wherever you run it, then add it to all "HQ and Remote" security groups for prod and dev, if it doesn't already exist.

import boto.ec2
import urllib2
import re

DRY_RUN = False 
URL = 'http://ip.the408.com'
DEV_SG_STRING = "Some_string_in_SG_name"
PROD_SG_STRING = "Some_other_string_in_SG_name"

def dry_run_notify (DRY_RUN):
        if DRY_RUN == True: print "DRY RUN is true, nothing will be modified"
        if DRY_RUN == False: print "DRY RUN is false, things are happening for real"
        print "#########################################################"

def get_wan_ip ():
	wan_ip = urllib2.urlopen(URL)
	wan_ip = wan_ip.read()
	wan_ip = wan_ip.rstrip()
	wan_ip = wan_ip + '/32'
	print "I think your IP is " + wan_ip + " this is what we will be adding."
	return wan_ip
	

def add_ip_dev (profile, wan_ip, sg_string):
	conn = boto.ec2.connect_to_region("us-west-1", profile_name = profile)
	groups = conn.get_all_security_groups()
	for group in groups:
		if re.search(sg_string, group.name):
			print '########## Using ' + profile + ' to add ' + wan_ip + ' to ' + group.name + ' ##########'
			try:
				if DRY_RUN == False: group.authorize('tcp', 0, 65535, wan_ip)
				print "ADDED\n"
			except boto.exception.BotoServerError as e:
				if e.error_code == "InvalidPermission.Duplicate":
					print "Entry already exists\n"
				else:
					print e.error_code
				
#
# MAIN
#
dry_run_notify ( DRY_RUN )
wan_ip = get_wan_ip()
add_ip_dev('dev', wan_ip, DEV_SG_STRING)
add_ip_dev('prod', wan_ip, PROD_SG_STRING)
