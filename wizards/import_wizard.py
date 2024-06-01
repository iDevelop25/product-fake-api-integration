from odoo import models, fields, api
import requests
import base64


# La clase `ImportWizard` es un modelo transitorio en Python que se utiliza para operaciones de
# importación de productos.
class ImportWizard(models.TransientModel):
    _name = "product.import.wizard"
    _description = "Product Import Wizard"

    def import_products(self):
        """
        La función llama al método de importación de productos en el modelo product.template.
        """
        self.env["product.template"].import_products_from_fake_store()
