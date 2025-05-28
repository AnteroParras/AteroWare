# Historial de Cambios

## [0.0.5] :  03 - 06 - 2025
- ### **Añadido**: 
  - Archivo Sprites_loader: Información de uso en **INFORMACIÓN_UTIL**
  - Archivo CHANGELOG: para llevar un historial de cambios
  - Archivo docs/Estructura_proyecto: Archivo visual sobre la estructura
  - Archivo test/spryte_test: Un test incompleto para tener una idea de como utilizar los Sprytes

- ### **Cambiado**:
  - Reorganización de carpetas: Toda la reorganización esta en **docs/Estructura_proyecto**
  - Se han añadido nueva informacion en **docs/INFORMACIÓN_UTIL**

- ### **Areglado**:
  - No se arregló nada pero para que veas el tipo de formato para el **CHANGELOG**


## [0.0.7] : 03 - 20 - 2025
### Rama alterada: Desarrollo
- ### **Añadido**:
  - #### Carpeta Core:
    - **Gestor_sprites**: Para cargar y gestionar los Sprites
    - **Gestor_escenas**: Para cargar y gestionar las escenas
    - **Gestor_audio**: Para cargar y gestionar los audios
    - **gestor_microgames**: Para cargar y gestionar los microgames
  
  - #### Carpeta microjuegos:
    - microgame_base: Clase base para los microgames
    - microgame_hankujas: Microjuego de hank ya implementado ( Falta musica )

- ### **Cambiado**:
  - Reorganización de carpetas: Toda la reorganización esta en **docs/Estructura_proyecto**
  - Se han añadido nuevas en **docs/TAREAS**
  - Se ha modificado AteroWare para implementar los nuevos gestores
  - El antiguo archivo microgames se ha llamado microgames_prev, quedando obsoleto

- ### **Areglado**:
  - El control de tiempos sobre los minijuegos

> [!IMPORTANT]
> Se prevee que la version [0.1] sea la primera versión jugable implementado todos los gestores, usando la rama release

> [!WARNING]
> No se puede eliminar aun microgames_prev por varias dependencias


## [0.0.8] :  08 - 04 - 2025
- ### **Añadido**:
  - Microjuego codigo: Microjuego de codigo ya implementado ( Falta musica )
  - Microjuego snake: Microjuego de snake ya implementado ( Falta musica )
  - Assets para snake
  
- ### **Cambiado**:
  - Se ha eliminado microgame_prev, ya no es necesario para el codigo en Ateroware
  - Se han modificado una serie de clases explicadas en detalle en Informacion_util

- ### **Areglado**:
  - Se ha solucionado el error a la hora de generar a los hanks



## [0.1] :  22 - 04 - 2025
- ### **Añadido**:
  - Macrojuego: Pong4D
  - Gestion de macrojuegos, ademas de pantalla, inicio y ventanas dedicadas al macrojuego
  - 
  
- ### **Cambiado**:
  - Se han activado los audios de los archivos, ya no son playholders
  
- ### **Areglado**:
  - Se ha arreglado incompatibilidades con la gestion de microjuegos y macrojuegos


## [0.8] :  24 - 04 - 2025
- ### **Añadido**:
  - Gestor de menus
  - Gran cantidad de assets
  
- ### **Cambiado**:
  - Se han puesto audios, efectos y gifs
  
## [0.8.6] :  06 - 05 - 2025
- ### **Añadido**:
  - Se ha añadido el microjuego Tetris
  - Se ha creado un nuevo menu, seleccion de minijuegos
  - Se han creado juegos especiales llamados "Infinity"
  
- ### **Arreglado**
  - Se ha arreglado el problema de crasheo al abrir juegos
  - Pong4D ya se puede ejecutar correctamente


## [0.9] :  08 - 05 - 2025
- ### **Cambiado**:
  - Se ha modificado por completo el archivo Ateroware.py, ahora es una clase en si misma
  - El bucle de juego se ha actualizado, aceptando ahora reinicio de juegos

- ### **Arreglado**
  - Se puede poner en pausa todos los juegos sin que haya fallos
  - Pong4D ya se puede cerrar correctamente

## [1.0.0] :  08 - 05 - 2025
- ### **Añadido**:
  - Se ha añadido el microjuego "polloVolador" con sus sprites y musica
  - Se ha añadido una opcion "Ayuda" en el menu de opciones
  - Se ha añadido el menu de ayuda en todos los minijuegos
  - Se ha añadido nuevas imagenes en los créditos

- ### **Arreglado**
  - Se ha arreglado el problema del bloque amaraillo en el Tetris
  - Se ha arreglado el fallo con los modos Infinity

