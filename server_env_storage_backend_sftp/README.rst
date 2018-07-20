
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================================
Storage Backend SFTP - Server Environment Configuration
=======================================================

This module is based on the ``server_environment`` module to use files or environment variable for
configuration.  Thus we can have a different configuration for each
environment (dev, test, staging, prod).  This module defines the config
variables for the ``storage_backend_sftp`` module.

Configuration and usage
=======================

In the configuration file, you can configure the server, port, login, password
of the storage backend.

Exemple of the section to put in the configuration file or environment
variable::

    [storage_backend.name_of_the_backend]
    directory_path = /demo
    sftp_server = sftp.example.com
    sftp_port = 22
    sftp_login = foo
    sftp_password = bar

Credits
=======

Contributors
------------

* Guewen Baconnier <guewen.baconnier@camptocamp.com>
