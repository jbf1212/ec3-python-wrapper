EPD Queries
==================

The EC3epds class can be used for simplifying queries of EPDs in the EC3 database.

The primary method currently setup for this class is the 'get_epds' method.
When using this the user should pass a dictionary of parameters and values for querying.

There are a large number of fields listed in the EC3 documentation that
can be used to query EPDs. Users should refer to that documentation
for the field names and values expected.

A small number of commonly used fields have been built into the class.
Refer to documentation below to see further details.

EC3epds
********

.. autoclass:: ec3.ec3_epds.EC3epds
    :members: