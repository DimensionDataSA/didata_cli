import click
from didata_cli.cli import pass_client
from libcloud.common.dimensiondata import DimensionDataAPIException
from didata_cli.utils import handle_dd_api_exception, get_single_server_id_from_filters


@click.group()
@pass_client
def cli(config):
    pass


@cli.command()
@click.option('--serverId', type=click.UNPROCESSED, help='The server ID to enable backups on')
@click.option('--servicePlan', required=True, help='The type of service plan to enroll in',
              type=click.Choice(['Enterprise', 'Essentials', 'Advanced']))
@click.option('--serverFilterIpv6', help='The filter for ipv6')
@pass_client
def enable(client, serverid, serviceplan, serverfilteripv6):
    if not serverid:
        serverid = get_single_server_id_from_filters(client, ex_ipv6=serverfilteripv6)
    try:
        extra = {'service_plan': serviceplan}
        client.backup.create_target(serverid, serverid, extra=extra)
        click.secho("Backups enabled for {0}.  Service plan: {1}".format(serverid, serviceplan), fg='green', bold=True)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--serverId', type=click.UNPROCESSED, help='The server ID to disable backups on')
@click.option('--serverFilterIpv6', help='The filter for ipv6')
@pass_client
def disable(client, serverid, serverfilteripv6):
    if not serverid:
        serverid = get_single_server_id_from_filters(client, ex_ipv6=serverfilteripv6)
    try:
        response = client.backup.delete_target(serverid)
        if response is True:
            click.secho("Backups disabled for {0}".format(serverid), fg='green', bold=True)
        else:
            click.secho("Backups not disabled for {0}".format(serverid, fg='red', bold=True))
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--serverId', type=click.UNPROCESSED, help='The server ID to disable backups on')
@click.option('--serverFilterIpv6', help='The filter for ipv6')
@pass_client
def info(client, serverid, serverfilteripv6):
    if not serverid:
        serverid = get_single_server_id_from_filters(client, ex_ipv6=serverfilteripv6)
    try:
        details = client.backup.ex_get_backup_details_for_target(serverid)
        click.secho("Backup Details for {0}".format(serverid))
        click.secho("Service Plan: {0}".format(details.service_plan[0]))
        if len(details.clients) > 0:
            click.secho("Clients:")
            for backup_client in details.clients:
                click.secho("")
                click.secho("{0}".format(backup_client.type.type), bold=True)
                click.secho("ID: {0}".format(backup_client.id))
                click.secho("Schedule: {0}".format(backup_client.schedule_policy))
                click.secho("Retention: {0}".format(backup_client.storage_policy))
                click.secho("DownloadURL: {0}".format(backup_client.download_url))
                if backup_client.running_job is not None:
                    click.secho("Running Job", bold=True)
                    click.secho("ID: {0}".format(backup_client.running_job.id))
                    click.secho("Status: {0}".format(backup_client.running_job.status))
                    click.secho("Percentage Complete: {0}".format(backup_client.running_job.percentage))
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command(help='Adds a backup client')
@click.option('--serverId', type=click.UNPROCESSED, help='The server ID to list backup schedules for')
@click.option('--clientType', required=True, help='The server ID to list backup schedules for')
@click.option('--storagePolicy', required=True, help='The server ID to list backup schedules for')
@click.option('--schedulePolicy', required=True, help='The server ID to list backup schedules for')
@click.option('--triggerOn', type=click.UNPROCESSED, help='The server ID to list backup schedules for')
@click.option('--notifyEmail', type=click.UNPROCESSED, help='The server ID to list backup schedules for')
@click.option('--serverFilterIpv6', help='The filter for ipv6')
@pass_client
def add_client(client, serverid, clienttype, storagepolicy, schedulepolicy, triggeron, notifyemail, serverfilteripv6):
    if not serverid:
        serverid = get_single_server_id_from_filters(client, ex_ipv6=serverfilteripv6)
    try:
        client.backup.ex_add_client_to_target(serverid, clienttype, storagepolicy,
                                              schedulepolicy, triggeron, notifyemail)
        click.secho("Enabled {0} client on {1}".format(clienttype, serverid), fg='red', bold=True)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command(help='Removes a backup client')
@click.option('--serverId', type=click.UNPROCESSED, help='The server ID to list backup schedules for')
@click.option('--clientType', required=True, help='The server ID to list backup schedules for')
@click.option('--serverFilterIpv6', help='The filter for ipv6')
@pass_client
def remove_client(client, serverid, clienttype, serverfilteripv6):
    if not serverid:
        serverid = get_single_server_id_from_filters(client, ex_ipv6=serverfilteripv6)
    try:
        details = client.backup.ex_get_backup_details_for_target(serverid)
        if len(details.clients) <= 0:
            click.secho("No clients found for {0}".format(serverid), fg='red', bold=True)
            exit(1)
        else:
            for backup_client in details.clients:
                if backup_client.type.type == clienttype:
                    client.backup.ex_remove_client_from_target(serverid, backup_client)
                    click.secho("Successfully removed client {0} from {1}".format(clienttype, serverid),
                                fg='green', bold=True)
                    exit(0)
            click.secho("Could not find a client {0} on {1}".format(clienttype, serverid), fg='red', bold=True)
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command(help='Fetch Download URL for Server')
@click.option('--serverId', type=click.UNPROCESSED, help='The server ID to list backup schedules for')
@click.option('--serverFilterIpv6', help='The filter for ipv6')
@pass_client
def download_url(client, serverid, serverfilteripv6):
    if not serverid:
        serverid = get_single_server_id_from_filters(client, ex_ipv6=serverfilteripv6)
    try:
        details = client.backup.ex_get_backup_details_for_target(serverid)
        if len(details.clients) < 1:
            click.secho("No clients configured so there is no backup url", fg='red', bold=True)
            exit(1)
        click.secho("{0}".format(details.clients[0].download_url))
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command(help='List client types available for server')
@click.option('--serverId', type=click.UNPROCESSED, help='The server ID to list backup client types for')
@click.option('--serverFilterIpv6', help='The filter for ipv6')
@pass_client
def list_available_client_types(client, serverid, serverfilteripv6):
    if not serverid:
        serverid = get_single_server_id_from_filters(client, ex_ipv6=serverfilteripv6)
    try:
        client_types = client.backup.ex_list_available_client_types(serverid)
        if len(client_types) < 1:
            click.secho("No available clients types for {0}".format(serverid), fg='red', bold=True)
            exit(1)
        click.secho("Available Client Types:", bold=True)
        for client_type in client_types:
            click.secho("{0}".format(client_type.type))
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command(help='List schedule policies for server')
@click.option('--serverId', type=click.UNPROCESSED, help='The server ID to list backup schedules for')
@click.option('--serverFilterIpv6', help='The filter for ipv6')
@pass_client
def list_available_schedule_policies(client, serverid, serverfilteripv6):
    if not serverid:
        serverid = get_single_server_id_from_filters(client, ex_ipv6=serverfilteripv6)
    try:
        schedules = client.backup.ex_list_available_schedule_policies(serverid)
        if len(schedules) < 1:
            click.secho("No available schedules for {0}".format(serverid), fg='red', bold=True)
            exit(1)
        click.secho("Available Schedule Policies:", bold=True)
        for schedule in schedules:
            click.secho("{0}".format(schedule.name))
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command(help='List storage policies for server')
@click.option('--serverId', type=click.UNPROCESSED, help='The server ID to list backup storage polciies for')
@click.option('--serverFilterIpv6', help='The filter for ipv6')
@pass_client
def list_available_storage_policies(client, serverid, serverfilteripv6):
    if not serverid:
        serverid = get_single_server_id_from_filters(client, ex_ipv6=serverfilteripv6)
    try:
        storage_policies = client.backup.ex_list_available_storage_policies(serverid)
        if len(storage_policies) < 1:
            click.secho("No available storage_policies for {0}".format(serverid), fg='red', bold=True)
            exit(1)
        click.secho("Available Storage Policies:", bold=True)
        for storage_policy in storage_policies:
            click.secho("{0}".format(storage_policy.name))
    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)
