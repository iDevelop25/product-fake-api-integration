{
    "name": "Product Fake API Integration",
    "version": "1.0",
    "category": "Product",
    "summary": "Integration of products via Fake Store API",
    "description": "Module for integrating products from the Fake Store API into Odoo.",
    "author": "Johannes Moreno",
    "depends": ["base", "product"],
    "data": [
        # "data/product_data.xml",
        "security/product_security.xml",
        "security/ir.model.access.csv",
        "data/product_cron.xml",
        "views/product_views.xml",
        "views/import_wizard_views.xml",
        "views/product_menu.xml",
    ],
    "installable": True,
    "application": True,
}
