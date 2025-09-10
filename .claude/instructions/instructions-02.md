## Próximo Sprint

Ya hemos avanzado mucho nuestro proyecto de Agente SQL, que es una interfaz escrita en Node.js para consultas a la base de datos de Shakila. 

El usuario realiza una consulta en lenguaje natural. 
El frontend escrito en Node.js hace la petición al backend de Python. 
El backend de Python utiliza la API de OpenAI para utilizar un modelo de lenguaje natural, un LLM, que traducirá la consulta en lenguaje natural a una consulta SQL. 

Tenemos el prompt, donde se especifica que el modelo debe devolver la consulta, una explicación, las consideraciones y alternativas con una estructura de salida en JSON. Todo eso está definido dentro del prompt del sistema. 

He hecho pruebas con Docker. Todos los servicios levantan. La base de datos se rellena correctamente. La consulta se envía correctamente al proveedor del modelo LLM, ya bien sea el de OpenAI ChatGPT o el local, con Docker Model Runner. 

## revisar y corregir

En principio está todo funcionando perfectamente, salvo que cuando se realiza la traducción de lenguaje natural a consulta SQL, el sistema no está mostrando por pantalla ni la explicación, ni las consideraciones, ni las alternativas. Solo está mostrando la consulta SQL. La consulta SQL la muestra correctamente, pero nos faltan esos datos (explicación, consideraciones, alternativas). El frontend está preparado para recibir esa información, pero por lo que sea no la está mostrando. Eso hay que revisarlo.

## probar

Ahora que hemos visto que el proveedor de openai funciona, es momento de probar contra el modelo que se ejecuta en local, con Docker Model Runner. Supongo que hay que cambiar alguna configuración en el docker-compose.yml, o en el comando de inicialización de docker que tecleeo en la terminal para arrancar los servicios.