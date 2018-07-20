# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

try:
    from odoo.addons.server_environment import serv_config
except ImportError:
    logging.getLogger("odoo.module").warning(
        "server_environment not available in addons path. "
        "server_env_storage_backend_sftp will not be usable"
    )


class StorageBackend(models.Model):
    _name = "storage.backend"
    _inherit = ["storage.backend", "server.env.mixin"]

    @property
    def _server_env_fields(self):
        return {"directory_path": {}}
