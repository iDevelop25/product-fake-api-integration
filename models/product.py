from odoo import models, fields, api
from odoo.exceptions import UserError
import requests
import base64


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def import_products_from_fake_store(self, *args, **kwargs):
        use_fake_api = self.env["ir.config_parameter"].sudo().get_param("use_fake_api")
        fake_api_endpoint = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("fake_api_endpoint", default="https://fakestoreapi.com/products")
        )

        if not use_fake_api:
            raise UserError(
                "Error al obtener productos de la API de Fake Store. "
                "Habilite la integración con la API de Fake Store en la configuración."
            )

        response = requests.get(fake_api_endpoint)
        if response.status_code == 200:
            products = response.json()
            for product in products:
                existing_product = self.search(
                    [("default_code", "=", product["id"])], limit=1
                )
                image_data = self._get_image_from_url(product["image"])
                product_data = {
                    "name": product["title"],
                    "list_price": product["price"],
                    "type": "product",
                    "default_code": product["id"],
                    "description": product["description"],
                    "image_1920": image_data,
                }
                if existing_product:
                    existing_product.write(product_data)
                else:
                    self.create(product_data)
        else:
            raise UserError("Error al obtener productos de la API de Fake Store.")

    def _get_image_from_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode("utf-8")
        else:
            return False
