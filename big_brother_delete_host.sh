#!/bin/bash
#To use this script, first delete the host from bb-hosts, note the exact hostname from bb-hosts (only use the hostname, not FQDN)
#Then pass the hostname as a command line arguement to this script
#
#In Summary: this script takes a single arguement, the host you want deleted from big brother
# WARNING: if no arguement is passed, all historical data will be deleted - this is a feature, not a bug.
# December 2011
# https://github.com/akabdog
#
rm -rf /home/bb/bbvar/logs/$1*
echo  /home/bb/bbvar/logs/$1*
rm -rf /home/bb/bb/www/html/$1*
echo /home/bb/bb/www/html/$1*
rm -rf /home/bb/bbvar/hist/$1*
echo /home/bb/bbvar/hist/$1*
rm -rf /home/bb/bbvar/histlogs/$1*
echo /home/bb/bbvar/histlogs/$1*
/home/bb/bb/runbb.sh restart
