#!/usr/bin/python
#https://github.com/akabdog  2015-05-06 
#until more features are added, this script will use the default credentials in ~/.aws/credentials tagged like [default]

#boto3 is a development edition, install via 'pip install boto3'
import boto3

#for debugging only
#boto3.set_stream_logger('botocore')

#STAGE stack
#stack="19c9bdf5-2fbf-4bf9-b5fe-xxxxxxxxxxxx"
#PROD stack
#stack="3298be32-67d9-4239-86c0-xxxxxxxxxxxx"
#TEST stack
stack="d57a2cac-387c-4c99-b700-xxxxxxxxxxxxx"
customer="cust"
#note: customer name can not have capital letters, since shortnames don't allow caps

#defining function and default values
def new_layer( name, shortname, arn="arn:aws:iam::556708859583:instance-profile/prod-opsworks-ec2-role", sec_groups=[], recipes=[], instance_size="m3.medium", subnet="subnet-b3cdxxxx", volumes=[], OS="", ami="", ):
	ow = boto3.client('opsworks')
#LAYER-CREATION
	result = ow.create_layer(
		StackId=stack, 
		Name=name, 
		Shortname=shortname, 
		Type="custom", 
		CustomInstanceProfileArn=arn, 
		CustomSecurityGroupIds=sec_groups, 
		CustomRecipes=recipes,
		VolumeConfigurations=volumes,
		)
	print "CREATED LAYER - %s" % (name)
	print result
	newLayer=[result[u'LayerId']]
#INSTANCE-CREATION
	result = ow.create_instance(
		StackId=stack, 
		LayerIds=newLayer, 
		InstanceType=instance_size, 
		#Os="Ubuntu 14.04 LTS", 
		Os=OS,
		AmiId=ami,
		SubnetId=subnet,
		)
	print "CREATED INSTANCE"
	print result
	newInstance=result[u'InstanceId']
#STARTING-INSTANCE
	result=ow.start_instance(InstanceId=newInstance)
	print "STARTED INSTANCE"
	print result
	print "==================================================="

def main():
#app1-LAYER
	new_layer(
		name="app1-%s" % (customer),
		shortname="app1-%s-" % (customer),
		sec_groups=[u'sg-c861c3ad'],
		recipes={u'Undeploy': [], u'Setup': [u'create_deploy_user::default', u'create_deploy_user::deploy_dirs', u'export_env::default', u'java::default', u'jsvc::default', u'rvm::system', u'create_deploy_user::copy_configs', u'install_newrelic::default', u'ops_install_cron::production'], u'Configure': [], u'Shutdown': [], u'Deploy': []},
		)
#app2-LAYER
        new_layer(
                name="app2-%s" % (customer),
		shortname="app2-%s-" % (customer),
                sec_groups=[u'sg-fa61c39f'],
                recipes={u'Undeploy': [], u'Setup': [u'ops_install_cron::production', u'create_deploy_user::default', u'java::default', u'jsvc::default', u'rvm::system'], u'Configure': [], u'Shutdown': [], u'Deploy': []},
                instance_size="m3.large",
		OS="Custom",
		ami="ami-f599xxxx",
                )
#app3-LAYER
        new_layer(
                name="app3-%s" % (customer),
                shortname="app3-%s-" % (customer),
                arn="arn:aws:iam::556708859583:instance-profile/aws-opsworks-ec2-role",
                sec_groups=[u'sg-fa61c39f'],
                recipes={u'Undeploy': [], u'Setup': [u'mysql::setup_data_dirs', u'ops_install_cron::production'], u'Configure': [u'install_mysql_pi::default'], u'Shutdown': [], u'Deploy': []},
		OS="Custom",
		ami="ami-7b1dfe3f",
                )
#MYSQL-LAYER
        new_layer(
                name="mysql-%s" % (customer),
                shortname="mysql-%s-" % (customer),
                recipes={u'Undeploy': [], u'Setup': [u'create_deploy_user::default', u'export_env::default', u'mysql::setup_data_dirs', u'ops_install_cron::production'], u'Configure': [u'mysql::upgrade_mysql', u'mysql::bootstrap_database_hf'], u'Shutdown': [], u'Deploy': []},
		volumes=[{u'MountPoint': u'/data', u'Size': 100, u'VolumeType': u'gp2', u'NumberOfDisks': 1}],
                )
# MAIN
#
main()
