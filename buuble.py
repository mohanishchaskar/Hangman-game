import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Hollow Blue Bubble")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Bubble class
class Bubble:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = BLUE
        self.speed = random.randint(1, 3)

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        # Draw filled circle
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # Draw outlined circle to give the 3D effect
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius, 2)

# Main function
def main():
    bubbles = []

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Create bubbles
        if random.randint(1, 100) < 5:  # Adjust the frequency of bubbles
            bubble = Bubble(random.randint(0, WIDTH), HEIGHT, random.randint(10, 30))
            bubbles.append(bubble)

        # Update bubbles
        for bubble in bubbles:
            bubble.move()

        # Draw
        screen.fill(WHITE)
        for bubble in bubbles:
            bubble.draw(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
