import math
import pathlib

import pygame
import sys

WIDTH = 1200
HEIGHT = 600
FPS = 30
FONT_FOLDER = pathlib.Path(__file__).parent.absolute() / "font/Roboto"
REGULAR_FONT = FONT_FOLDER / "Roboto-Regular.ttf"

BLACK = (0, 0, 0)
GREY = (102, 102, 110)
WHITE = (244, 244, 246)

pygame.font.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neat Visualiser")
BUTTON_DIC = {
    "Mutate": "mutate",
    "Mutate Connection": "mutate_connection",
    "Mutate Node": "mutate_node",
    "Mutate Shift Weight": "mutate_shift_weight",
    "Mutate Random Weight": "mutate_random_weight",
    "Mutate Toggle Connection": "mutate_toggle_connection",
    "Activate": "activate"
}
BUTTON_BOARDER = 3
BUTTON_WIDTH = (WIDTH / len(BUTTON_DIC)) - BUTTON_BOARDER
BUTTON_HEIGHT = HEIGHT * 0.1
BUTTONS = {}


def present(genome):
    clock = pygame.time.Clock()
    init_button()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_mouse_click(*pygame.mouse.get_pos(), genome)

        WIN.fill(BLACK)

        draw_buttons()
        draw_genome(genome)
        pygame.display.update()


def draw_genome(genome):
    network_height = HEIGHT - BUTTON_HEIGHT - BUTTON_BOARDER
    gene_node_dict = {}
    radius = int(network_height * 0.05)
    # padding_in, padding_out = 0, 0
    padding_in = (network_height - (
            (((genome.neat.inputs_count - 1) / genome.neat.inputs_count) * network_height) +
            BUTTON_HEIGHT + BUTTON_BOARDER + radius)) / 2
    padding_out = (network_height - (
            (((genome.neat.outputs_count - 1) / genome.neat.outputs_count) * network_height) +
            BUTTON_HEIGHT + BUTTON_BOARDER + radius)) / 2

    for node in genome.nodes:
        x = node.x * WIDTH
        y = node.y * network_height + BUTTON_HEIGHT + BUTTON_BOARDER + radius + \
            (padding_in if node.x == 0.1 else padding_out)

        boarder = pygame.draw.circle(WIN, WHITE, (x, y), radius, 5)  # border
        draw_text_centered_at(str(node.innovation_number), pygame.font.Font(REGULAR_FONT, radius), WHITE,
                              x, y, WIN, 0, 0)

        gene_node_dict[node.innovation_number] = boarder

    for con in genome.connections:
        from_circle = gene_node_dict[con.frm.innovation_number]
        to_circle = gene_node_dict[con.to.innovation_number]
        from_radian = math.atan2(to_circle.centery - from_circle.centery, to_circle.centerx - from_circle.centerx)
        to_radian = math.atan2(from_circle.centery - to_circle.centery, from_circle.centerx - to_circle.centerx)
        color = WHITE if con.enabled else GREY
        line = pygame.draw.line(WIN, color,
                         (from_circle.centerx + (math.cos(from_radian) * radius),
                          from_circle.centery + (math.sin(from_radian) * radius)),
                         (to_circle.centerx + (math.cos(to_radian) * radius),
                          to_circle.centery + (math.sin(to_radian) * radius)), 5)
        draw_text_centered_at(str(con.weight), pygame.font.Font(REGULAR_FONT, radius), color,
                              line.centerx, line.centery, WIN, 0, 0)

    pygame.display.flip()


def init_button():
    for i, button_key in enumerate(BUTTON_DIC.keys()):
        button = pygame.Rect((BUTTON_WIDTH + BUTTON_BOARDER) * i, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        BUTTONS[button_key] = button


def handle_button_mouse_click(x, y, genome):
    for method, button in BUTTONS.items():
        if button.collidepoint(x, y):
            print(method)
            if method == "Activate":
                output = getattr(genome, BUTTON_DIC[method])(1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
                print(output)
                return
            getattr(genome, BUTTON_DIC[method])()


def draw_buttons():
    for method_txt, button in BUTTONS.items():
        pygame.draw.rect(WIN, BLACK, button)
        pygame.draw.rect(WIN, GREY, button, 5)
        draw_text_centered_at(method_txt, pygame.font.Font(REGULAR_FONT, 20),
                              WHITE, button.x, button.y, WIN,
                              BUTTON_WIDTH - BUTTON_BOARDER * 2, BUTTON_HEIGHT)


def draw_text_centered_at(text, font, colour, x, y, screen, allowed_width, allowed_height):
    # first, split the text into words
    words = text.split()

    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        # add a line consisting of those words
        line = ' '.join(line_words)
        lines.append(line)

    # now we've split our text into lines that fit into the width, actually
    # render them

    # we'll render each line below the last, so we need to keep track of
    # the culmative height of the lines we've rendered so far
    y_offset = 0
    txt_height = 0
    for line in lines:
        txt_height += font.size(line)[1]

    for line in lines:
        fw, fh = font.size(line)

        # (tx, ty) is the top-left of the font surface
        tx = x + ((allowed_width - fw) / 2)
        ty = y + ((allowed_height - txt_height) / 2) + y_offset

        font_surface = font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))

        y_offset += fh
