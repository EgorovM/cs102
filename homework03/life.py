import pygame
from pygame.locals import *
import random
from pprint import pprint as pp

class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        clist = self.cell_list(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            clist = self.update_cell_list(clist)
            self.draw_cell_list(clist)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True):
        """ Создание списка клеток.

        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        self.clist = [[random.randint(0,1) if randomize else 0 \
                     for i in range(self.cell_width)]
                     for i in range(self.cell_height)]
        # PUT YOUR CODE HERE
        return self.clist

    def draw_cell_list(self, clist):
        """ Отображение списка клеток

        :param rects: Список клеток для отрисовки, представленный в виде матрицы
        """

        for line_ind in range(len(clist)):
            for cell_ind in range(len(clist[line_ind])):
                pygame.draw.rect(self.screen, pygame.Color('green') if clist[line_ind][cell_ind] else pygame.Color('white'),
                    (cell_ind * self.cell_size, line_ind * self.cell_size,
                    self.cell_size, self.cell_size))

        self.draw_grid()

    def get_neighbours(self, cell):
        """ Вернуть список соседей для указанной ячейки

        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        neighbours = []
        cell_row, cell_col = cell
        for row in range(3):
            for col in range(3):
                cur_row, cur_col = cell_row - 1 + row, cell_col - 1 + col

                if (cur_row, cur_col) != cell and cur_row >= 0 and cur_col >= 0 and\
                    cur_col < self.cell_width and cur_row < self.cell_height:
                    neighbours.append((cell_row - 1 + row, cell_col - 1 + col))

        return neighbours

    def update_cell_list(self, cell_list):
        """ Выполнить один шаг игры.

        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.

        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        new_clist = [[0 for i in range(self.cell_width)] for i in range(self.cell_height)]

        for row in range(self.cell_height):
            for col in range(self.cell_width):
                neighbours_count = 0

                for cur_cell in self.get_neighbours((row, col)):
                    if cell_list[cur_cell[0]][cur_cell[1]]:
                        neighbours_count += 1

                if neighbours_count >= 2 and neighbours_count <= 3:
                    new_clist[row][col] = 1

        self.clist = new_clist
        return self.clist
