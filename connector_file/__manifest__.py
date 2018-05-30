# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Connector File",
    "summary": "Allows user to define a file backend",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "category": "Storage",
    "website": "https://github.com/akretion/storage",
    "depends": [
        "storage_backend_sftp",
        "connector"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/connector_file_views.xml",
    ],
    "installable": True,
}
