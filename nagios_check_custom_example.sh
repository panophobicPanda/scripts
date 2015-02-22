#!/bin/bash
#this will test the ability of a given sid and namespace to axl lock on a CC node

#this SID will be used for the test
sid=p4a5

outputFile=/tmp/nagios/.axl_health_check_cc
echo -n " " > $outputFile

#to add new namespaces, increment this loop
for i in 1 {5..11} {13..14}; do
	result=" "
	result=$(sudo /usr/bin/timeout 30 /usr/local/axcient/axl -s $sid -c /usr/local/axcient/ax_Gen2_SJC$i.conf /bin/ls -a 2>&1)
	echo $result | grep ".cc_nagios_health_check" > /dev/null

	if [ $? -eq 0 ]; then
			echo -n " namespace$i OK," >> $outputFile
		else
			echo -n " namespace$i CRITICAL," >> $outputFile
	fi
done


cat $outputFile | grep "CRITICAL" > /dev/null

if [ $? -eq 0 ]; then
	echo "CRITICAL - `cat $outputFile`"
	exit 2
		else
	echo "OK - `cat $outputFile`"
	exit 0
fi
