FROM steveej/gentoo-base:latest
MAINTAINER Stefan Junker <code@stefanjunker.de>

emerge --autounmask-write =www-apps/horizon-2014.1.2*
etc-update --automode -5
emerge =www-apps/horizon-2014.1.2* -k

ENTRYPOINT /sbin/init
