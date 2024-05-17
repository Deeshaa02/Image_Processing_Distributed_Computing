#!/usr/bin/env bash
scp -i ./belal.pem ./Master.py ec2-user@ec2-51-20-31-232.eu-north-1.compute.amazonaws.com:/home/ec2-user
scp -i ./belal.pem ./Master.py ec2-user@ec2-13-53-153-74.eu-north-1.compute.amazonaws.com:/home/ec2-user
scp -i ./belal.pem ./Master.py ec2-user@ec2-51-20-53-119.eu-north-1.compute.amazonaws.com:/home/ec2-user
scp -i ./belal.pem ./Slave.py ec2-user@ec2-51-20-31-232.eu-north-1.compute.amazonaws.com:/home/ec2-user
scp -i ./belal.pem ./Slave.py ec2-user@ec2-13-53-153-74.eu-north-1.compute.amazonaws.com:/home/ec2-user
scp -i ./belal.pem ./Slave.py ec2-user@ec2-51-20-53-119.eu-north-1.compute.amazonaws.com:/home/ec2-user


