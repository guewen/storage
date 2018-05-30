# Copyright 2017 Akretion (http://www.akretion.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import os
import errno

from contextlib import contextmanager
from odoo.addons.component.core import Component


logger = logging.getLogger(__name__)

try:
    import paramiko
except ImportError as err:
    logger.debug(err)


def sftp_mkdirs(client, path, mode=511):
    try:
        client.mkdir(path, mode)
    except IOError as e:
        if e.errno == errno.ENOENT and path:
            sftp_mkdirs(client, os.path.dirname(path), mode=mode)
            client.mkdir(path, mode)
        else:
            raise


@contextmanager
def sftp(backend):
    account = backend._get_keychain_account()
    password = account.get_password()
    transport = paramiko.Transport((backend.sftp_server, backend.sftp_port))
    transport.connect(username=backend.sftp_login, password=password)
    client = paramiko.SFTPClient.from_transport(transport)
    yield client
    transport.close()


class SftpStorageBackend(Component):
    _name = 'sftp.adapter'
    _inherit = 'base.storage.adapter'
    _usage = 'sftp'

    def add(self, relative_path, data, **kwargs):
        with sftp(self.collection) as client:
            full_path = self._fullpath(relative_path)
            dirname = os.path.dirname(full_path)
            if dirname:
                try:
                    client.stat(dirname)
                except IOError as e:
                    if e.errno == errno.ENOENT:
                        sftp_mkdirs(client, dirname)
                    else:
                        raise
            remote_file = client.open(full_path, 'w+b')
            remote_file.write(data)
            remote_file.close()

    def get(self, relative_path, **kwargs):
        full_path = self._fullpath(relative_path)
        with sftp(self.collection) as client:
            file_data = client.open(full_path, 'rb')
            data = file_data.read()
        return data

    def list(self, relative_path):
        full_path = self._fullpath(relative_path)
        with sftp(self.collection) as client:
            try:
                return client.listdir(full_path)
            except IOError as e:
                if e.errno == errno.ENOENT:
                    # The path do not exist return an empty list
                    return []
                else:
                    raise

    def delete(self, relative_path):
        full_path = self._fullpath(relative_path)
        with sftp(self.collection) as client:
            return client.remove(full_path)
