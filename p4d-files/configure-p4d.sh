#!bin/bash

mkfs -t xfs /dev/sdb
mkdir -p /mnt/team/root
mount /dev/sdb /mnt/team/root
echo '/dev/sdb       /mnt/team/root   xfs    defaults,nofail        0       2' >> /etc/fstab

mkfs -t xfs /dev/sdc
mkdir -p /mnt/team/journals
mount /dev/sdc /mnt/team/journals
echo '/dev/sdc       /mnt/team/journals   xfs    defaults,nofail        0       2' >> /etc/fstab

export P4ROOT="/mnt/team"
export P4PORT="ssl:1666"
export P4PASSWD=$(curl --silent http://169.254.169.254/latest/meta-data/instance-id)
export P4ADDRESS="ssl:1666"
/opt/perforce/sbin/configure-helix-p4d.sh main -p $P4ADDRESS -r $P4ROOT -u super -P $P4PASSWD --case 0 -n

sed -i '16i\        P4PORT    =     ssl:1666' /etc/perforce/p4dctl.conf.d/main.conf