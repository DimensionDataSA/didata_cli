Modifying Output
================

Output Types
------------

In the 0.2+ release we have introduced a new mechanism to control what type of output is available.

You can change the output type one of two ways

Exporting a variable for the output type::

    export DIDATA_OUTPUTTYPE=<outputtype>

For one time runs of changing the output::

    didata --outputType <outputtype> server list

Example output types
~~~~~~~~~~~~~~~~~~~~

json::

    [
        {
          "Name": "rhel5-buildserver",
          "ID": "524dd016-5225-4b94-ab4b-e8f6ba240b7a",
          "State": "running",
          "CPU Count": 1
        }
    ]

grid::

    +-------------------+--------------------------------------+---------+-------------+
    | Name              | ID                                   | State   |   CPU Count |
    +===================+======================================+=========+=============+
    | rhel5-buildserver | 524dd016-5225-4b94-ab4b-e8f6ba240b7a | running |           1 |
    +-------------------+--------------------------------------+---------+-------------+

rst::

    =================  ====================================  =======  ===========
    Name               ID                                    State      CPU Count
    =================  ====================================  =======  ===========
    rhel5-buildserver  524dd016-5225-4b94-ab4b-e8f6ba240b7a  running            1
    =================  ====================================  =======  ===========

pretty::

    Name: rhel5-buildserver
    ID: 524dd016-5225-4b94-ab4b-e8f6ba240b7a
    State: running
    CPU Count: 1

mediawiki::

    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    ! Name              !! ID                                   !! State   !! align="right"|   CPU Count
    |-
    | rhel5-buildserver || 524dd016-5225-4b94-ab4b-e8f6ba240b7a || running || align="right"|           1
    |}

html::

    <table>
    <tr><th>Name             </th><th>ID                                  </th><th>State  </th><th style="text-align: right;">  CPU Count</th></tr>
    <tr><td>rhel5-buildserver</td><td>524dd016-5225-4b94-ab4b-e8f6ba240b7a</td><td>running</td><td style="text-align: right;">          1</td></tr>
    </table>

latex::

    \begin{tabular}{lllr}
    \hline
     Name              & ID                                   & State   &   CPU Count \\
    \hline
     rhel5-buildserver & 524dd016-5225-4b94-ab4b-e8f6ba240b7a & running &           1 \\
    \hline
    \end{tabular}

Queries
-------

Currently we have a very basic query syntax, it will improve over time.
Queries can be used on lists, and all sub-commands that support the --query parameter (most commands with list in them)

The syntax is homegrown and looks like  "<QueryParameter>:<Value>|<QueryParameter:<Value>"

Example of returning only ID and Name from server list, and only returning 5 entries::

    didata server list --query "ReturnKeys:ID,Name|ReturnCount:5"

Query Parameters
~~~~~~~~~~~~~~~~

ReturnKeys
++++++++++

Return keys will return only the keys you specify.

Here's an example of a server list command, where I don't care about any other keys besides the ID and Name of the server::

    didata server list --query "ReturnKeys:ID,Name"

The ReturnKeys parameter is ok with spaces, so if you want to query the status of Disk 0 on all of your boxes::

    didata server list --query "ReturnKeys:ID,Disk 0 State"

ReturnCount
+++++++++++

ReturnCount does exactly as you would expect, modifies the return count of the entries coming back.

Limiting your server responses to only 5 servers::

    didata server list --query "ReturnCount:5"
