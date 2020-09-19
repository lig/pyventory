A New Feel for Ansible Inventory
================================

`Pyventory` is a tricky twist in thinking about the way to create and maintain Ansible
inventory. It brings the power of OOP into play to defend from some common errors like
undefined variables and to help keep the inventory in line with the DRY principle.


Installation
============

It is usually enough to install `Pyventory` into the same Python environment as you have
Ansible installed into. The command below should make it happen in most cases.

.. code-block:: shell

   pip3 install pyventory


If the above doesn't work for you, read :doc:`/guide/installation`.


Contents
========

.. toctree::
   :maxdepth: 2

   tutorial/index
   guide/index
   how-tos/index


Contributing
============

We welcome any help including but not limited to bug reports, feature requests,
translations, documentation improvements, packaging. It could be anything you think
could help you and others to use or to improve the project.

Use `our GitHub page`_. Be sure to review the `contributing guidelines`_ and `code of conduct`_.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _`our GitHub page`: https://github.com/lig/pyventory
.. _`code of conduct`: https://github.com/lig/pyventory/blob/main/CODE_OF_CONDUCT.md
.. _`contributing guidelines`: https://github.com/lig/pyventory/blob/main/CONTRIBUTING.md
