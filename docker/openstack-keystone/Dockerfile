FROM steveej/gentoo-base:latest
MAINTAINER Stefan Junker <code@stefanjunker.de>

euse -E mysql =sys-auth/keystone-2014.1.2*
emerge --autounmask-write =sys-auth/keystone-2014.1.2*
etc-update --automode -5
emerge =sys-auth/keystone-2014.1.2* -k

ENTRYPOINT /sbin/init
