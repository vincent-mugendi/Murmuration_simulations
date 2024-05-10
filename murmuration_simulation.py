import pygame
import random
import math

# Screen dimensions
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Bird parameters
NUM_BIRDS = 200
MAX_SPEED = 5  # Increased maximum speed
MAX_FORCE = 0.2  # Increased maximum force
VISION_RADIUS = 50
SEPARATION_RADIUS = 20
AVOID_RADIUS = 100

# Predator parameters
NUM_PREDATORS = 3
PREDATOR_SPEED = 8  # Increased predator speed
PREDATOR_VISION_RADIUS = 100

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Faster Murmuration Simulation")
clock = pygame.time.Clock()

# Vector class for 2D vectors
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return self / mag
        else:
            return Vector2D(0, 0)

# Bird class
class Bird:
    def __init__(self):
        self.position = Vector2D(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.velocity = Vector2D(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * random.uniform(0, MAX_SPEED)
        self.acceleration = Vector2D(0, 0)

    def apply_force(self, force):
        self.acceleration += force

    def update(self, birds, predators):
        # Apply flocking behaviors
        separation = self.separation(birds)
        alignment = self.alignment(birds)
        cohesion = self.cohesion(birds)
        avoid_predators = self.avoid(predators)

        # Weight the forces
        separation *= 1.5
        alignment *= 1.0
        cohesion *= 1.0
        avoid_predators *= 5.0

        # Apply forces
        self.apply_force(separation)
        self.apply_force(alignment)
        self.apply_force(cohesion)
        self.apply_force(avoid_predators)

        # Update velocity
        self.velocity += self.acceleration
        self.velocity = self.velocity.normalize() * min(self.velocity.magnitude(), MAX_SPEED)

        # Update position
        self.position += self.velocity
        self.position.x %= WIDTH
        self.position.y %= HEIGHT

        # Reset acceleration
        self.acceleration = Vector2D(0, 0)

    def separation(self, birds):
        # Move away from nearby birds
        steer = Vector2D(0, 0)
        count = 0
        for bird in birds:
            dist = (self.position - bird.position).magnitude()
            if 0 < dist < SEPARATION_RADIUS:
                diff = self.position - bird.position
                diff = diff.normalize() / dist
                steer += diff
                count += 1
        if count > 0:
            steer /= count
        if steer.magnitude() > 0:
            steer = steer.normalize() * MAX_SPEED - self.velocity
            steer = steer.normalize() * MAX_FORCE
        return steer

    def alignment(self, birds):
        # Align velocity with nearby birds
        avg_velocity = Vector2D(0, 0)
        count = 0
        for bird in birds:
            dist = (self.position - bird.position).magnitude()
            if 0 < dist < VISION_RADIUS:
                avg_velocity += bird.velocity
                count += 1
        if count > 0:
            avg_velocity /= count
            avg_velocity = avg_velocity.normalize() * MAX_SPEED
            steer = avg_velocity - self.velocity
            steer = steer.normalize() * MAX_FORCE
            return steer
        else:
            return Vector2D(0, 0)

    def cohesion(self, birds):
        # Move towards the center of mass of nearby birds
        avg_position = Vector2D(0, 0)
        count = 0
        for bird in birds:
            dist = (self.position - bird.position).magnitude()
            if 0 < dist < VISION_RADIUS:
                avg_position += bird.position
                count += 1
        if count > 0:
            avg_position /= count
            return self.seek(avg_position)
        else:
            return Vector2D(0, 0)

    def avoid(self, predators):
        # Move away from nearby predators
        steer = Vector2D(0, 0)
        for predator in predators:
            dist = (self.position - predator.position).magnitude()
            if 0 < dist < AVOID_RADIUS:
                diff = self.position - predator.position
                diff = diff.normalize() / dist
                steer += diff
        if steer.magnitude() > 0:
            steer = steer.normalize() * MAX_SPEED - self.velocity
            steer = steer.normalize() * MAX_FORCE
        return steer

    def seek(self, target):
        # Move towards a target position
        desired = target - self.position
        desired = desired.normalize() * MAX_SPEED
        steer = desired - self.velocity
        steer = steer.normalize() * MAX_FORCE
        return steer

    def draw(self):
        pygame.draw.circle(screen, BLACK, (int(self.position.x), int(self.position.y)), 3)

# Predator class
class Predator:
    def __init__(self):
        self.position = Vector2D(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.velocity = Vector2D(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * PREDATOR_SPEED

    def update(self):
        self.position += self.velocity
        self.position.x %= WIDTH
        self.position.y %= HEIGHT

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.position.x), int(self.position.y)), 5)

# Create birds
birds = [Bird() for _ in range(NUM_BIRDS)]

# Create predators
predators = [Predator() for _ in range(NUM_PREDATORS)]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    for predator in predators:
        predator.update()
        predator.draw()

    for bird in birds:
        bird.update(birds, predators)
        bird.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
