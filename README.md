# Manual de instalación para el modulo "Product Fake API Integration"

### Modulos requeridos:

- Inventario (stock)
- Website (website)

![Inventario](./static/img/1.png)
![Website](./static/img/9.png)

### Instalando Modulo "Product Fake API Integration"

Vamos a:
**Home Menú => Aplicaciones**
Pegamos el nombre técnico del modulo a instalar en el buscador de aplicaciones y damos enter.

> product_fake_api_integration

![Imagen buscar modulo](./static/img/2.png)

Ahora, una vez identificado el modulo procedemos a instalarlo dando clic en Activar.
Una vez instalado se nos habilita en la sección de Ajustes Generales las opciones de Ajustes del modulo.

![Imagen ajustes modulo](./static/img/3.png)

Por defecto el modulo se instala pero hay que habilitarlo, para ello se debe habilitar el check "Usar Fake Store API".

![Imagen check ajustes modulo](./static/img/4.png)

Una vez habilitado la sincronización con la API nos la hará cada 24Hrs (1 día), podemos verificar el tarea programada en el menú técnico.

> Importar Productos desde Fake Store

![Imagen cron modulo](./static/img/5.png)

Podemos sincronizar los productos de forma inmediata con una opcion manual que tiene disponible, para ello vamos a darle permisos al usuario que va hacer la sincronización o importación de los productos.

![Imagen permiso modulo](./static/img/6.png)

Una vez habilitados los permisos estará disponible el menu

![Imagen menu modulo](./static/img/7.png)

![Imagen importación modulo](./static/img/8.png)

### Website para descargar archivo Excel con listado de productos

Ir a la siguiente url

> http://tudominio/web/export/products/page

Dar clic en el boton "Descargar Productos en Excel"

![website descarga](./static/img/10.png)
