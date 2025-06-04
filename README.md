# Galaxy Blast

## Descripción
Galaxy blast es un juego de tipo bullet hell espacial en el que se debe ir matando enemigos y jefes durante fases que suben de dificultad mientras se suma la máxima puntuación posible.

## Herramientas utilizadas
- Python como lenguaje para desarrollar el juego.
- Pygame como entorno gráfico.
- JSON para guardar la puntuación y las fases alcanzadas.

## Como ejecutar
En la carpeta raiz del juego `Galaxy Blast/` ejecutar con `py -m src.main`.

## Controles básicos
En los menús se puede navegar con las flechas y seleccionar opciones con enter.
Para jugar:
- Flechas direccionales: Moverse.
- Z: Disparar.
- X: Flash.
- C: Sobrecarga.

## Mecanicas principales
- Parry: Al usarse el dash en el momento exacto
- Sobrecarga: Al activarse se aumenta la cantidad de disparos, la velocidad de movimiento y de disparo y se reduce el cooldown del dash. Además ralentiza a los enemigos y sus disparos.
