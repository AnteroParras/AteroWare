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

### IMPORTANTE
En microgames.py existe la funcion:  
~~~
def all_microgames_list():
    return [func for name, func in globals().items() if callable(func) and name.startswith("microgame")]
~~~
Esta funcion se encarga de devolver una lista con todas las funciones, pero para ello es **NECESARIO QUE LOS MINIJUEGOS EMPIECEN POR minigame**