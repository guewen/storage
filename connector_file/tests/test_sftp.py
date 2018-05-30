# Copyright 2018 Open Source Integrators
#   (http://www.opensourceintegrators.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo.tests import common
import os
import logging
_logger = logging.getLogger(__name__)


class FileBackendSftpCase(common.TransactionCase):

    def setUp(self):
        super(FileBackendSftpCase, self).setUp()
        # storage backend and file backend records
        self.backend = self._create_backend()
        self.file_backend = self._create_file_backend()

    def _create_backend(self):
        return self.env['storage.backend'].create({
            'name': 'SFTP Backend',
            'backend_type': 'sftp',
            'sftp_login': 'foo',
            'sftp_password': 'pass',
            'sftp_server': os.environ.get('SFTP_HOST', 'localhost'),
            'sftp_port': os.environ.get('SFTP_PORT', '2222'),
            'directory_path': 'upload',
        })

    def _create_file_backend(self):
        return self.env['file.backend'].create({
            'name': 'SFTP File Backend',
            'storage_backend_id': self.backend.id,
        })
