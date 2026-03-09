# prova

Preparación para ingeniería inversa de juegos de ZX Spectrum y port a Python/Pygame.

## Archivos esperados
Coloca tus snapshots dentro de esta carpeta:

- `juego.tap`
- `juego.z80`

## Análisis inicial
```bash
python3 analyze_spectrum.py juego.tap
python3 analyze_spectrum.py juego.z80
```

## Esqueleto de port
```bash
python3 -m pip install pygame
python3 pygame_port_skeleton.py
```

Cuando los archivos estén presentes, el siguiente paso es mapear:

1. bucle principal,
2. controles,
3. estado de entidades,
4. colisiones/puntuación,
5. y trasladarlo al bucle `update/draw` de Pygame.
