from odoo import models, fields, api
from odoo.exceptions import UserError
import requests
import base64


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Definir los nuevos campos para el rating
    rating_rate = fields.Float(string="Rating Rate")
    rating_count = fields.Integer(string="Rating Count")

    @api.model
    def import_products_from_fake_store(self, *args, **kwargs):
        # Obtener el parámetro de configuración para habilitar o deshabilitar el uso de la API de Fake Store
        use_fake_api = self.env["ir.config_parameter"].sudo().get_param("use_fake_api")
        # Obtener el endpoint de la API de Fake Store desde los parámetros de configuración
        fake_api_endpoint = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("fake_api_endpoint", default="https://fakestoreapi.com/products")
        )

        # Si la API está deshabilitada, se lanza un error
        if not use_fake_api:
            raise UserError(
                "Error al obtener productos de la API de Fake Store. "
                "Habilite la integración con la API de Fake Store en la configuración."
            )

        # Realizar la solicitud GET a la API de Fake Store
        response = requests.get(fake_api_endpoint)
        if response.status_code == 200:
            products = response.json()
            for product in products:
                existing_product = self.search(
                    [("default_code", "=", str(product["id"]))], limit=1
                )
                image_data = self._get_image_from_url(product["image"])
                product_data = {
                    "name": product["title"],
                    "list_price": product["price"],
                    "type": "product",
                    "default_code": str(product["id"]),
                    "description": product["description"],
                    "image_1920": image_data,
                    "categ_id": self._get_category_id(product["category"]),
                    "rating_rate": product["rating"]["rate"],
                    "rating_count": product["rating"]["count"],
                }
                if existing_product:
                    existing_product.write(product_data)
                else:
                    self.create(product_data)
        else:
            raise UserError("Error al obtener productos de la API de Fake Store.")

    def _get_image_from_url(self, url):
        # Realizar una solicitud GET para obtener la imagen desde la URL proporcionada
        response = requests.get(url)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode("utf-8")
        else:
            return False

    def _get_category_id(self, category_name):
        # Buscar una categoría existente con el nombre proporcionado
        category = self.env["product.category"].search(
            [("name", "=", category_name)], limit=1
        )
        if category:
            return category.id
        else:
            # Si la categoría no existe, se crea una nueva
            return self.env["product.category"].create({"name": category_name}).id
