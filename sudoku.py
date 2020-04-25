import pygame
pygame.init()

Width, Height = 1280, 720
Name = "Sudoku"
Win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption(Name)

bg = (255, 255, 255)

run = True

def grid():
    for i in range(3):
        pass 


def redraw_window():

    Win.fill(bg)
    pygame.display.update()

def main():
    while run:
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
