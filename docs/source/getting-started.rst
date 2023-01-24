Getting Started
======================================

Installation
************

To use ec3-python-wrapper, first install it using pip:

.. code-block:: console

   $ pip install ec3-python-wrapper


Authentication
**************

Usage of the EC3 Python Wrapper assumes you have obtained a bearer token from Building Transparency.
To obtain your token `follow the instructions found here <https://buildingtransparency.org/ec3/manage-apps/api-doc/guide#/01_Overview/01_Introduction.md>`_

Your token should be securely stored.
A common way to do this, is to `store it as an environment variable <https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html>`_,
and load it using ``os.environ``:

.. code-block:: python

    import os
    api_key = os.environ["EC3_KEY"]


Quickstart
**********

The following is a simple example of querying for a list of materials.
Refer to the `Building Transparency API documentation <https://buildingtransparency.org/ec3/manage-apps/api-doc/api#/>`_ for valid fields to search.

.. code-block:: python

    >>> import os
    >>> from ec3 import EC3Materials
    >>> token = os.environ['EC3_KEY']
    >>> ec3_materials = EC3Materials(bearer_token=token, ssl_verify=False)
    >>> mat_param_dict = {"lightweight":True, "concrete_compressive_strength_at_28d__target":"5000 psi", "jurisdiction":"US"}
    >>> ec3_materials.return_fields = ["id", "concrete_compressive_strength_28d", "gwp"]
    >>> mat_records = ec3_materials.get_materials(return_all=True, params=mat_param_dict)


Examples
**********

Some Jupyter Notebook examples can be found over in the github repository:
`Overview example <https://github.com/jbf1212/ec3-python-wrapper/blob/master/ec3_overview.ipynb>`_
`Material plotting example <https://github.com/jbf1212/ec3-python-wrapper/blob/master/ec3_materials_plot.ipynb>`_