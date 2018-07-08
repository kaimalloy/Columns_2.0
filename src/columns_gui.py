# -----------------------------------------------------------------------------
# Name:        Project 5 - COLUMNS_GUI.PY
# Purpose:     Module used to make a simple gui for the python shell.
#
# Author:      Kai Malloy
# Student ID:  62023627
# Date:        12/6/2017
# -----------------------------------------------------------------------------
import pygame
import columns_gamestate
import random


class ColumnsGame:
    """This class represents the Columns Game UI"""

    TOTAL_ROW = 12
    TOTAL_COL = 6
    NUM_COLORS = 10

    def __init__(self):
        self._running = True
        self._quit = False
        self._width = 700
        self._height = 550

    def run(self) -> None:
        """This function runs the GUI"""
        game_state = columns_gamestate.GameState(self.TOTAL_ROW, self.TOTAL_COL)
        game_state.set_field(self.build_field(self.TOTAL_ROW, self.TOTAL_COL))

        pygame.init()
        self._resize_surface((self._width, self._height))
        clock = pygame.time.Clock()
        last_time = pygame.time.get_ticks()

        self._draw_field(game_state)
        self._create_new_faller(game_state)

        while self._running:
            clock.tick(30)
            self._handle_events(game_state)

            if not self._quit and pygame.time.get_ticks() - last_time > 200:
                if not game_state.active_game():
                    self._quit = True
                if game_state.faller_complete():
                    self._create_new_faller(game_state)
                else:
                    game_state.move_faller()
                last_time = pygame.time.get_ticks()

            self._draw_field(game_state)

        pygame.quit()

    def build_field(self, rows: int, columns: int) -> list:
        """This function builds an empty list"""
        field = []
        for num1 in range(rows):
            new_column = []
            for num2 in range(columns):
                new_column.append(columns_gamestate.GamePiece(' ', num1, num2))
            field.append(new_column)
        return field

    def _create_new_faller(self, game_state: columns_gamestate.GameState) -> None:
        """This function creates a new faller"""
        faller_1 = int(round(random.random() * (self.NUM_COLORS - 1)))
        faller_2 = int(round(random.random() * (self.NUM_COLORS - 1)))
        faller_3 = int(round(random.random() * (self.NUM_COLORS - 1)))
        faller_loc = int(round(random.random() * (self.TOTAL_COL - 1)))

        game_state.new_faller([str(faller_1), str(faller_2), str(faller_3)], faller_loc)

    def _draw_field(self, game_state: columns_gamestate.GameState) -> None:
        """This function draws the field"""
        surface = pygame.display.get_surface()

        surface.fill(pygame.Color(128, 246, 115))

        black = 0, 0, 0
        white = 255, 255, 255
        off_white = 94, 94, 94
        gray = 192, 192, 192

        split_x = self._width / 20
        split_y = self._height / 15

        column_start_x = int(split_x * 7)
        column_start_y = int(split_y)

        column_width = split_x * 6
        column_height = split_y * 13

        margin_x = int(column_width / self.TOTAL_COL)
        margin_y = int(column_height / self.TOTAL_ROW)

        field = game_state.get_field()

        line_width = 2

        pygame.draw.rect(surface, black, (column_start_x, column_start_y,
                                          margin_x * self.TOTAL_COL, margin_y * self.TOTAL_ROW))

        for row in range(self.TOTAL_ROW):
            for col in range(self.TOTAL_COL):
                x = column_start_x + margin_x * col
                y = column_start_y + margin_y * row

                # pygame.draw.rect(surface, white, (x, y, margin_x, margin_y), line_width)
                pygame.draw.line(surface, off_white, (x, y), (x + margin_x - 5, y), line_width)
                pygame.draw.line(surface, off_white, (x, y), (x, y + margin_y - 5), line_width)

                if not game_state.faller_complete() and game_state.is_faller(row, col) \
                        and game_state.landed_faller():
                    pygame.draw.rect(surface, gray, (x + 2, y + 2, margin_x - 3, margin_y - 3))

                elif field[row][col].get_contents() != ' ':
                    if not game_state.faller_complete() and game_state.is_match(row, col):
                        color = white
                    else:
                        color = self._choose_color(int(field[row][col].get_contents()))
                    pygame.draw.rect(surface, color, (x + 2, y + 2, margin_x - 3, margin_y - 3))

        pygame.draw.rect(surface, white, (column_start_x, column_start_y,
                                          margin_x * self.TOTAL_COL, margin_y * self.TOTAL_ROW), line_width)

        pygame.display.flip()

    def _choose_color(self, num: int) -> (int, int, int):
        """This function chooses colors based on a list of predetermined colors"""
        # Red, Orange, Yellow, Mint, Turquoise, Blue, Navy, Purple, Pink, Brown
        colors = [(255, 51, 51), (255, 150, 0), (255, 255, 51), (0, 255, 128), (0, 255, 255),
                  (0, 128, 255), (0, 76, 153), (178, 102, 255), (255, 148, 202),  (153, 76, 0)]
        return colors[num]

    def _handle_events(self, game_state: columns_gamestate.GameState) -> None:
        """This function handles events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state.rotate_faller()
                elif event.key == pygame.K_LEFT:
                    game_state.move_faller_left()
                elif event.key == pygame.K_RIGHT:
                    game_state.move_faller_right()

    def _resize_surface(self, size: (int, int)) -> None:
        """This function handles resizing"""
        self._width, self._height = size
        pygame.display.set_mode(size, pygame.RESIZABLE)

    def _end_game(self) -> None:
        """This function ends the game"""
        self._running = False


if __name__ == '__main__':
    game = ColumnsGame()
    game.run()
