FROM steveej/gentoo-base:latest
MAINTAINER Stefan Junker <code@stefanjunker.de>

euse -E mysql -p =app-admin/glance-2014.1.2*
emerge --autounmask-write =app-admin/glance-2014.1.2*
etc-update --automode -5
emerge =app-admin/glance-2014.1.2* -k

ENTRYPOINT /sbin/init
