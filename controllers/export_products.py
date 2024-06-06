from odoo import http
from odoo.http import request
import xlwt
import io


class ExportProductsController(http.Controller):

    @http.route("/export/products", type="http", auth="public")
    def export_products(self):
        """
        Exporta a un archivo Excel los productos que han sido importados o actualizados desde la API de Fake Store.
        """
        # Usar el superusuario para realizar la consulta de productos importados
        products = (
            request.env["product.template"]
            .sudo()
            .search([("imported_from_fake_store", "=", True)])
        )

        # Crear un libro de trabajo y una hoja
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Productos")

        # Definir el estilo para la cabecera
        header_style = xlwt.easyxf("font: bold 1")

        # Escribir las cabeceras
        headers = [
            "ID",
            "Nombre",
            "Precio",
            "Descripción",
            "Categoría",
            "Rating",
            "Rating Count",
            "Cantidad en Stock",
        ]
        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_style)

        # Escribir los datos de los productos
        for row, product in enumerate(products, start=1):
            sheet.write(row, 0, product.default_code)
            sheet.write(row, 1, product.name)
            sheet.write(row, 2, product.list_price)
            sheet.write(row, 3, product.description)
            sheet.write(row, 4, product.categ_id.name)
            sheet.write(row, 5, product.rating_rate)
            sheet.write(row, 6, product.rating_count)
            sheet.write(row, 7, product.qty_available)

        # Guardar el archivo en un buffer
        buffer = io.BytesIO()
        workbook.save(buffer)
        buffer.seek(0)

        # Crear una respuesta HTTP con el archivo Excel
        response = request.make_response(
            buffer.getvalue(),
            headers=[
                ("Content-Type", "application/vnd.ms-excel"),
                ("Content-Disposition", "attachment; filename=productos.xls;"),
            ],
        )
        return response

    @http.route("/web/export/products/page", type="http", auth="public", website=True)
    def export_products_page(self):
        """
        Renderiza la página web que contiene el botón para exportar los productos a un archivo Excel.
        """
        return request.render("product_fake_api_integration.export_products_page")
