#!/usr/bin/perl

#bsmith@the408.com August 2013
#this script started with the one from https://github.com/tomdc/graphite-zpool/blob/master/zpool_iostat.pl but hardly resembles it now

# Pushes zpool metrics to carbon: disk usage of zpool 
# Graphite path: iostat.{hostname}.{zfs}.metric
#

use strict;
use IO::Socket;

######################################
#WARNING: if you enable debug, uncomment the crontab first or you will spam yourself and CORAID !
my $debug=0;
#my $iostat_iterations=10;
my $carbon_server='10.10.16.248';
my $carbon_port='2003';
my $zpool='zpool1';
sub remove_percent_sign;
sub send_to_graphite;
######################################

my @iostat=`zpool list $zpool`;
my $time=time();
my $hostname=`hostname`;
my ($used_percent);
chomp $hostname;

foreach my $line (@iostat) {
	chomp $line;
	if ( $line =~ /NAME/ ) { next; }
	my ($zfs, $size, $alloc, $free, $cap, $dedup, $health, $altroot);
	if ( $line =~ /\A$zpool/ ) { 
		($zfs, $size, $alloc, $free, $cap, $dedup, $health, $altroot) = split m'\s+', $line;
		print "$line\n" if $debug;
		print "zfs: $zfs -- size: $size -- alloc: $alloc -- free: $free -- cap: $cap -- dedup: $dedup -- health: $health -- altroot: $altroot\n\n" if $debug;
	$used_percent = $cap;
	
	}
}

remove_percent_sign($used_percent);

print "Used Percent without percentage sign: $used_percent\n\n" if $debug;

send_to_graphite($zpool, $used_percent);


sub remove_percent_sign {
	if ($_[0] =~ /\%/) {
		$_[0] =~ s/\%//; 
	}
	return $_[0];
}

sub send_to_graphite {
## Prep the socket
# code from benr http://cuddletech.com/blog/?category_name=solaris
	my $sock = IO::Socket::INET->new(
    		Proto => 'tcp',
    		PeerPort => $carbon_port,
    		PeerAddr => $carbon_server,
	) or die "Could not create socket: $!\n";

	my $zfs=$_[0];
	my $cap=$_[1];

	print "iostat\.$hostname\.$zfs.usage $cap $time\n" if $debug;
	$sock->send("iostat\.$hostname\.$zfs.usage $cap $time\n") or die "Send error: $!\n";
}
