import click
from didata_cli.cli import pass_client
from libcloud.common.dimensiondata import DimensionDataAPIException
from didata_cli.utils import handle_dd_api_exception
from didata_cli.filterable_response import DiDataCLIFilterableResponse
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


@click.group()
@pass_client
def cli(client):
    pass


@cli.command()
@click.option('--name', type=click.UNPROCESSED, help="Name of the key", required=True)
@click.option('--description', help="Description of tag")
@click.option('--valueRequired', is_flag=True, default=False, help="If a key value is required")
@click.option('--displayOnReport', is_flag=True, default=False, help="If a key should display on usage reports")
@pass_client
def create_key(client, name, description, valuerequired, displayonreport):
    try:
        response = client.node.ex_create_tag_key(name, description, valuerequired, displayonreport)
        if response is True:
            click.secho("Tag key {0} created".format(name), fg='green', bold=True)
        else:
            click.secho("Error when creating tag key".format(name, fg='red', bold=True))
            exit(1)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--tagKeyId', type=click.UNPROCESSED, help="The ID of the tag key", required=True)
@click.option('--name', type=click.UNPROCESSED, help="Name of the key")
@click.option('--description', help="Description of tag")
@click.option('--valueRequired/--no-valueRequired', is_flag=True, default=None, help="Filter if value is required")
@click.option('--displayOnReport/--no-displayOnReport', is_flag=True,
              default=None, help="Filter if tag key should display on report")
@pass_client
def modify_key(client, tagkeyid, name, description, valuerequired, displayonreport):
    try:
        response = client.node.ex_modify_tag_key(tagkeyid, name=name,
                                                 description=description,
                                                 value_required=valuerequired,
                                                 display_on_report=displayonreport)
        if response is True:
            click.secho("Tag key {0} modified".format(tagkeyid), fg='green', bold=True)
        else:
            click.secho("Error when modifying tag key".format(name, fg='red', bold=True))
            exit(1)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--tagKeyId', type=click.UNPROCESSED, help="The ID of the tag key", required=True)
@pass_client
def remove_key(client, tagkeyid):
    try:
        response = client.node.ex_remove_tag_key(tagkeyid)
        if response is True:
            click.secho("Tag key {0} removed".format(tagkeyid), fg='green', bold=True)
        else:
            click.secho("Error when removing tag key", fg='red', bold=True)
            exit(1)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--id', help="Filter by ID")
@click.option('--name', type=click.UNPROCESSED, help="Filter by name")
@click.option('--valueRequired/--no-valueRequired', is_flag=True, default=None, help="Filter if value is required")
@click.option('--displayOnReport/--no-displayOnReport', is_flag=True,
              default=None, help="Filter if tag key should display on report")
@click.option('--query', type=click.UNPROCESSED, help="The query to pass to the filterable response")
@pass_client
def list_keys(client, id, name, valuerequired, displayonreport, query):
    tag_key_list = client.node.ex_list_tag_keys(id=id, name=name,
                                                value_required=valuerequired,
                                                display_on_report=displayonreport)
    response = DiDataCLIFilterableResponse()
    for tag_key in tag_key_list:
        response.add(_tag_key_to_dict(tag_key))
    if not response.is_empty():
        if query is not None:
            response.do_filter(query)
        click.secho(response.to_string(client.output_type))
    else:
        click.secho("No tags found", fg='red', bold=True)


@cli.command()
@click.option('--id', help="The asset ID to tag", required=True)
@click.option('--assetType', required=True,
              type=click.Choice(['SERVER', 'VLAN']),
              help="The type of asset to tag")
@click.option('--tagKeyName', type=click.UNPROCESSED, help="The key name", required=True)
@click.option('--tagKeyValue', help="The value of the key if needed")
@pass_client
def apply(client, id, assettype, tagkeyname, tagkeyvalue):
    try:
        asset = _get_asset(client, id, assettype)
        response = client.node.ex_apply_tag_to_asset(asset, tagkeyname, tagkeyvalue)
        if response is True:
            click.secho("Tag applied to {0}".format(id), fg='green', bold=True)
        else:
            click.secho("Error when applying tag", fg='red', bold=True)
            exit(1)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--id', help="The asset ID to tag", required=True)
@click.option('--assetType', required=True,
              type=click.Choice(['SERVER', 'VLAN']),
              help="The type of asset to tag")
@click.option('--tagKeyName', type=click.UNPROCESSED, help="The key name", required=True)
@pass_client
def remove(client, id, assettype, tagkeyname):
    try:
        asset = _get_asset(client, id, assettype)
        response = client.node.ex_remove_tag_from_asset(asset, tagkeyname)
        if response is True:
            click.secho("Tag removed from {0}".format(id), fg='green', bold=True)
        else:
            click.secho("Error when removing tag", fg='red', bold=True)
            exit(1)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--assetId', help="Filter by asset ID")
@click.option('--assetType', help="Filter by asset type")
@click.option('--datacenter', help="Filter by datacenter")
@click.option('--tagKeyId', type=click.UNPROCESSED, help="Filter by tag key id")
@click.option('--tagKeyName', type=click.UNPROCESSED, help="Filter by tag key name")
@click.option('--tagKeyValue', type=click.UNPROCESSED, help="Filter by tag key value")
@click.option('--valueRequired/--no-valueRequired', is_flag=True, default=None, help="Filter if value is required")
@click.option('--displayOnReport/--no-displayOnReport', is_flag=True,
              default=None, help="Filter if tag key should display on report")
@click.option('--query', type=click.UNPROCESSED, help="The query to pass to the filterable response")
@pass_client
def list(client, assetid, assettype, datacenter, tagkeyid,
         tagkeyname, tagkeyvalue, valuerequired, displayonreport, query):
    tag_list = client.node.ex_list_tags(asset_id=assetid, asset_type=assettype,
                                        location=datacenter, tag_key_name=tagkeyname,
                                        tag_key_id=tagkeyid, value=tagkeyvalue,
                                        value_required=valuerequired,
                                        display_on_report=displayonreport)
    response = DiDataCLIFilterableResponse()
    for tag in tag_list:
        response.add(_tag_to_dict(tag))
    if not response.is_empty():
        if query is not None:
            response.do_filter(query)
        click.secho(response.to_string(client.output_type))
    else:
        click.secho("No tags found", fg='red', bold=True)


def _get_asset(client, id, type):
    if type == 'SERVER':
        return client.node.ex_get_node_by_id(id)
    if type == 'VLAN':
        return client.node.ex_get_vlan(id)
    else:
        raise "Unhandled asset type"


def _tag_key_to_dict(tag_key):
    tag_key_dict = OrderedDict()
    tag_key_dict['ID'] = tag_key.id
    tag_key_dict['Name'] = tag_key.name
    tag_key_dict['Description'] = tag_key.description
    tag_key_dict['Value Required'] = tag_key.value_required
    tag_key_dict['Display on Report'] = tag_key.display_on_report
    return tag_key_dict


def _tag_to_dict(tag):
    tag_dict = OrderedDict()
    tag_dict['Asset ID'] = tag.asset_id
    tag_dict['Asset Type'] = tag.asset_type
    tag_dict['Asset Name'] = tag.asset_name
    tag_dict['Datacenter'] = tag.datacenter
    tag_dict['Key ID'] = tag.key.id
    tag_dict['Key Name'] = tag.key.name
    tag_dict['Value'] = tag.value
    return tag_dict
