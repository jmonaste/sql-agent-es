# Proyecto SQL Agent

## Descripción del Proyecto

Este es un proyecto SQL Agent desarrollado con Node.js. La aplicación funciona como un agente inteligente para operaciones y consultas en bases de datos SQL.

## Idioma del proyecto.

Este proyecto se realizará enteramente en español

## Estructura del Proyecto

- `src/` - Código fuente  
- `tests/` - Archivos de pruebas  
- `docs/` - Documentación  
- `package.json` - Configuración del proyecto Node.js


## Instrucciones de instalación de base de datos
La base de datos SAKILA está completamente configurada en español y lista para usar con Docker.

**Fuentes de la base de datos en español:**
- Esquema: https://gist.github.com/josejuansanchez/b44d3d1f84800eb07e188958e99de9bc
- Datos: https://gist.github.com/josejuansanchez/122675071cdacce7f7ba61051707dae3

**Tablas principales de la base de datos (en español):**
- `actor` - Actores de las películas
- `direccion` - Direcciones
- `categoria` - Categorías de películas
- `ciudad` - Ciudades
- `pais` - Países
- `cliente` - Clientes del negocio
- `pelicula` - Películas disponibles
- `inventario` - Inventario de películas
- `alquiler` - Registros de alquileres
- `pago` - Registros de pagos

La base de datos incluye también vistas, procedimientos almacenados, funciones y triggers para operaciones avanzadas.

## Configuración Docker completada
La base de datos está completamente configurada con Docker. Ver README.md para instrucciones de uso.

**Archivos de configuración:**
- `docker-compose.yml` - Configuración del contenedor MySQL
- `database/init.sql` - Script de inicialización automática
- `database/sakila-schema-spanish.sql` - Esquema de la base de datos en español
- `database/sakila-data-spanish.sql` - Datos de la base de datos en español

**Uso:**
```bash
docker-compose up -d    # Levantar la base de datos (puerto 3307)
docker-compose down     # Detener la base de datos
```

**Información de conexión:**
- Host: localhost
- Puerto: 3307
- Base de datos: sakila
- Usuario: root
- Contraseña: sakila_password