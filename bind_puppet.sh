#!/bin/bash
#This script will quickly bind a puppet client to a puppet server.
#Run this script on the puppet server
#
# bsmith@the408.com 2013-05-13
#
#USAGE - superPuppetClientBind.sh <FQDN>
#EXAMPLE - ./superPuppetClientBind.sh reportdb1.qa.qualys.com
#
#USER CONFIGURABLE VALUES
username=root
#at the moment this script only works using Root
#
puppetServer=sjc-puppetmaster01.test.lan
ntpServer=10.1.2.10
#
#first lets make sure an argument is provided
if [ "$1" != "" ]; then
########## SERVER ##########
#This script will not add the nodes to nodes.pp, do that manually or use a different script
#
#Now clean server certs just in case this client was previously added
puppetca --clean $1
rm /etc/puppet/ssl/ca/signed/$1*
#
########## CLIENT ##########
#Setup Keyless entry just to make it easy
#cat ~/.ssh/id_rsa.pub | ssh $username"@"$1 'mkdir ~/.ssh; cat >> ~/.ssh/authorized_keys2'
#Now lets initiate the client signing request
ssh $username"@"$1 puppetServer=$puppetServer ntpServer=$ntpServer "\
puppet -V;\
service puppet stop;\
#clean old certs in case this was previously bound to a different puppet server
rm -rf /var/lib/puppet/ssl;\
#make sure time is in sync
apt-get -q -y install ntpdate;\
service ntpd stop; ntpdate $ntpServer; service ntpd start;\
#stop all puppet requests
killall /usr/bin/ruby;\
#register client
puppet agent --server=$puppetServer --waitforcert 120"
#
########## SERVER AGAIN ##########
# Sign the cert from the server
sleep 10
/usr/sbin/puppetca --sign $1
sleep 5
#
########## CLIENT AGAIN ##########
#Run the first time to verify and start puppet service
ssh $username"@"$1 puppetServer=$puppetServer "\
puppet agent --server=$puppetServer --no-daemonize --verbose --onetime;"
#
echo "SCRIPT COMPLETE, bye"
exit
#if command $1 was empty
else
        echo "No arguement provided"
        echo "USAGE - superPuppetClientBind.sh <FQDN>
EXAMPLE - ./superPuppetClientBind.sh reportdb1.qa.qualys.com"
fi
#
