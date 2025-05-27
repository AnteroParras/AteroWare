## NOTACIONES
### Usos de import o from
En algunos archivos del juego veras que utilizo o bien from global... y en otros utilizo import globa... 
Esto dependerá del uso que le demos a las variables importadas, siendo que con from traemos variables que podemos **renombrar** y que **NO PODEMOS MODIFICAR**
En cambio usando import **NO PODEMOS RENOMBRAR** pero **SI PODEMOS MODIFICAR**, los usos dados son:
- En vidas, que al ser una variable que se debe modificar se usa como import
- En screen, como es una pantalla no modificable usamos from
- En el diccionario de colores, que tampoco se debe modificar usamos from
- etc...

### SPRITES_LOADERS
Esta archivo tiene dos clases implementada ( y una tercera en cocción si lo ves necesario ):
- Sprite: Sirve para cargar imagenes de casi cualquier tipo ( mejor usar PNG )
- GIFloader: Sirve para cargar GIFS, hereda de Sprite

### NOMBRE EN MICROJUEGOS
Antes era totalmente necesario empezase por microgame por la funcion que se utilizaba para recopilarlos pero ya no hace falta, cualqueir nombre es aceptado

Solo debe incluirse en el gestor de microjuegos

### AUDIO
Todo el audio se controla con gestor_audio.Audio().

Por defecto el metodo ejecutar de la clase MicrojuegoBase controla el audio, solo teniendo que definir el audio con el atributo self.musica.

Si quieres comportamientos distintos hay que sobreescribir el metodo ejecutar en las clases herencia


### SFX
Si se quiere incluir efectos de sonido hay que utilizar pygame.mixer.sound