# Copyright 2017 Akretion (http://www.akretion.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)
try:
    import paramiko
except ImportError as err:
    logger.error(err)


class StorageBackend(models.Model):
    _inherit = 'storage.backend'

    backend_type = fields.Selection(
        selection_add=[('sftp', 'SFTP')])
    sftp_password = fields.Char(
        related="password",
        string="Password")
    sftp_login = fields.Char(
        string='Login',
        help='Login to connect to sftp server',
        sparse="data")
    sftp_server = fields.Char(
        string='Host',
        sparse="data")
    sftp_port = fields.Integer(
        string='Port',
        default=22,
        sparse="data")

    def _get_stfp_connection(self):
        try:
            account = self._get_keychain_account()
            password = account.get_password()
            transport = paramiko.Transport(
                    (self.sftp_server, self.sftp_port))
            transport.connect(username=self.sftp_login, password=password)
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
    def connnection_test(self):
        self.ensure_one()
        try:
            transport = self._get_stfp_connection()
            self._close_stfp_connection(transport)
        except Exception as e:
            raise Warning(_('Exception details\n\n%s' % e))
        # Not a user error but a quick way to send feedback
        raise UserError(_('Test connection successful.'))
