from odoo import models, fields, api
from odoo.exceptions import UserError
import requests
import base64


# Esta clase amplía la funcionalidad del modelo "product.template".
class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def import_products_from_fake_store(self, *args, **kwargs):
        """
        La función `import_products_from_fake_store` recupera productos de la API de Fake Store y los
        crea o actualiza en el sistema en función de los datos recuperados.
        """
        use_fake_api = self.env["ir.config_parameter"].sudo().get_param("use_fake_api")
        if not use_fake_api:
            raise UserError(
                "Error al obtener productos de la API de Fake Store. "
                "Habilite la integración con la API de Fake Store en los Ajustes Generales."
            )

        response = requests.get("https://fakestoreapi.com/products")
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
            raise Exception("Failed to fetch products from Fake Store API")

    def _get_image_from_url(self, url):
        """
        Esta función recupera una imagen de una URL determinada y la codifica en formato base64 si el
        código de estado de respuesta es 200.

        El parámetro `url` en la función `_get_image_from_url` es una cadena que representa
        la URL desde la cual se debe obtener una imagen. La función utiliza el método `requests.get`
        para realizar una solicitud GET a esta URL y luego codifica el contenido de la respuesta en
        formato base64
        :return: Si el código de estado de la respuesta es 200, la función devolverá el contenido
        codificado en base64 de la respuesta como una cadena decodificada en UTF-8. Si el código de
        estado de respuesta no es 200, la función devolverá Falso.
        """
        response = requests.get(url)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode("utf-8")
        else:
            return False
