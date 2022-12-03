#!/bin/bash

function create_macvlans()
{
    ip link set $PARENT_IFACE promisc on
    ip addr del $PARENT_IP dev $PARENT_IFACE 2> /dev/null

    ip link add link $PARENT_IFACE dev $PARENT_IFACE.1 type macvlan mode ${MACVLAN_MODE}
    ip link set $PARENT_IFACE.1 up
    ip addr add 192.168.0.254/24 dev $PARENT_IFACE.1

    ip link add link $PARENT_IFACE dev $PARENT_IFACE.2 type macvlan mode ${MACVLAN_MODE}
    ip link set $PARENT_IFACE.2 up
    ip addr add 192.168.1.254/24 dev $PARENT_IFACE.2

    ip link add link $PARENT_IFACE dev $PARENT_IFACE.3 type macvlan mode ${MACVLAN_MODE}
    ip link set $PARENT_IFACE.3 up
    ip addr add 192.168.2.254/24 dev $PARENT_IFACE.3

    ip addr del $PARENT_IP dev $PARENT_IFACE 2> /dev/null
}

function delete_macvlans()
{
    ip link del dev ${PARENT_IFACE}.1 2> /dev/null
    ip link del dev ${PARENT_IFACE}.2 2> /dev/null
    ip link del dev ${PARENT_IFACE}.3 2> /dev/null
    dhclient ${PARENT_IFACE} -r
}

function print_usage()
{
    echo "\
Usage: sudo $0 <iface> <add|del> [mode]

	iface:   the parent interface to use for configuring macvlans
	add|del: choose up to add macvlans and del to delete them
	mode:    macvlan mode to create ; default value: bridge
"
}

## Main
# Primary test: sudo user + argument count
if [ $EUID -ne 0 ]; then
    echo -e "Please run with sudo user access right\n"
    print_usage
    exit 1
fi
if [ "$#" -ne 2 ] && [ "$#" -ne 3 ]; then
    print_usage
    exit 2
fi

PARENT_IFACE=$1
OPERATION=$2
MACVLAN_MODE="${3:-bridge}"
PARENT_IP=$(ip -f inet addr show $PARENT_IFACE | awk '/inet / {print $2}')

# Test arguemnt 1 validity
type=$(nmcli device show ${PARENT_IFACE} 2> /dev/null | awk '{ if ($1=="GENERAL.TYPE:") print $2}')
if [ $? -ne 0 ] || [ "$type" != "ethernet" ]; then
    echo "Interfcae does not exist or is not ethernet"
    exit 3
fi

case ${OPERATION} in
    add)
    create_macvlans
    ;;

    del)
    delete_macvlans
    ;;

    *)
    print_usage
    exit 4
    ;;
esac

exit 0
