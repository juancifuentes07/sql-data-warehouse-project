Data Catalog — Capa Gold
Visión general

La capa Gold es la capa de consumo del datawarehouse, diseñada bajo un modelo dimensional (esquema estrella) compuesto por tablas de dimensión y una tabla de hechos. Todos los objetos de esta capa son vistas (VIEW), que combinan y transforman datos ya limpios provenientes de la capa Silver.

Objeto	Tipo	Descripción
gold.dim_customer	Dimensión	Información de clientes, combinando datos del CRM y del ERP
gold.dim_products	Dimensión	Información de productos vigentes, combinando datos del CRM y del ERP
gold.fact_sales	Hechos	Transacciones de venta, conectadas a las dimensiones de cliente y producto
gold.dim_customer

Dimensión de clientes. Combina información maestra del CRM con datos complementarios del ERP (género de respaldo, fecha de nacimiento, país).

Fuentes: silver.crm_cust_info, silver.erp_cust_az12, silver.erp_loc_a101

Columna	Tipo	Descripción
customer_key	INT	Clave subrogada. Identificador único generado por el datawarehouse (ROW_NUMBER()), usado para relacionar con la tabla de hechos
customer_id	INT	Identificador del cliente en el sistema fuente CRM (cst_id)
customer_number	VARCHAR(50)	Número/código de cliente del CRM (cst_key), usado para cruzar con el ERP
first_name	VARCHAR(50)	Nombre del cliente
last_name	VARCHAR(50)	Apellido del cliente
country	VARCHAR(50)	País de residencia. Fuente: ERP (erp_loc_a101)
marital_status	VARCHAR(50)	Estado civil estandarizado: Single, Married, n/a
gender	VARCHAR(50)	Género estandarizado: Male, Female, n/a. El CRM es la fuente maestra; si el CRM no tiene el dato (n/a), se usa el valor del ERP como respaldo
birthdate	DATE	Fecha de nacimiento. Fuente: ERP (erp_cust_az12). Fechas futuras inválidas fueron descartadas en Silver
create_date	DATE	Fecha de creación del registro de cliente en el sistema CRM
gold.dim_products

Dimensión de productos actualmente vigentes. Excluye versiones históricas de un mismo producto (solo se incluyen aquellos cuyo prd_end_dt es NULL, es decir, la versión activa más reciente).

Fuentes: silver.crm_prd_info, silver.erp_px_cat_g1v2

Columna	Tipo	Descripción
product_key	INT	Clave subrogada. Identificador único generado por el datawarehouse (ROW_NUMBER()), usado para relacionar con la tabla de hechos
product_id	INT	Identificador del producto en el sistema fuente CRM (prd_id)
product_number	VARCHAR(50)	Código del producto (prd_key), sin el prefijo de categoría
product_name	VARCHAR(50)	Nombre del producto
category_id	VARCHAR(50)	Identificador de categoría, extraído del prd_key original
category	VARCHAR(50)	Categoría del producto. Fuente: ERP (erp_px_cat_g1v2)
subcategory	VARCHAR(50)	Subcategoría del producto. Fuente: ERP
maintenance	VARCHAR(50)	Indicador de mantenimiento del producto. Fuente: ERP
cost	INT	Costo del producto. Valores nulos se estandarizaron a 0 en Silver
product_line	VARCHAR(50)	Línea de producto estandarizada: Mountain, Road, Other Sales, Touring, n/a
start_date	DATE	Fecha desde la cual esta versión del producto está vigente
gold.fact_sales

Tabla de hechos con el detalle de cada línea de venta, conectada a dim_customer y dim_products mediante sus claves subrogadas.

Fuentes: silver.crm_sales_details, gold.dim_products, gold.dim_customer

Columna	Tipo	Descripción
order_number	VARCHAR(50)	Número de orden de venta
product_key	INT	Clave subrogada del producto (FK → gold.dim_products.product_key)
customer_key	INT	Clave subrogada del cliente (FK → gold.dim_customer.customer_key)
order_date	DATE	Fecha en que se realizó el pedido. Nulo si el dato de origen era inválido
shipping_date	DATE	Fecha de envío. Nulo si el dato de origen era inválido
due_date	DATE	Fecha de vencimiento/entrega esperada. Nulo si el dato de origen era inválido
sales_amount	INT	Monto total de la venta. Recalculado en Silver como quantity * ABS(price) cuando el valor original era inconsistente o inválido
quantity	INT	Cantidad de unidades vendidas
price	INT	Precio unitario. Recalculado en Silver como sales_amount / quantity cuando el valor original era inválido o nulo
Notas de arquitectura
Modelo: esquema estrella, con fact_sales como tabla de hechos y dim_customer / dim_products como dimensiones.
Claves subrogadas: generadas en la capa Gold mediante ROW_NUMBER(), desacoplando el modelo de los identificadores originales de los sistemas fuente (CRM/ERP).
Capa Gold = vistas, no tablas físicas: se consulta en tiempo real sobre Silver, sin duplicar almacenamiento.
Fuente maestra por atributo: cuando un mismo dato existe en más de un sistema fuente (ej. género del cliente), se define explícitamente cuál sistema es la fuente de verdad y cuál es el respaldo.
