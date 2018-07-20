# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StorageBackend(models.Model):
    _inherit = "storage.backend"

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        sftp_fields = {
            "sftp_server": {},
            "sftp_port": {'getter': "getint"},
            "sftp_login": {},
            "sftp_password": {
                # integration with keychain, the 'default' field
                # is forwarded to keychain's compute/inverse
                "no_default_field": True,
                "compute_default": "_compute_password",
                "inverse_default": "_inverse_password",
            },
        }
        sftp_fields.update(base_fields)
        return sftp_fields
