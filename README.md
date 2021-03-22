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

RESTfull manejo de compras, ventas e inventario.

## Tabla de contenido

* Instalación
* Diseño DB
* Diseño RESTfull
* Demo
* Tests

## Instalación

```bash
# Configuraciones definidos por:
# APP_SETTINGS dev | test | production

## Por pipenv
## Revisar plantilla deployments/testing/config.json
pipenv shell 
pip install -r requirements.txt
export APP_SETTINGS=dev
python manage.py db upgrade
python run.py

## Por docker-compose
## Revisar plantilla deployments/production/config.json
export APP_SETTINGS=production
docker-compose up --build -d
docker container  exec -t cargamos python manage.py db upgrade

## Puerto 8844
* Serving Flask app "app" (lazy loading)
* Running on http://0.0.0.0:8844/ (Press CTRL+C to quit)
```

## Diseño DB

```bash
Todas heredan de una clase abastracta y tienen los siguientes campos:
1.- name - Nombre del movimiento, transaccion ó usuario
2.- id - Identificador del registro
3.- date_created - Fecha de creacion del registro
4.- date_modified - Fecha de la ultima modificacion del registro

Tablas:

1.- USERS - Se utiliza para el manejo autenticaciones
	* email - Correo del usuario 
	* password - Contraseña encriptada el usuario
	* token - Token authorizacion para peticiones HTTP

2.- WAREHOUSE - Se utiliza para registrar almacenes (tiendas)
	* address - Direccion del alamcen

3.- PRODUCT - Se utiliza para registra productos
	* sku - unidad de mantenimiento en almacen del producto

4.- STOCK_MOVE - Se utiliza para registrar movimientos de alamcen
	* type - Tipo de movimiento entrda (in) o salida (out)
	* qty - Cantidad de movmiento
	* product_id - ID del producto 
	* warahouse_id - ID del almacen

Vistas(consultas):
	
1.- STOCK - manejo de existencias
	* qry - Cantidad de existencias 
	* product_id - ID del producto
	* warehouser - ID del almacen


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

## Diseño RESTfull

```bash

```



## Demo

RESTfull demo http://demo.josehbez.com

## Tests

```bash
export APP_SETTINGS=test
python test.py
```

