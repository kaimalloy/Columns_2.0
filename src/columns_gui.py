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
    NUM_COLORS = 6

    def __init__(self):
        self._running = True
        self._start_screen = True
        self._quit = False
        self._game_over = False
        self._width = 700
        self._height = 550
        self._last_time = 0
        self._event_last_time = 0
        self._event_left = False
        self._event_right = False
        self._event_down = False
        self._score = 0

    def run(self) -> None:
        """This function runs the GUI"""
        game_state = columns_gamestate.GameState(self.TOTAL_ROW, self.TOTAL_COL)
        game_state.set_field(self.build_field(self.TOTAL_ROW, self.TOTAL_COL))

        pygame.init()
        self._resize_surface((self._width, self._height))
        clock = pygame.time.Clock()
        self._last_time = pygame.time.get_ticks()

        # wait for the start screen
        while self._start_screen:
            clock.tick(30)
            self._handle_events(game_state)
            if pygame.time.get_ticks() - self._last_time > 2000:
                self._start_screen = False
                self._last_time = pygame.time.get_ticks()
            self._run_start_screen()
            if not self._running:
                pygame.quit()

        self._create_new_faller(game_state)
        self._draw_field(game_state)

        # start the music
        pygame.mixer.Channel(0).set_volume(0.1)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("columns.wav"), -1)


        # main loop
        while self._running:
            clock.tick(30)
            self._handle_events(game_state)
                
            if not self._quit and pygame.time.get_ticks() - self._last_time > 650:
                if not game_state.active_game():
                    pygame.mixer.Channel(0).stop()
                    self._quit = True
                    self._game_over = True
                if game_state.faller_complete():
                    self._create_new_faller(game_state)
                else:
                    game_state.move_faller()
                    if game_state.landed_faller():
                        pygame.mixer.Channel(1).set_volume(0.1)
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("landed.wav"))
                    if game_state.match_found():
                        self._score += len(game_state.get_match_lst())
                        pygame.mixer.Channel(2).set_volume(0.3)
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound("match.wav"))
                self._last_time = pygame.time.get_ticks()

            if self._game_over:
                if pygame.time.get_ticks() - self._last_time > 2000:
                    self._game_over = False
                self._draw_game_over()
            else:
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

    def _run_start_screen(self):
        """This function draws the start screen"""
        surface = pygame.display.get_surface()

        surface.fill(pygame.Color(128, 246, 115))

        # logo
        logo = pygame.image.load('columns_img.png')
        surface.blit(logo,(self._width//2 - logo.get_rect().size[0]//2,
                           self._height//3 - logo.get_rect().size[1]//2))

        # name
        font = pygame.font.SysFont("Agency FB", 30)
        created_by = font.render("Created by: Kai Malloy", True, (0, 0, 0))

        surface.blit(created_by, (self._width//2 - font.size("Created by: Kai Malloy")[0]//2,
                                  self._height//2 + font.size("H")[1]//3))

        # copyright
        font = pygame.font.SysFont("Times New Roman", 15)
        cpyright = font.render("Created for educational purposes only. No copyright intended.", True, (0, 0, 0))

        surface.blit(cpyright, (self._width//2 -
                                  font.size("Created for educational purposes only. No copyright intended.")[0]//2,
                                  self._height - font.size("H")[1]))

        pygame.display.flip()


    def _create_new_faller(self, game_state: columns_gamestate.GameState) -> None:
        """This function creates a new faller"""
        faller_1, faller_2, faller_3 = 0, 0, 0
        while faller_1 == faller_2 and faller_1 == faller_3 and faller_2 == faller_3:
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


        
        # faller hint block
        block_start_x = column_start_x - margin_x - margin_x/2
        block_start_y = column_start_y

        pygame.draw.rect(surface, black,(block_start_x, block_start_y,
                                          margin_x + 2, margin_y * 3 + 2))

        for num in range(game_state.get_faller_size()):
            hint_start_x = block_start_x + 2
            hint_start_y = block_start_y + margin_y * num + 2
            pygame.draw.rect(surface, self._choose_color(int(game_state.get_faller_colors()[num])),
                             (hint_start_x, hint_start_y, margin_x - 2, margin_y - 2))

        # Text
        left_x = column_start_x
        right_x = column_start_x + margin_x * self.TOTAL_COL
        bottom_y = column_start_y + margin_y * self.TOTAL_ROW

        font = pygame.font.SysFont("comicsansms", 20)
        score_text = font.render("SCORE:", True, (255,215,0), black)
        score = font.render(str(self._score), True, (255,215,0), black)
        
        surface.blit(score_text, (left_x - margin_x * 4, bottom_y - margin_y * 3))

        pygame.draw.rect(surface, black, (left_x - margin_x * 4,
                                            bottom_y - margin_y * 3 + font.size("H")[1],
                                            margin_x * 3, font.size("H")[1]))
        
        surface.blit(score, (left_x - margin_x  - font.size(str(self._score))[0],
                             bottom_y - margin_y * 3 + font.size("H")[1]))
    
        pygame.display.flip()

    def _draw_game_over(self) -> None:
         surface = pygame.display.get_surface()

         surface.fill(pygame.Color(128, 246, 115))

         font = pygame.font.SysFont("Agency FB", 100, True)
         game_over_text = font.render("GAME OVER", True, (0 ,0 ,0))

         surface.blit(game_over_text, (self._width//2 - font.size("GAME OVER")[0]//2,
                                  self._height//2 - font.size("H")[1]//2))

         pygame.display.flip()

    def _choose_color(self, num: int) -> (int, int, int):
        """This function chooses colors based on a list of predetermined colors"""
        # Red, Orange, Yellow, Green, Blue, Purple
        colors = [(255, 51, 51), (255, 150, 0), (255, 255, 51),
                  (50, 205, 50), (0, 191, 255), (186, 85, 211)]
        return colors[num]

    def _handle_events(self, game_state: columns_gamestate.GameState) -> None:
        """This function handles events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
##            elif event.type == pygame.VIDEORESIZE:
##                self._resize_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Channel(3).set_volume(0.1)
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound("rotate.wav"))
                    game_state.rotate_faller()
                elif event.key == pygame.K_LEFT:
                    self._event_left = True
                    game_state.move_faller_left()
                elif event.key == pygame.K_RIGHT:
                    self._event_right = True
                    game_state.move_faller_right()
                elif event.key == pygame.K_DOWN and game_state.active_faller():
                    self._event_down = True
                    game_state.move_faller()
                    self._last_time = pygame.time.get_ticks()
                    if game_state.landed_faller():
                        pygame.mixer.Channel(1).set_volume(0.1)
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("landed.wav"))
                # set the last time for continuous button presses
                self._event_last_time = pygame.time.get_ticks()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self._event_left = False
                elif event.key == pygame.K_RIGHT:
                    self._event_right = False
                elif event.key == pygame.K_DOWN:
                    self._event_down = False

        # if enough time elapses while holding down key, move rapidly
        if self._event_left and pygame.time.get_ticks() - self._event_last_time > 300:
            game_state.move_faller_left()
        elif self._event_right and pygame.time.get_ticks() - self._event_last_time > 300:
            game_state.move_faller_right()
        elif self._event_down and pygame.time.get_ticks() - self._event_last_time > 300 \
                              and game_state.active_faller():
            game_state.move_faller()
            self._last_time = pygame.time.get_ticks()
            if game_state.landed_faller():
                        pygame.mixer.Channel(1).set_volume(0.1)
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("landed.wav"))
                


    def _resize_surface(self, size: (int, int)) -> None:
        """This function handles resizing"""
        self._width, self._height = size
        # took out pygame.RESIZABLE
        pygame.display.set_mode(size)

    def _end_game(self) -> None:
        """This function ends the game"""
        self._running = False


if __name__ == '__main__':
    game = ColumnsGame()
    game.run()
