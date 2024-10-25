![Cube Libre](https://github.com/FlyingFathead/pygame-opengl-polygon-demos/raw/main/cube_libre.jpg)

# OpenGL 3D cube-in-cube and other graphics demos
a.k.a. "Cube Libre" 
- various nested cube tests for `pygame` w/ `opengl`
- each demo comes with a different approach to multi-cube drawing
- repo: https://github.com/FlyingFathead/pygame-opengl-cube-demos/

## Description

Cube Libre is a Pygame and OpenGL demonstration project that explores the world of 3D cubes and their interactions. This project showcases various versions of a cube-based demo, each with its unique features and improvements.

## How to Run

**(Debian/Ubuntu tree Linux)**

1. Make sure you have the Python `venv` package installed that's required for handling Python's virtual environments. If you don't have it, install it with i.e.:

    ```bash
    sudo apt-get install python3-venv
    ```

2. Make sure you have OpenGL libraries installed. Install them with i.e.:

    ```bash
    sudo apt install mesa-utils freeglut3-dev
    ```

2. Then, just run the `run.sh` script with i.e.:

    ```bash
    ./run.sh
    ```

The two abovementioned steps should be enough for most systems, if this doesn't work, figure out an environment where you can run:

    ```bash
    `pip install -r requirements.txt`
    ```

You can then execute the program with i.e. `python3 cube_libre.py` to start the demo. 

In `cube_libre.py` (which is the main demo at the moment), you can control the cube with either W,A,S,D keys or arrows. Colliding with the grid causes the cube to take damage (1 lost cube per impact within given tick timer limit), when all cubes are lost, the scene will reset. 

Currently, "Cube Libre" is merely an early proof-of-concept of a cubistic 3D platformer-strategy-puzzle game.

## Changelog
`cube_libre.py`
- v0.12.4 - more try/except blocks on startup for error catching
- v0.12.3 - fixes to OpenGL checkup on startup
- v0.12.2 - added OpenGL compatibility checks on startup
- v0.12.1 - added `run.sh`
- v0.12 - added numpy as an optimization option on vertices (not implemented yet; needs metrics)
- v0.11 - added stars
- v0.10 - proximity gradient + shake effect on collision
- v0.09 - reset cycle for cube animation
- v0.08 - Reverted to this
- v0.07 - Flash and reset when all cubes are gone
- v0.06 - Reset on complete cube loss
- v0.05 - Wild horizons
- v0.04 - More cubes
- v0.03 - Horizon and navigation
- v0.02 - Solid color

## About
- By FlyingFathead (with a little help from imaginary digital friends)
- Dec 2023 // Updated Oct 2024