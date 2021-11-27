import pathlib

import pygame as pygame
from pygame.locals import *
import random
import os

from neat.Neat import Neat

WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
FPS = 300
# STAT_FONT = pygame.font.SysFont("Aral", 50)
# END_FONT = pygame.font.SysFont("Aral", 70)
DRAW_LINES = False
VELOCITY = 5

FONT_FOLDER = pathlib.Path(__file__).parent.absolute() / "font/Roboto"
REGULAR_FONT_PATH = FONT_FOLDER / "Roboto-Regular.ttf"
pygame.font.init()
STAT_FONT_REGULAR = pygame.font.Font(REGULAR_FONT_PATH, 30)


WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bg.png")).convert_alpha(), (600, 900))
bird_images = [pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bird" + str(x) + ".png"))) for x in range(1, 4)]
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")).convert_alpha())

gen = 0


class Bird:
    MAX_ROTATION = 25
    IMGS = bird_images
    ROT_VEL = 20
    ANIMATION_TIME = VELOCITY
    JUMP_VELOCITY = -10.5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0  # degrees to tilt
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = self.JUMP_VELOCITY
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        # for downward acceleration
        displacement = self.vel * self.tick_count + 0.5 * 3 * self.tick_count ** 2  # calculate displacement

        # terminal velocity
        if displacement >= 16:
            displacement = (displacement / abs(displacement)) * 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        # For animation of bird, loop through three images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # so when bird is nose diving it isn't flapping
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # tilt the bird
        blit_rotate_center(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = VELOCITY

    def __init__(self, x):
        self.x = x
        self.height = 0

        # where the top and bottom of the pipe is
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)
        self.PIPE_BOTTOM = pipe_img

        self.passed = False

        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True

        return False


class Base:
    VEL = VELOCITY
    WIDTH = base_img.get_width()
    IMG = base_img

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def blit_rotate_center(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)


def draw_window(win, birds, pipes, base, score, gen, pipe_ind):
    win.blit(bg_img, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)

    for bird in birds:
        # draw lines from bird to pipe
        if DRAW_LINES:
            try:
                pygame.draw.line(win, (255, 0, 0), (
                    bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2), (
                                     pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width() / 2,
                                     pipes[pipe_ind].height), 5)
                pygame.draw.line(win, (255, 0, 0), (
                    bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2), (
                                     pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width() / 2,
                                     pipes[pipe_ind].bottom), 5)
            except:
                pass
        bird.draw(win)

    # score
    score_label = STAT_FONT_REGULAR.render("Score: " + str(score), True, (255, 255, 255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    # generations
    score_label = STAT_FONT_REGULAR.render("Gens: " + str(gen - 1), True, (255, 255, 255))
    win.blit(score_label, (10, 10))

    # alive
    score_label = STAT_FONT_REGULAR.render("Alive: " + str(len(birds)), True, (255, 255, 255))
    win.blit(score_label, (10, 50))

    pygame.display.update()


def run(genomes, generation, max_score):
    birds = []
    birds_genomes = []
    for g in genomes:
        birds.append(Bird(230, 350))
        birds_genomes.append(g)

    base = Base(FLOOR)
    pipes = [Pipe(WIN_WIDTH)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
                return 0
            # if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            #     bird.jump()

        pipe_ind = 0
        if len(birds) > 0:
            # determine whether to use the first or second
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                # pipe on the screen for neural network input
                pipe_ind = 1
        else:
            return 0

        for i, bird in enumerate(birds):  # give each bird a fitness of 0.1 for each frame it stays alive
            birds_genomes[i].score += 0.1
            bird.move()
            # send bird location, top pipe location and bottom pipe location
            # and determine from network whether to jump or not
            output = birds_genomes[i].activate(
                bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom))
            if output[0] > 0.5:
                bird.jump()

        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    birds_genomes[i].score -= 1
                    birds_genomes.pop(i)
                    birds.pop(i)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            if score == max_score:
                return score
            for g in birds_genomes:
                g.score += 5
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)

        # hits the flower
        for i, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= FLOOR or bird.y < 0:
                birds.pop(i)
                birds_genomes.pop(i)

        draw_window(win, birds, pipes, base, score, generation, pipe_ind)


def setup():
    input_count, output_count, genome_count = 3, 1, 20
    neat = Neat(input_count, output_count, genome_count)
    neat.C1 = neat.C2 = neat.C3 = 1
    neat.DT = 2  # distance threshold
    neat.WEIGHT_SHIFT_STRENGTH = 0.3
    neat.WEIGHT_RANDOM_STRENGTH = 1
    neat.KILLING_RATE = 0.4
    neat.PROBABILITY_MUTATE_CONNECTION = 0.01
    neat.PROBABILITY_MUTATE_NODE = 0.01
    neat.PROBABILITY_MUTATE_SHIFT_WEIGHT = 0.2
    neat.PROBABILITY_MUTATE_RANDOM_WEIGHT = 0.2
    neat.PROBABILITY_MUTATE_CONNECTION_TOGGLE = 0.003

    elite_score = 20
    generation = 500
    for i in range(generation):
        gen_score = run(neat.genomes, i, elite_score)
        if gen_score >= elite_score:
            pygame.quit()
            from neat.GUI import Presenter
            Presenter.present(neat.get_elite())
        neat.evolve()
        neat.print_species()
        print("================== {} ======================".format(i))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    # local_dir = os.path.dirname(__file__)
    # config_path = os.path.join(local_dir, 'config-feedforward.txt')
    # run(config_path)
    setup()
