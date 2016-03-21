Network Sub-Command
===================

create_network_domain
---------------------

This command will create a network domain in a location.  Network domains are the base networking unit in MCP2.0::

    didata network create_network_domain --name <Name> --datacenterId <DC> --description <description> --servicePlan <servicePlan>

delete_network_domain
---------------------

This command will create a network domain in a location::

    didata network delete_network_domain --networkDomainId <networkDomainId>

list_network_domains
--------------------

This command will list all the network domains::

    didata network list_network_domains


create_network
--------------

This command will create a network in a location.  Networks are the base networking unit in MCP10::

    didata network create_network --name <Name> --datacenterId <DC> --servicePlan <servicePlan>

delete_network
--------------

This command will delete a network in a location::

    didata network delete_network --networkId <networkId>

list_networks
-------------

This command will list all the networks::

    didata network list_networks

create_vlan
-----------

This command will create a vlan in a network domain with a defaulted /24::

    didata network create_vlan --name <Name> --networkDomainId <DC> --baseIpv4Address <ipv4>

delete_vlan
--------------

This command will delete a vlan::

    didata network delete_vlan --vlanId <vlanId>

list_vlans
----------

This command will list all vlans::

    didata network list_vlans

create_firewall_rule
--------------------

This command will create a firewall rule in.  MCP2.0 Only::

    didata network create_firewall_rule --name <name> --action <ACCEPT_DECISIVELY|DROP> --networkDomainId <networkDomainId> --ipVerson <IPv4|IPv6> --sourceIP <SOURCE_IP> --destinationIP <DEST_IP> --sourceStartPort <PORT> --destinationStartPort <PORT> --position <FIRST|LAST>

delete_firewall_rule
--------------------

This command will delete firewall rule::

    didata network delete_firewall_rule --networkDomainId <networkDomainId> --ruleId <ruleId>

list_firewall_rules
-------------------

This command will list all vlans::

    didata network list_firewall_rules --networkDomainId <networkDomainId>
