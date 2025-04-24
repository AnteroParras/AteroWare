# TAREAS
## CREAR MACROGAMES
Cada macrogame tendrá su propio archivo, ir pensando la estructura vaya


## EXPORTAR
Mirar como pirocas creamos un .exe vaya


## CONFETI
Dar efecto de confeti para Hank ( o lo que surja )

## AÑADIR ASSTES
Poco que explicar, hay que ajustar los tiempos de los microjuegos a su musica o al reves


## DEPURACION:
### Variables
Ajustar correctamente el nombre de las variables, a preferencia meter chascariilos para hacerlo mas gracioso

### Ajuste de  tiempos
Lo ideal seria eliminar la variable tiempo de cada microjuego y colocar su tiempo propio

Algo mucho mejor seria ajustar el tiempo en base a la dificultad, pero eso ya es un poco mas complicado

## MEJORAS
Estaria de lujisimo mejorar la funcion **show_text** en ***layout*** con las siguientes cosas:
- Poder elegir la alineacion horizontal
- Buscar una tipografica bonica para el juego
- Tal vez añadir funciones como rebordes para que se vea mejor sobre los fondos
- Comentar cada funcion en cada juego aunque sea un poco rebundante a veces


## Nerd zone
- ### **Cambios técnicos a realizar**
    - Hay un problema con los fps dentro del Pong4D, mirar eso
    - Pygame.mixer() no permite superponer audios, lo que significa que no podemos poner efectos de sonido, buscar si podemos hacer algo
    - Comprobar los tamaños de pantalla a la hora de dibujar, fijarse que todas las divisiones son exactas