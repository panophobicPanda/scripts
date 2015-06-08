#!/usr/bin/env python
# 2015-03-27
#https://github.com/akabdog/scripts
#define your PROFILE in ~/.boto like this:
#[profile aws-prod]
#aws_access_key_id = ****
#aws_secret_access_key = ****
#

import boto.route53
import time

#####<USER CONFIGURABLE VARIABLES>######
#
#profile name from .boto:
PROFILE = "aws-prod"
#
#zone to connect to:
ZONE = "the408.com."
#dns record to be created:
RECORD_TYPE = "CNAME"
DNS_NAME = "f.the408.com."
DNS_VALUE = "load-balancer.the408.com"
#
#####</USER CONFIGURABLE VARIABLES>#####

def dns ( str ):
    print "connecting to zone %s with a profile %s " % (ZONE,PROFILE)
    conn = boto.route53.connect_to_region("us-west-1", profile_name = str )
    zone = conn.get_zone( ZONE )
    print "adding %s record named %s ==> %s" % (RECORD_TYPE,DNS_NAME,DNS_VALUE)
    status = zone.add_record( RECORD_TYPE, DNS_NAME, DNS_VALUE )
#
# MAIN
#
dns( PROFILE )
