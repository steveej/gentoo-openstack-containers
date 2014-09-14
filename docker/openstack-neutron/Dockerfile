FROM steveej/gentoo-base:latest
MAINTAINER Stefan Junker <code@stefanjunker.de>

euse -E mysql metadata server openvswitch l3 linuxbridge dhcp -p =sys-cluster/neutron-2014.1.2*
euse -D modules -p =net-misc/openvswitch-2.3*
emerge --autounmask-write =sys-cluster/neutron-2014.1.2*
etc-update --automode -5
emerge =sys-cluster/neutron-2014.1.2* -k

ENTRYPOINT /sbin/init
