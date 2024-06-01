from odoo import models, fields, api


# Esta clase extiende el modelo "res.config.settings" en Odoo.
class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    use_fake_api = fields.Boolean("Use Fake Store API")

    @api.model
    def get_values(self):
        """
        La función `get_values` recupera valores de configuración, incluido un parámetro para usar una
        API falsa, actualizando los valores obtenidos de la clase principal.
        :return: Un diccionario que contiene los valores de la clase principal `ResConfigSettings` junto
        con el valor del parámetro `use_fake_api` recuperado de los parámetros de configuración.
        """
        res = super(ResConfigSettings, self).get_values()
        res.update(
            use_fake_api=self.env["ir.config_parameter"]
            .sudo()
            .get_param("use_fake_api", default=False)
        )
        return res

    def set_values(self):
        """
        La función `set_values` establece el valor del parámetro de configuración "use_fake_api" en el
        entorno.
        """
        super(ResConfigSettings, self).set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "use_fake_api", self.use_fake_api
        )
