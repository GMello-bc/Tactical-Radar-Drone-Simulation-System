# Tactical Radar Drone Simulation System

Real-time tactical radar simulation system designed for drone tracking, target monitoring, and mission control visualization.

![Radar Preview](assets/preview.png)

---

## Overview

Tactical Radar is a real-time tactical drone simulation developed in Python using the Pygame library. The project was created as a college assignment focused on real-time rendering, object-oriented programming, simulation systems, and interactive graphical interfaces.

The application simulates a military-inspired command center where autonomous drones patrol an operational area, track dynamic targets, execute attack missions, and return to base automatically. The interface includes radar scanning effects, animated particles, sound systems, mission logs, tactical panels, and visual effects designed to recreate a modern tactical environment.

---

# Features

* Real-time tactical radar simulation
* Autonomous drone patrol system
* Dynamic moving targets
* Mission assignment system
* Interactive tactical interface
* Radar sweep animation
* Particle explosion effects
* Drone trail rendering
* Sound effects and audio feedback
* State-based drone behavior
* Fullscreen tactical HUD

---

# Technologies Used

* Python
* Pygame
* Object-Oriented Programming (OOP)
* Real-time rendering systems
* Particle systems
* Event-driven programming

---

# System Architecture

The project was refactored into a modular structure to improve scalability, readability, and maintainability.

## Main Modules

### Core

Responsible for:

* game loop;
* configuration;
* constants;
* global settings.

### Entities

Contains:

* drones;
* targets;
* explosions;
* tactical units.

### Systems

Handles:

* mission management;
* audio systems;
* event logs;
* radar logic.

### UI

Responsible for:

* buttons;
* tactical panels;
* HUD rendering;
* interface effects.

### Utils

Contains:

* helper functions;
* mathematical interpolation;
* visual effects.

---

# Drone System

Each drone operates independently using a state-based behavior system.

Implemented states:

* Patrolling
* Assigned
* Engaging
* Attacking
* Returning

The drones automatically:

* patrol the map;
* receive targets;
* move toward enemies;
* execute attacks;
* return to base.

---

# Radar and Visual Effects

The radar system includes:

* rotating sweep animation;
* glow rendering;
* tactical grid rendering;
* lighting effects;
* particle explosions;
* animated movement trails.

These systems were implemented manually using Pygame rendering functions.

---

# Learning Objectives

This project was developed to improve knowledge in:

* real-time application development;
* software architecture;
* game loop systems;
* object-oriented programming;
* graphical rendering;
* simulation logic;
* event systems;
* modular code organization.

---

# Challenges

The main development challenges included:

* managing multiple simultaneous systems;
* synchronizing real-time animations;
* implementing smooth movement interpolation;
* organizing large-scale code structure;
* designing responsive tactical UI systems.

---

# Conclusion

Tactical Radar demonstrates how real-time simulation systems can be developed using Python and Pygame while applying advanced programming concepts such as modular architecture, state management, animation systems, and interactive rendering.

The project provided practical experience in software engineering, graphical programming, and system organization, serving as both a technical learning experience and a tactical simulation prototype.
