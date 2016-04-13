import click
from libcloud.compute.drivers.dimensiondata import DimensionDataNodeDriver
from libcloud.backup.drivers.dimensiondata import DimensionDataBackupDriver
from libcloud.common.dimensiondata import DEFAULT_REGION
import os
import sys

CONTEXT_SETTINGS = dict(auto_envvar_prefix='DIDATA')
DEFAULT_OUTPUT_TYPE = 'pretty'


class DiDataCLIClient(object):
    def __init__(self):
        self.verbose = False

    def init_client(self, user, password, region):
        self.node = DimensionDataNodeDriver(user, password, region=region)
        self.backup = DimensionDataBackupDriver(user, password, region=region)

pass_client = click.make_pass_decorator(DiDataCLIClient, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                             'commands'))


class DiDataCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('didata_cli.commands.cmd_' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli


@click.command(cls=DiDataCLI, context_settings=CONTEXT_SETTINGS)
@click.option('--verbose', is_flag=True)
@click.option('--user', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
@click.option('--region', default=DEFAULT_REGION)
@click.option('--outputType', default=DEFAULT_OUTPUT_TYPE)
@pass_client
def cli(client, verbose, user, password, region, outputtype):
    """An interface into the Dimension Data Cloud"""
    client.init_client(user, password, region)
    client.output_type = outputtype
    if verbose:
        click.echo('Verbose mode enabled')
