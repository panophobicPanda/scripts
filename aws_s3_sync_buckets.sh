#!/bin/bash
#https://github.com/akabdog 2015-05-29
#
#make sure you've preconfigured your aws creds before running this script:
#aws configure --profile dev
#aws configure --profile prod 
#
TEMP_DIR=/tmp/configs-qa/nonsensitive

mkdir -p $TEMP_DIR 
rm -rf $TEMP_DIR/*

aws --profile dev s3 cp s3://configs-qa/nonsensitive/ $TEMP_DIR --recursive

aws --profile prod s3 cp $TEMP_DIR s3://configs-staging/nonsensitive/ --recursive

aws --profile prod s3 cp $TEMP_DIR s3://configs-production/nonsensitive/ --recursive

rm -rf $TEMP_DIR/*
