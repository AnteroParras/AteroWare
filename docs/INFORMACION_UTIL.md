## NOTACIONES
### Usos de import o from
En algunos archivos del juego veras que utilizo o bien from global... y en otros utilizo import globa... 
Esto dependerá del uso que le demos a las variables importadas, siendo que con from traemos variables que podemos **renombrar** y que **NO PODEMOS MODIFICAR**
En cambio usando import **NO PODEMOS RENOMBRAR** pero **SI PODEMOS MODIFICAR**, los usos dados son:
- En vidas, que al ser una variable que se debe modificar se usa como import
- En screen, como es una pantalla no modificable usamos from
- En el diccionario de colores, que tampoco se debe modificar usamos from
- etc...

### DICCIONARIOS DEFINIDOS
Usar diccionarios es bastante comodo para mantener una coherencia, es como una array con un index personalizado. En este caso lo he utlizado unicamente para los colores

### SPRITES_LOADERS
Esta archivo tiene dos clases implementada ( y una tercera en cocción si lo ves necesario ):
- Sprite: Sirve para cargar imagenes de casi cualquier tipo ( mejor usar PNG )
- GIFloader: Sirve para cargar GIFS, hereda de Sprite
- VideoLoader: Serviría para mostrar video

### NOMBRE EN MICROJUEGOS
Antes era totalmente necesario empezase por microgame por la funcion que se utilizaba para recopilarlos pero ya no hace falta, cualqueir nombre es aceptado

### IMPORTANTE
Reviste los cambios realizados en:
- AteroWare, ahora adaptado a la nueva forma de cargar los microjuegos con gestor_microjuegos
- GestorMicrojuegos, ahora usando la dificultad como parametro
- Las nuevas funciones en gestor_microjuegos, funciones sencillas pero hay que usar