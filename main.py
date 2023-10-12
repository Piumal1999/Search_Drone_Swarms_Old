import pygame
from constants import *
from simulation import ScreenSimulation, Simulation


vec2 = pygame.math.Vector2
# =========================
screenSimulation = ScreenSimulation()

background_image = pygame.image.load("models/texture/camouflage.png").convert()
background_image = pygame.transform.scale(
    background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

simulation = Simulation(screenSimulation)

run = True
while run:
    # Draws at every dt
    screenSimulation.clock.tick(FREQUENCY)

    # Background
    screenSimulation.screen.fill(LIGHT_BLUE)
    screenSimulation.screen.blit(background_image, [0, 0])

    game_over, score = simulation.play_step()

    # updates and draws all simulations
    run = simulation.run_simulation()
    pygame.display.flip()

    if game_over:
        print(f'Game Over, Score: {score}')
        simulation.reset_simulation()

    if not run:
        pygame.time.wait(1000)
