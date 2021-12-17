import pygame
from pygame.math import Vector2 as vec
from random import randint


class Primitive(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.position = pos
        self.size = size
        self.rect = self.image.get_rect(topleft=(self.position.x * self.size, self.position.y * self.size))
        self.image.fill((255, 255, 0))

    def move(self, new_pos):
        self.rect = self.image.get_rect(topleft=(new_pos.x * self.size, new_pos.y * self.size))
        self.position = new_pos

    def move_left(self):
        self.position += vec(-1, 0)
        self.rect = self.image.get_rect(topleft=(self.position.x * self.size, self.position.y * self.size))

    def move_right(self):
        self.position += vec(1, 0)
        self.rect = self.image.get_rect(topleft=(self.position.x * self.size, self.position.y * self.size))

    def move_down(self):
        self.position += vec(0, 1)
        self.rect = self.image.get_rect(topleft=(self.position.x * self.size, self.position.y * self.size))

    def rotate_clockwise(self, center=vec(0, 0)):
        normal_vector = self.position - center
        normal_vector.x, normal_vector.y = normal_vector.y, -normal_vector.x
        self.position = normal_vector + center
        self.rect = self.image.get_rect(topleft=(self.position.x * self.size, self.position.y * self.size))

    def get_rotated_position(self, center=vec(0, 0)):
        normal_vector = self.position - center
        normal_vector.x, normal_vector.y = normal_vector.y, -normal_vector.x
        return normal_vector + center

    def get_position(self):
        return self.position


class Shape(pygame.sprite.Group):
    shapes = {
        1: ((0, 0), (1, 0), (2, 0), (3, 0)),        # line
        2: ((0, 0), (1, 0), (2, 0), (0, 1)),        # left angle
        3: ((0, 0), (1, 0), (2, 0), (2, 1)),        # right angle
        4: ((0, 0), (1, 0), (0, 1), (1, 1)),        # cube
        5: ((0, 0), (1, 0), (2, 0), (1, 1)),        # T-shape
        6: ((0, 0), (1, 0), (1, 1), (2, 1)),        # left Z
        7: ((0, 1), (1, 1), (1, 0), (2, 0))         # right Z
    }

    def __init__(self, scaler):
        super().__init__()
        for pos in self.shapes[randint(1, 7)]:
            self.add(Primitive(vec(pos), scaler))

    def get_move_position(self, pos):
        vects = list()
        for element in self:
            vects.append(element.get_position() + pos)
        return vects

    def move(self, pos):
        for element in self:
            new_position = element.position + pos
            element.move(new_position)
        return True

    def get_position(self):
        vects = list()
        for element in self:
            vects.append(element.get_position())
        return vects

    def get_next_left_position(self):
        shape = list()
        for element in self:
            shape.append(element.get_position() + vec(-1, 0))
        return shape

    def move_left(self):
        for element in self:
            element.move_left()

    def get_next_right_position(self):
        shape = list()
        for element in self:
            shape.append(element.get_position() + vec(1, 0))
        return shape

    def move_right(self):
        for element in self:
            element.move_right()
        return True

    def get_next_down_position(self):
        shape = list()
        for element in self:
            shape.append(element.get_position() + vec(0, 1))
        return shape

    def move_down(self):
        for element in self:
            element.move_down()

    def get_rotated_position(self):
        shape = list()
        center = self.sprites()[1].position
        for element in self:
            shape.append(element.get_rotated_position(center))
        return shape

    def rotate_clockwise(self):
        center = self.sprites()[1].position
        for element in self:
            element.rotate_clockwise(center)


class Board(pygame.sprite.Group):
    def __init__(self, board_size: vec):
        super().__init__()
        self.board_size = board_size

    def can_it_be_placed(self, shape_vects: list):
        for el in shape_vects:
            if el.x < 0 or el.y < 0 or el.x >= self.board_size.x or el.y >= self.board_size.y:
                return False
        for element in self:
            if element.get_position() in shape_vects:
                return False
        return True

    def compact(self):
        line = self.board_size.y
        while line >= 0:
            line_primitives = pygame.sprite.Group()
            for element in self:
                if element.get_position().y == line:
                    line_primitives.add(element)
            if len(line_primitives) == int(self.board_size.x):
                print(f"Line num {line}, Elements in line: {len(line_primitives)}, line size: {self.board_size.x}")
                self.remove(line_primitives)
                for el in self:
                    if el.get_position().y < line:
                        el.move_down()
                line += 1
            line -= 1
