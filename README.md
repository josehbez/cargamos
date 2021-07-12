<p align="center">
    <a href="LICENSE">
        <img src="https://img.shields.io/github/license/josehbez/cargamos?style=flat-square" />
    </a>
    <a href=".pm/version.yml">
        <img src="https://img.shields.io/badge/dynamic/yaml?color=green&label=version&query=version.*&url=https://raw.githubusercontent.com/josehbez/cargamos/master/.pm/version.yml"/>
    </a>
    <a href=".pm/version.yml">
        <img src="https://img.shields.io/badge/dynamic/yaml?color=green&label=prerelease&query=prerelease.*&url=https://raw.githubusercontent.com/josehbez/cargamos/master/.pm/version.yml"/>
    </a href="#">
        <img src="https://github.com/josehbez/cargamos/workflows/Build%20and%20Deploy/badge.svg"/>
    <a>
</a>
</p>

# Cargamos

Simple gestor de inventario desarrollado sobre FLASK, FLASK-RESTFUL, FLASK-SQLALCHEMY, 

## Tabla de contenido

* Instalación
* Diseño DB
* Diseño RESTful
  * Url demo
  * Documentacion en Postman
  * Demo en Postman
* Tests

## Instalación

```bash
# Configuración definido por: APP_SETTINGS
# Puede tener los siguientes valores: dev | test | production
# El archivo config.json debe ser colocado en deployments/${APP_SETTINGS}/config.json
#
# Variables importantes del archivo config.json
#
# SQLALCHEMY_DATABASE_URI - Conector base dedatos
# e.g: postgresql://USERNAME:PASSWORD@HOST/DBNAME 
# e.g: sqlite:///../storage/cargamos.db
#
# SECRET_KEY - Llave de la configuración
# e.g: \\x83\\xb8\\xf0\\x9e%\\x1f\\xd9\\xf2\\xf6\\x8b\\x04"\\x886Pjz\\x9f2M


################## pipenv ##################
# Copiar plantilla deployments/testing/config.json
# Pegar el archivo en deployments/dev/config.json

pipenv shell
pip install -r requirements.txt
export APP_SETTINGS=dev
python manage.py db upgrade
python run.py

################## docker-compose ##################
# Revisar plantilla deployments/production/config.json

export APP_SETTINGS=production
docker-compose up --build -d
docker container  exec -t cargamos python manage.py db upgrade

################## Puerto 8844 ##################
* Serving Flask app "app" (lazy loading)
* Running on http://0.0.0.0:8844/ (Press CTRL+C to quit)
```

## Diseño DB

```bash
Todas las tablas heredan de una clase abstracta y tienen los siguientes campos:
1.- name - Nombre del movimiento, transaccion ó usuario
2.- id - Identificador del registro
3.- date_created - Fecha de creación del registro
4.- date_modified - Fecha de la ultima modificación del registro

Tablas:

1.- USERS - Se utiliza para el manejo de autenticaciones
	* email - Correo del usuario
	* password - Contraseña encriptada el usuario
	* token - Token de authorización para peticiones HTTP

2.- WAREHOUSE - Se utiliza para registrar almacenes (tiendas)
	* address - Dirección del almacén

3.- PRODUCT - Se utiliza para registrar productos
	* sku - unidad de mantenimiento en almacén del producto

4.- STOCK_MOVE - Se utiliza para registrar movimientos de almacén
	* type - Tipo de movimiento entrda (in) o salida (out)
	* qty - Cantidad de movmiento
	* product_id - ID del producto 
	* warahouse_id - ID del almacén

Vistas(consultas):
	
1.- STOCK - manejo de existencias
	* qry - Cantidad de existencias 
	* product_id - ID del producto
	* warehouser - ID del almacén


Ejemplo:

-------------------users------------------
| id | name | email   | password | token |
| 1  | jose | j@j.com | sha256   | j.w.t |

------warehouse--------
| id | name | address | 
| 1  | WH1  | GDL     |
| 2  | WH2  | CDMX    |

--------product------
| id | name   | sku | 
| 1  | iPhone | I2  | 
| 1  | iPad   | I6  |

----------------------stock_move----------------------
| id | type | qty | name | product_id | warehouse_id | 
| 1  | in   | 93  | PO/1 | 1          | 1            |
| 1  | out  | 3   | SO/2 | 1          | 1            |
| 1  | in   | 20  | PO/3 | 2          | 2            |

---------------stock--------------
| qty | product_id | warehouse_id |
| 90  | 1          | 1            |
| 20  | 2          | 2            |


```

## Diseño RESTful

### URL

http://demo.josehbez.com

### Documentación

https://documenter.getpostman.com/view/5247124/TzCFfqC8

### Demo

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/ca919d4646123590d6ea#?env%5BStaging%5D=W3sia2V5IjoiVVJMIiwidmFsdWUiOiJodHRwOi8vZGVtby5qb3NlaGJlei5jb20iLCJlbmFibGVkIjp0cnVlfSx7ImtleSI6IlVTRVJfTkFNRSIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZX0seyJrZXkiOiJVU0VSX0VNQUlMIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlfSx7ImtleSI6IlVTRVJfUEFTU1dPUkQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWV9LHsia2V5IjoiVE9LRU4iLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWV9LHsia2V5IjoiV0hfTkFNRSIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZX0seyJrZXkiOiJXSF9BRERSRVNTIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlfSx7ImtleSI6IlBST0RVQ1RfTkFNRSIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZX0seyJrZXkiOiJQUk9EVUNUX1NLVSIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZX1d)



```bash
# Auth:

POST /v1/auth/register HTTP/1.1
POST /v1/auth/login HTTP/1.1

# Warehouse
POST /v1/warehouse HTTP/1.1
PUT /v1/warehouse/{{WH_ID}} HTTP/1.1
GET /v1/warehouse HTTP/1.1
DELETE /v1/warehouse/{{WH_ID}} HTTP/1.1

# Product
POST /v1/product HTTP/1.1
PUT /v1/product/{{PRODUCT_ID}} HTTP/1.1
GET /v1/product HTTP/1.1
DELETE /v1/product/{{PRODUCT_ID}} HTTP/1.1

# Stock Move
POST /v1/purchase HTTP/1.1
POST /v1/sale HTTP/1.1

# Stock 
GET /v1/stock HTTP/1.1
GET /v1/stock/product/{{PRODUCT_ID}} HTTP/1.1
GET /v1/stock/warehouse/{{WH_ID}} HTTP/1.1
GET /v1/stock/{{PRODUCT_ID}}/{{WH_ID}} HTTP/1.1

```

## Tests

```bash
export APP_SETTINGS=test
python test.py
```