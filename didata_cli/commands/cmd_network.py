import click
from didata_cli.cli import pass_client
from libcloud.common.dimensiondata import DimensionDataAPIException, DimensionDataNetworkDomain
from libcloud.common.dimensiondata import DimensionDataVlan
from libcloud.common.dimensiondata import DimensionDataFirewallRule
from libcloud.common.dimensiondata import DimensionDataFirewallAddress
from didata_cli.utils import handle_dd_api_exception


@click.group()
@pass_client
def cli(client):
    pass


@cli.command()
@click.option('--datacenterId', type=click.UNPROCESSED, help="Filter by datacenter Id")
@click.option('--networkDomainId', type=click.UNPROCESSED, help="Filter by network domain")
@pass_client
def list_vlans(client, datacenterid, networkdomainid):
    try:
        if networkdomainid is not None:
            networkdomainid = DimensionDataNetworkDomain(networkdomainid, None, None, None, None, None)
        vlans = client.node.ex_list_vlans(
            location=datacenterid,
            network_domain=networkdomainid
        )
        for vlan in vlans:
            click.secho("{0}".format(vlan.name), bold=True)
            click.secho("ID: {0}".format(vlan.id))
            click.secho("Description: {0}".format(vlan.description))
            click.secho("IPv4 Range: {0}/{1}".format(vlan.private_ipv4_range_address, vlan.private_ipv4_range_size))
            click.secho("IPv6 Range: {0}/{1}".format(vlan.ipv6_range_address, vlan.ipv6_range_size))
            click.secho("")
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--networkDomainId', required=True, type=click.UNPROCESSED, help="Network domain to create VLAN under")
@click.option('--name', required=True, type=click.UNPROCESSED, help="Name of the VLAN")
@click.option('--baseIpv4Address', required=True, type=click.UNPROCESSED, help="Base IPv4 Address")
@click.option('--description', type=click.UNPROCESSED, help="Description of the VLAN")
@click.option('--prefixSize', type=click.UNPROCESSED, help="Prefix Size", default='24')
@pass_client
def create_vlan(client, networkdomainid, name, baseipv4address, description, prefixsize):
    try:
        networkdomainid = DimensionDataNetworkDomain(networkdomainid, None, None, None, None, None)
        vlan = client.node.ex_create_vlan(networkdomainid, name, baseipv4address, description, prefixsize)
        click.secho("Successfully created VLAN {0}".format(vlan.id), bold=True, fg='green')
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--vlanId', type=click.UNPROCESSED, required=True, help="ID of the vlan to remove")
@pass_client
def delete_vlan(client, vlanid):
    try:
        client.node.ex_delete_vlan(
            DimensionDataVlan(
                vlanid, None, None, None, None, None, None, None, None, None, None, None
            )
        )
        click.secho("Vlan {0} deleted.".format(vlanid), fg='green', bold=True)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--datacenterId', type=click.UNPROCESSED, help="Filter by datacenter Id")
@pass_client
def list_network_domains(client, datacenterid):
    try:
        network_domains = client.node.ex_list_network_domains(location=datacenterid)
        for network_domain in network_domains:
            click.secho("{0}".format(network_domain.name), bold=True)
            click.secho("ID: {0}".format(network_domain.id))
            click.secho("Description: {0}".format(network_domain.description))
            click.secho("Plan: {0}".format(network_domain.plan))
            click.secho("Location: {0}".format(network_domain.location.id))
            click.secho("Status: {0}".format(network_domain.status))
            click.secho("")
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--datacenterId', required=True, type=click.UNPROCESSED, help="Location for the network domain")
@click.option('--name', required=True, help="Name for the network")
@click.option('--servicePlan', required=True, help="Service plan")
@click.option('--description', help="Description for the network domain")
@pass_client
def create_network_domain(client, datacenterid, name, serviceplan, description):
    try:
        client.node.ex_create_network_domain(datacenterid, name, serviceplan, description=description)
        click.secho("Network Domain {0} created in {1}".format(name, datacenterid), fg='green', bold=True)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--networkDomainId', type=click.UNPROCESSED, required=True, help="ID of the network domain to remove")
@pass_client
def delete_network_domain(client, networkdomainid):
    try:
        client.node.ex_delete_network_domain(
            DimensionDataNetworkDomain(
                networkdomainid, None, None, None, None, None
            )
        )
        click.secho("Network Domain {0} deleted.".format(networkdomainid), fg='green', bold=True)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--datacenterId', required=True, type=click.UNPROCESSED, help="Location for the network")
@click.option('--name', required=True, help="Name for the network")
@click.option('--servicePlan', required=True, help="Service plan")
@pass_client
def create_network(client, datacenterid, name):
    try:
        client.node.ex_create_network(datacenterid, name)
        click.secho("Network {0} created in {1}".format(name, datacenterid), fg='green', bold=True)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--datacenterId', type=click.UNPROCESSED, help="Filter by datacenter Id")
@pass_client
def list_networks(client, datacenterid):
    try:
        networks = client.node.ex_list_networks(location=datacenterid)
        for network in networks:
            click.secho("{0}".format(network.name), bold=True)
            click.secho("ID: {0}".format(network.id))
            click.secho("Description: {0}".format(network.description))
            click.secho("PrivateNet: {0}".format(network.private_net))
            click.secho("Location: {0}".format(network.location.id))
            click.secho("")
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--networkId', type=click.UNPROCESSED, required=True, help="ID of the network to remove")
@pass_client
def delete_network(client, networkid):
    try:
        client.node.ex_delete_network(networkid)
        click.secho("Network {0} deleted.".format(id), fg='green', bold=True)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--name', required=True, help="Name for the rule")
@click.option('--action', required=True, type=click.Choice(['ACCEPT_DECISIVELY', 'DROP']))
@click.option('--networkId', type=click.UNPROCESSED, required=True, help="The network domain to apply the rule to")
@click.option('--ipVersion', required=True, type=click.Choice(['IPV4', 'IPV6']))
@click.option('--protocol', required=True, type=click.Choice(['IP', 'ICMP', 'TCP', 'UDP']))
@click.option('--sourceIP', required=True, help="ANY or valid IPv4/IPv6 address")
@click.option('--sourceIP_prefix_size', required=False, help="Only required if specify a range of hosts, e.g. 24")
@click.option('--sourceStartPort', required=True,
              help="ANY or port number. If ANY or single port, endport not required")
@click.option('--sourceEndPort', required=False, help="Port number, required only for port range", default=None)
@click.option('--destinationIP', required=True, help="ANY or valid IPv4/IPv6 address")
@click.option('--destinationIP_prefix_size', required=False, help="Only required if specify a range of hosts, e.g. 24")
@click.option('--destinationStartPort', required=True,
              help="ANY or port number. If ANY or single port, endport not required")
@click.option('--destinationEndPort', required=False, help="Port number, required only for port range", default=None)
@click.option('--position', required=True, type=click.Choice(['FIRST', 'LAST']))
@pass_client
def create_firewall_rule(client, name, action, networkid, ipversion, protocol, sourceip, sourceip_prefix_size,
                         sourcestartport, sourceendport, destinationip, destinationip_prefix_size, destinationstartport,
                         destinationendport, position):
    try:
        network_domain = client.node.ex_get_network_domain(networkid)
        source_any = True if sourceip == 'ANY' else False
        dest_any = True if destinationip == 'ANY' else False
        source_address = DimensionDataFirewallAddress(source_any, sourceip, sourceip_prefix_size, sourcestartport,
                                                      sourceendport)
        dest_address = DimensionDataFirewallAddress(dest_any, destinationip, destinationip_prefix_size,
                                                    destinationstartport, destinationendport)
        rule = DimensionDataFirewallRule(id=None, name=name, action=action, location=network_domain.location,
                                         network_domain=network_domain, status=None, ip_version=ipversion,
                                         protocol=protocol, source=source_address, destination=dest_address,
                                         enabled=True)
        client.node.ex_create_firewall_rule(network_domain, rule, position)
        click.secho("Firewall rule {0} created in {1}".format(name, network_domain.name), fg='green', bold=True)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--networkId', type=click.UNPROCESSED, required=True, help="Network Domain ID where the rules live")
@pass_client
def list_firewall_rules(client, networkid):
    try:
        networkDomain = client.node.ex_get_network_domain(networkid)
        rules = client.node.ex_list_firewall_rules(networkDomain)
        for rule in rules:
            source_location = ParseNetworkLocation(rule.source)
            dest_location = ParseNetworkLocation(rule.destination)
            click.secho("{0}".format(rule.name), bold=True)
            click.secho("Status: {0}".format(rule.status))
            click.secho("ID: {0}".format(rule.id))
            click.secho("Enabled: {0}".format(rule.enabled))
            click.secho("Action: {0}".format(rule.action))
            click.secho("IP Version: {0}".format(rule.ip_version))
            click.secho("Protocol: {0}".format(rule.protocol))
            click.secho("Source: IP: {0}, Ports: {1}".format(source_location.ip, source_location.ports))
            click.secho("Destination: IP: {0}, Ports: {1}".format(dest_location.ip, dest_location.ports))
            click.secho("")
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--networkId', type=click.UNPROCESSED, required=True, help="Network ID where the firewall rule lives")
@click.option('--ruleId', type=click.UNPROCESSED, required=True, help="ID of the fireall rule to remove")
@pass_client
def delete_firewall_rule(client, networkid, ruleid):
    try:
        networkDomain = client.node.ex_get_network_domain(networkid)
        rule = client.node.ex_get_firewall_rule(networkDomain, ruleid)
        client.node.ex_delete_firewall_rule(rule)
        click.secho("Firewall rule {0} deleted.".format(ruleid), fg='green', bold=True)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--networkId', required=True, type=click.UNPROCESSED, help="ID of the network to add the public IP block")
@pass_client
def add_public_ip_block(client, networkid):
    try:
        networkDomain = client.node.ex_get_network_domain(networkid)
        ip_block = client.node.ex_add_public_ip_block_to_network_domain(networkDomain)
        click.secho("Public IP Block with base IP of {0} and block size of {1} added to {2}".format(ip_block.base_ip,
                    ip_block.size, networkid), fg='green', bold=True)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--networkId', type=click.UNPROCESSED, help="ID of the network to list public IP blocks")
@pass_client
def list_public_ip_blocks(client, networkid):
    try:
        networkDomain = client.node.ex_get_network_domain(networkid)
        ip_blocks = client.node.ex_list_public_ip_blocks(networkDomain)
        for ip_block in ip_blocks:
            click.secho("ID: {0}".format(ip_block.id), bold=True)
            click.secho("Base IP: {0}".format(ip_block.base_ip))
            click.secho("Block size: {0}".format(ip_block.size))
            click.secho("Status: {0}".format(ip_block.status))
            click.secho("")
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--ipBlockId', type=click.UNPROCESSED, required=True, help="ID of IP block to remove")
@pass_client
def delete_public_ip_block(client, ipblockid):
    try:
        ip_block = client.node.ex_get_public_ip_block(ipblockid)
        client.node.ex_delete_public_ip_block(ip_block)
        click.secho("Public IP block with id {0} deleted.".format(ipblockid), fg='green', bold=True)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


class ParseNetworkLocation(object):

    def __init__(self, location):
        self._location = location

    @property
    def ip(self):
        if self._location.ip_address == 'ANY':
            return self._location.ip_address
        else:
            return self._location.ip_address + '/' + self._cidr

    @property
    def _cidr(self):
        if self._location.ip_prefix_size is None:
            return '32'
        else:
            return self._location.ip_prefix_size

    @property
    def ports(self):
        if self._location.port_begin is None:
            ports = 'ANY'
        else:
            if self._location.port_end is None:
                ports = self._location.port_begin
            else:
                ports = self._location.port_begin + '-' + self._location.port_end
        return ports
