# Catalogo_online
# Indicaciones de ejecución
> Instala [Python](https://www.python.org/downloads/) en tu equipo si es que no lo tienes.
>
> Descarga los archivos del repositorio en [Git Hub](https://github.com/JesusVillanuevaRo/Catalogo_online.git)

>* Para S.O. Windows
>   1. Opcion 1: Activar en un sólo click con uso del ambiente virtual.
>       * entra en la carpeta donde se encuentran los archivos, y ejecuta el archivo **ejecutor.bat** lo que activara el ambiente virtual (virtualenv) y pondrá el servidor en ejecución
>       * La ejecución se realiza en **localhost**, abre tu navegador y en el buscador de direcciones coloca **localhost**
>   2. Opción 2: Instalar requerimientos en tu equipo
>       * Preciona  **win+r** escribe **cmd** y presiona enter para abrir el símbolo del sistema.
>       * Una vez dentro coloca el siguiente código para instalar los requerimientos en tu ordenador **pip install -r rquirements.txt**, de esta manera no tendrás que activar el ambiente virtual para ejecutar el servidor.
>       *Al terminar la descarga e instalación de los modulos cierra el símbolo del sistema y ejecuta el archivo **app.py** de la carpeta de archivos

>* Para S.O. Linux
>   1. Opción 1: activa el ambiente virtual (la carpeta del ambiente virtual se llama **virtualenv**) y posteriormente ejecuta el archivo app.py
>   2. Opción 2: Instala los requerimientos que se encuentran en el archivo **requirements.txt** en tu ordenador, despues ejecuta el archivo app.py

# Documentación
VillanuevaRodea Jesús Alberto - Desarrollador WEB

## Herramientas de desarrollo
> ## MongoDB Atlas
>>Servidor en la nube para bases de datos no relacionales, implementado con la finalidad de que esté siempre disponible y no exista la necesidad
>>
>>de instalar un gestor de base de datos en el equipo que ejecute el servidor backend.
>
> ## Flask
>>Framework backend que usa Python como lenguaje de programación, que
permite la creación eficiente de servidores con ayuda de la gran
>>
>>cantidad de módulos que pueden implementarse para mejorar su funcionamiento, entre los cuales se utiliza **pymongo** para realizar
>>
>>las conexiones con la base de datos, **bcrypt** para encriptar las contraseñas de los usuarios registrados y al iniciar sesión, entre otros.
>>
>>En el archivo **requirements.txt** que se encuentra en el repositorio de  [Git Hub](https://github.com/JesusVillanuevaRo/Catalogo_online.git) puede
encontrar los módulos utilizados y su respectiva version.
>
> ## HTML
>>Utilizado para renderizar las paginas que se presentan al publico general y a los usuarios de la aplicación, lenguaje con el que se crean
>>
>>los formularios y las pantallas correspondientes, según indíque el backend, con ayuda de las siguientes herramientas.
>
> ## CSS y Bootstrap
>>Hojas de estilo en cascada para darle una vista más atractiva y brindarle al usuario una mejor experiencia.
>
> ## JavaScript
>>Nuestra aplicación no requiere de muchos efectos y animaciones, su uso más importante se encuentra en proporcionar alertas a los clientes y
>>
>>usuarios cuando existe un comportamiento erroneo, o al ingresar a espacios sin los permisos correspondientes.

## Diseño de la Base de datos
>## Diccionario de datos
>>Colección: usuario
>>
>>|Nombre   |Descripción          |Tipo de dato|Asignación    |
|---------|---------------------|------------|--------------|
|_id   |Identificador único de usuario|ObjectId|Autoasignación|
|nombre|Nombre con el cual se registra el usuario|String|Asignado por el usuario|
|correo|Correo electrónico del cliente con el cual realiza su registro y login|String|Asignado por el usuario|
|password|Clave de acceso a la cuenta del usuario|Binary|Proporcionada por el usuario y autocodificada|
>>
>>Colección: producto
>>
>>|Nombre   |Descripción          |Tipo de dato|Asignación    |
|---------|---------------------|------------|--------------|
|_id   |Identificador único de producto|ObjectId|Autoasignación|
|id_cliente|Identificador único que crea la relación del producto con el cliente que lo publica|String|Autoasignación|
|producto|Nombre con el que se publica el producto|String|Asignado por el usuario|
|tipo|Describe si se trata de un producto físico, digital o un servicio|String|Asignado por el usuario|
|precio|Costo por el producto o servicio publicado|Double|Asignado por el usuario|
>
>## Modelo orientado a objetos
>>![Modelo orientado a objetos.](/image/modelo orientado a objetos.png "Modelo de la base de datos")
>>Si la imagen no se muestra, puede consultarla en el correo que le envíe
>
>## Diagrama Entidad-Relación
>>![Diagrama ER.](/image/diagrama ER 1.png "Diagra ER")
>>Si la imagen no se muestra, puede consultarla en el correo que le envíe
>>
>>![Diagrama ER.](/image/diagrama ER 2.png "Diagra ER")
>>Si la imagen no se muestra, puede consultarla en el correo que le envíe

## Implementación del servidor
>## Rutas
>>El servidor cuenta con 8 rutas 3 de acceso público y 5 de acceso restringido:
>>* Rutas de acceso público:
>>  * Ruta principal donde se muestran todos los productos del catálogo **(/)**
>>  * **(/login)** Donde los usuarios registrados pueden iniciar sesión y así poder agregar productos, eliminarlos o editarlos.
>>  * **(/signup)** Para que nuevos usuarios puedan registrarse.
>>* Rutas de acceso restingido (el usuario debe ingresar con sus claves de acceso):
>>  * **(/mis_productos)** Ruta en la que el usuario puede obcervar todos los productos que registró teniendo las opciones de registrar nuevo, editar algun producto o eliminarlo.
>>      * **(/add_producto)** Cuando el ususario opta por la opcion registrar nuevo, es redireccionado a esta ruta que contiene el formulario para registrar el producto nuevo
>>      * El ususario al elegir la opción de editar se le redirecciona a la ruta **(/editar)** donde le espera el formulario con la información actual del producto a editar, para que la edición sea más eficiente.
>>      * Cuando el usuario elige la opción eliminar se le redirecciona a la ruta **(/eliminar)** donde se realiza la eliminación del producto seleccionado para posteriormente redireccionarlo a la ruta **(/mis_productos)**
>>  * Cuando el clienta seleccina la opción **logout** es redireccionado a la ruta **(/logout)** que se encarga de cerrar sesión y regresar al usuario a la ruta pública principal ocultando botones de acceso a las areas de acceso restringido **(/)**
>
>## Seguridad
>>Como se mencionó dentro de las rutas, se maneja una restricción de rutas. Esto se lleva a cabo con el módulo **session** que proporciona una confirmación de inicio de sesión con cierta información del cliente que inició sesión.
Hay botones que se activan y desactivan al iniciar o cerrar sesión, por ejemplo: al iniciar sesió se desactivan los botones de **signin** y **signup** puesto que el usuario ya se ah registrado, mientras que se activan botones como **mis productos**, **ver catálogo completo** y **cerrar sesión**, pero aún ocultando los botones se pueden ingresar las rutas en el buscador de direcciones, es entonces donde el módulo **session** entra en acción, puesto que al tratar de ingresar a una ruta de acceso restringido sin haber iniciado sesión, el usuario es redirigido a una ruta de acceso público con una alerta indicando que no puede acceder a esa ruta.
>>
>>La protección de las contraseñas de los usuarios registrados es protegida con un algoritmo de hash binario que proporciona el módulo **bcrypt**

# Resultados obtenidos
>* pagina de consulta del catálogo de productos completo.
>* Registro de usuarios nuevos proporcionando correo y contraseña.
>* Inicio de sesión proporcionando correo y contraseña.
>* Restringir areas de acceso no permitido. 
>* Protejer contraseñas de acceso.
>* Agregar, editar y eliminar productos registrados, una vez que se ah iniciado sesión.
# catalogo_online
# catalogo_online
