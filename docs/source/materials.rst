Material Queries
==================
The EC3Materials class is meant to simplify the querying of materials from the EC3 database

The primary method currently setup for this class is the 'get_materials' method.
When using this the user should pass a dictionary of parameters and values for querying.

There are a large number of fields listed in the EC3 documentation that
can be used to query materials. Users should refer to that documentation
for the field names and values expected.

A small number of commonly used fields have been built into the class.
Refer to documentation below to see further details.

EC3Materials
************

.. autoclass:: ec3.ec3_materials.EC3Materials
    :members: