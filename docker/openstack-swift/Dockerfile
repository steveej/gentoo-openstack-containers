FROM steveej/gentoo-base:latest
MAINTAINER Stefan Junker <code@stefanjunker.de>

euse -E account container object proxy -p =sys-cluster/swift-2014.1.9999
emerge --autounmask-write =sys-cluster/swift-2014.1.9999
etc-update --automode -5
emerge =sys-cluster/swift-2014.1.9999 -k

ENTRYPOINT /sbin/init
