from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    """
    Esta clase hereda de res.config.settings para agregar opciones de configuración
    específicas para la integración con la API de Fake Store.
    """

    _inherit = "res.config.settings"

    # Definición de los campos para configurar el uso de la API de Fake Store
    use_fake_api = fields.Boolean("Use Fake Store API")
    fake_api_endpoint = fields.Char("Fake Store API Endpoint")

    @api.model
    def get_values(self):
        """
        Obtiene los valores actuales de los parámetros de configuración desde ir.config_parameter.
        """
        # Llamada al método get_values del modelo padre
        res = super(ResConfigSettings, self).get_values()
        # Actualización del diccionario con los valores específicos de los parámetros configurados
        res.update(
            use_fake_api=self.env["ir.config_parameter"]
            .sudo()
            .get_param("use_fake_api", default=False),
            fake_api_endpoint=self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "fake_api_endpoint", default="https://fakestoreapi.com/products"
            ),
        )
        return res

    def set_values(self):
        """
        Guarda los valores actualizados de los parámetros de configuración en ir.config_parameter.
        """
        # Llamada al método set_values del modelo padre
        super(ResConfigSettings, self).set_values()
        # Guardar los valores de configuración en ir.config_parameter
        self.env["ir.config_parameter"].sudo().set_param(
            "use_fake_api", self.use_fake_api
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "fake_api_endpoint", self.fake_api_endpoint
        )
