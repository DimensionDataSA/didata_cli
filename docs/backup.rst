Backup Sub-Command
==================

enable
------

Enable Backups for a Host::

    didata backup enable --serverId <serverId>

disable
-------

Disable Backups for a Host::

    didata backup disable --serverId <serverId>

add_client
----------

Add a client for a Host::

    didata backup add_client --serverId <serverId> --clientType <clientType> --schedulePolicy <schedulePolicy> --storagePolicy <storagePolicy> --notifyEmail <emailaddr> --trigger ON_FAILURE

remove_client
-------------

Remove a backup client for a Host::

    didata backup remove_client --serverId <serverId> --clientType <clientType>

info
----

Gets the backup info for a Host::

    didata backup info --serverId <serverId>

download_url
------------

Gets the backup download url for a Host::

    didata backup download_url --serverId <serverId>

list_available_client_types
---------------------------

There are a few client types.

- FA.AD
- FA.Win
- FA.Linux
- MySQL
- PostgreSQL

This command will filter this to the available client types for a Host::

    didata backup list_available_client_types --serverId <serverId>

list_available_storage_policies
-------------------------------

There are a ton of storage policies.

- 7 Day Storage Policy
- 7 Day Storage Policy + Secondary Copy
- 14 Day Storage Policy
- 14 Day Storage Policy + Secondary Copy
- Ect.

This command will filter this to the available storage policies for a Host::

    didata backup list_available_storage_policies --serverId <serverId>

list_available_schedule_policies
--------------------------------

There are a few schedule policies.

- 12AM - 6AM
- 6AM - 12PM
- 12PM - 6PM
- 6PM - 12AM

This command will filter this to the available storage policies for a Host::

    didata backup list_available_schedule_policies --serverId <serverId>
