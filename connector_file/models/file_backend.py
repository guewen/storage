# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models, _
from odoo.exceptions import Warning


logger = logging.getLogger(__name__)

try:
    import paramiko
except ImportError as err:
    logger.debug(err)


class FileBackend(models.Model):
    _name = 'file.backend'
    _inherit = ['mail.thread']
    _description = 'File Backend'

    name = fields.Char(string='Name', required=True)
    storage_backend_id = fields.Many2one(
        comodel_name='storage.backend',
        string='Storage Backend',
        required=True,
    )

    def _get_stfp_connection(self, backend):
        try:
            account = backend._get_keychain_account()
            password = account.get_password()
            transport = paramiko.Transport(
                (backend.sftp_server, backend.sftp_port))
            transport.connect(username=backend.sftp_login, password=password)
        except Exception as e:
            raise Warning(_('Exception details\n\n%s' % e))
        return transport

    def _close_stfp_connection(self, transport):
        try:
            transport.close()
        except Exception as e:
            raise Warning(_('Exception details\n\n%s' % e))
        return

    @api.multi
    def sftp_connnection_test(self):
        self.ensure_one()
        backend = self.storage_backend_id
        try:
            transport = self._get_stfp_connection(backend)
            self._close_stfp_connection(transport)
        except Exception as e:
            raise Warning(_('Exception details\n\n%s' % e))
        raise Warning(_('Test connection successfully.'))
