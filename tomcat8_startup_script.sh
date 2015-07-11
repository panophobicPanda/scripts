#!/bin/sh
#
# /etc/init.d/tomcat -- startup script for the Tomcat 8 servlet engine
#
# Written by Miquel van Smoorenburg <miquels@cistron.nl>.
# Modified for Debian GNU/Linux by Ian Murdock <imurdock@gnu.ai.mit.edu>.
# Modified for Tomcat by Stefan Gybas <sgybas@debian.org>.
# Modified for Tomcat6 by Thierry Carrez <thierry.carrez@ubuntu.com>.
# Modified for Tomcat7 by Ernesto Hernandez-Novich <emhn@itverx.com.ve>.
# Modified for Tomcat8 by https://github.com/akabdog
# Additional improvements by Jason Brittain <jason.brittain@mulesoft.com>.
#
### BEGIN INIT INFO
# Provides:          tomcat7
# Required-Start:    $local_fs $remote_fs $network
# Required-Stop:     $local_fs $remote_fs $network
# Should-Start:      $named
# Should-Stop:       $named
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start Tomcat.
# Description:       Start the Tomcat servlet engine.
### END INIT INFO

set -e

PATH=/bin:/usr/bin:/sbin:/usr/sbin
NAME=tomcat8
DESC="Tomcat servlet engine"
DEFAULT=/etc/default/$NAME
JVM_TMP=/tmp/tomcat8-$NAME-tmp

if [ `id -u` -ne 0 ]; then
        echo "You need root privileges to run this script"
        exit 1
fi

# Make sure tomcat is started with system locale
if [ -r /etc/default/locale ]; then
        . /etc/default/locale
        export LANG
fi

. /lib/lsb/init-functions

if [ -r /etc/default/rcS ]; then
        . /etc/default/rcS
fi

# Tomcat auto-start
#
# description: Auto-starts tomcat
# processname: tomcat
# pidfile: /var/run/tomcat.pid
 
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
export CATALINA_HOME=/health_fidelity/apache-tomcat-8.0.23
 
case $1 in
start)
    sh $CATALINA_HOME/bin/startup.sh
    ;;
stop)
    sh $CATALINA_HOME/bin/shutdown.sh
    ;;
restart)
    sh $CATALINA_HOME/bin/shutdown.sh
    sh $CATALINA_HOME/bin/startup.sh
    ;;
esac
exit 0
