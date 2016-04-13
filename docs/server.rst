Server Sub-Command
==================

list
----

This is likely the most common command that will be used::

    didata server list

filters
*******

You can filter the list of servers easily to your specification.
The filters include:

- datacenterId
- networkId
- networkDomainId
- vlanId
- state
- started
- ipv6
- privateIpv4
- sourceImageId
- name

Filter by datacenterId::

    didata server list --datacenterId <DC>

Filter by datacenterId and name::

    didata server list --datacenterId <DC> --name <name>


info
----

To get info on only a single server, instead of filtering you can just pass in the server id to the info command::

    didata server info --serverId <SERVER_ID>

create
------

This is how you can provision a server in the cli::

    didata server create --name <name> --description <description> --imageId <imageId> --autostart --networkDomainId <networkDomainId> --vlanId <vlanId> --administratorPassword <password>

destroy
-------

This is how you can remove a server in the cli::

    didata server destory --serverId <SERVER_ID>


shutdown
--------

This is how you can shutdown a server in the cli::

    didata server shutdown --serverId <SERVER_ID>

shutdown-hard
-------------

This is how you can shutdown a server in the cli
It will doing a hard poweroff and you may lose some state::

    didata server shutdown-hard --serverId <SERVER_ID>

reboot
------

This is how you can reboot a server in the cli::

    didata server reboot --serverId <SERVER_ID>

reboot-hard
-----------

This is how you can reboot a server in the cli
It will doing a hard reboot and you may lose some state::

    didata server reboot-hard --serverId <SERVER_ID>

start
-----

This is how you can start a server in the cli::

    didata server start --serverId <SERVER_ID>

update_cpu_count
----------------

This command will update the cpu count on a particular server::

    didata server update_cpu_count --serverId <SERVER_ID> --cpuCount 8

update_ram
----------

This command will update the ram (GB) on a particular server::

    didata server update_ram --serverId <SERVER_ID> --ramInGB 8

add_disk
--------

This command will add a new disk to a particular server::

    didata server add_disk --serverId <SERVER_ID> --size 50 --speed STANDARD


remove_disk
-----------

This command will remove a disk in slot 2 from a particular server::

    didata server remove_disk --serverId <SERVER_ID> --diskId 2

modify_disk
-----------

This command will modify a disk in slot 2 to be 60Gb::

    didata server modify_disk --serverId <SERVER_ID> --diskId 2 --size 60

This command will modify a disk in slot 2 to be HIGH PERFORMANCE::

    didata server modify_disk --serverId <SERVER_ID> --diskId 2 --speed HIGHPERFORMANCE
