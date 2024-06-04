from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    use_fake_api = fields.Boolean("Use Fake Store API")
    fake_api_endpoint = fields.Char("Fake Store API Endpoint")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
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
        super(ResConfigSettings, self).set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "use_fake_api", self.use_fake_api
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "fake_api_endpoint", self.fake_api_endpoint
        )
