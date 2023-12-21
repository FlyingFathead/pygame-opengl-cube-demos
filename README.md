![Cube Libre](https://github.com/FlyingFathead/pygame-opengl-polygon-demos/raw/main/cube_libre.jpg)

# OpenGL 3D cube-in-cube and other graphics demos
a.k.a. "Cube Libre" 
- various nested cube tests for `pygame` w/ `opengl`
- each demo comes with a different approach to multi-cube drawing
- by FlyingFathead (with a little help from imaginary digital friends) // dec 2023
- https://github.com/FlyingFathead/pygame-opengl-polygon-demos

## Description

Cube Libre is a Pygame and OpenGL demonstration project that explores the world of 3D cubes and their interactions. This project showcases various versions of a cube-based demo, each with its unique features and improvements.

## How to Run

To run "Cube Libre," make sure you have Python, Pygame, and OpenGL installed on your system. You can then execute i.e. `cube_libre.py` to start the demo. In `cube_libre.py` (which is the main demo at the moment), you can control the cube with either W,A,S,D keys or arrows. Colliding with the grid causes the cube to take damage (1 lost cube per impact within given tick timer limit), when all cubes are lost, the scene will reset.

## Changelog
`cube_libre.py`
- v0.10 - proximity gradient + shake effect on collision
- v0.09 - reset cycle for cube animation
- v0.08 - Reverted to this
- v0.07 - Flash and reset when all cubes are gone
- v0.06 - Reset on complete cube loss
- v0.05 - Wild horizons
- v0.04 - More cubes
- v0.03 - Horizon and navigation
- v0.02 - Solid color
