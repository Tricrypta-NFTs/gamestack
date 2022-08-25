#!/bin/sh
yum update -y
rpm --import https://package.perforce.com/perforce.pubkey
cat > /etc/yum.repos.d/perforce.repo <<!
[perforce]
name=Perforce
baseurl=http://package.perforce.com/yum/rhel/7/x86_64
enabled=1
gpgcheck=1
!
yum -y install helix-p4d