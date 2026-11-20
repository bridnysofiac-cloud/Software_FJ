# Software FJ
## Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto académico desarrollado en Python para el curso Programación (213023), Fase 4.

### Objetivo
Construir una aplicación orientada a objetos para gestionar clientes, servicios y reservas, con validaciones, manejo de excepciones y registro de eventos y errores.

### Requisitos
- Python 3.10 o superior.
- No requiere instalar librerías externas.

### Archivos
- `main.py`: menú principal y demostración de operaciones.
- `entidades.py`: clase abstracta Entidad.
- `clientes.py`: clase Cliente y validaciones.
- `servicios.py`: clase abstracta Servicio y tres servicios especializados.
- `reservas.py`: gestión de reservas y estados.
- `excepciones.py`: excepciones personalizadas.
- `logs.py`: configuración de registro.
- `sistema.py`: administración de listas internas.
- `registro_sistema.log`: se crea automáticamente al ejecutar el programa.

### Ejecución
Desde la terminal, dentro de esta carpeta:

```bash
python main.py
```

Para ejecutar automáticamente la demostración:

```bash
python main.py demo
```

En Windows también puede utilizarse:

```bash
py main.py
py main.py demo
```

### Funcionalidades
- Registro y consulta de clientes.
- Registro y consulta de servicios.
- Creación, confirmación, cancelación y procesamiento de reservas.
- Validación de datos.
- Herencia, abstracción, encapsulación y polimorfismo.
- Cálculos con parámetros opcionales para impuesto y descuento.
- Excepciones personalizadas y encadenamiento.
- Registro de eventos y errores en archivo LOG.
- Demostración de más de diez operaciones.

### Consideraciones
La información de clientes, servicios y reservas se mantiene en listas en memoria durante la ejecución. No se utiliza una base de datos. El archivo LOG registra eventos y errores; no sustituye una base de datos ni almacena el inventario completo.
