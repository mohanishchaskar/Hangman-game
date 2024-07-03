import pygame
import random
import math

WIDTH, HEIGHT = 1365,710 
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Make the screen resizable
pygame.display.set_caption("Hangman !")

# Define constants for fire particle properties
FIRE_COLOR = (255, 100, 0)  # Adjust color as needed
FIRE_PARTICLE_RADIUS = 3
FIRE_SPEED_RANGE = (1, 1)  # Adjust speed range as needed

class FireParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = FIRE_PARTICLE_RADIUS
        self.color = FIRE_COLOR
        self.speed = random.randint(*FIRE_SPEED_RANGE)
        self.direction = random.uniform(0, 2 * math.pi)

    def move(self):
        # Update position based on speed and direction
        self.x += self.speed * math.cos(self.direction)
        self.y += self.speed * math.sin(self.direction)

    def draw(self, screen):
        # Draw fire particle as a circle
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def create_fire_particles(x, y, num_particles):
    # Generate multiple fire particles around the specified position
    particles = []
    for _ in range(num_particles):
        particle = FireParticle(x, y)
        particles.append(particle)
    return particles

def draw_fire_particles(particles, screen):
    # Draw all fire particles on the screen
    for particle in particles:
        particle.draw(screen)

def move_fire_particles(particles):
    # Move all fire particles to simulate fire movement
    for particle in particles:
        particle.move()

# Inside your main loop, update and draw fire particles
fire_particles = []

# Example usage:
while True:
    # Generate new fire particles periodically
    if random.randint(1, 100) < 25:  # Adjust frequency as needed
        new_particles = create_fire_particles(random.randint(0, WIDTH), HEIGHT, 5)
        fire_particles.extend(new_particles)

    # Move and draw fire particles
    move_fire_particles(fire_particles)
    draw_fire_particles(fire_particles, screen)

    pygame.display.update()
