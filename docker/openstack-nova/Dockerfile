FROM steveej/gentoo-base:latest
MAINTAINER Stefan Junker <code@stefanjunker.de>

euse -E rbd spice usbredir xen
euse -E mysql -p =sys-cluster/nova-2014.1.2*
euse -D modules -p =net-misc/openvswitch-2.3*
emerge --autounmask-write =sys-cluster/nova-2014.1.2*
etc-update --automode -5
echo "sys-cluster/ceph ~amd64" >> /etc/portage/package.accept_keywords
emerge =sys-cluster/nova-2014.1.2* -k

ENTRYPOINT /sbin/init
