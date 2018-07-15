# -----------------------------------------------------------------------------
# Name:        Project 5 - COLUMNS_GAMESTATE.PY
# Purpose:     Module used to implement functions of the columns game.
#
# Author:      Kai Malloy
# Student ID:  62023627
# Date:        12/6/2017
# -----------------------------------------------------------------------------


class GameState:
    """This class represents the Gamestate"""

    MATCH_LEN = 3
    F_SIZE = 3

    def __init__(self, rows: int, columns: int):
        self._active = True
        self._active_faller = False
        self._landed_faller = False
        self._faller_complete = True
        self._matched = False
        self._one_step_delay = False
        self._rows = rows
        self._columns = columns
        self._field = []
        self._faller = None
        self._previous_faller = None
        self._match_set = set()

    def get_total_rows(self) -> int:
        """This function gets the total rows"""
        return self._rows

    def get_total_columns(self) -> int:
        """This function gets the total columns"""
        return self._columns

    def set_field(self, contents: list) -> None:
        """This function sets the field"""
        self._field = contents

    def get_field(self) -> list:
        """This function gets the field"""
        return self._field

    def change_active_game(self) -> None:
        self._active = not self._active

    def active_game(self) -> bool:
        """This function sends the game state"""
        return self._active

    def match_found(self) -> bool:
        """This function prints the state for match found"""
        return self._matched

    def get_match_lst(self) -> set:
        """This function gets the match list"""
        return self._match_set

    def is_match(self, row: int, col: int) -> bool:
        """This function prints true when match is found"""
        for element in self._match_set:
            if row == element[0] and col == element[1]:
                return True
        return False

    def get_faller_size(self) -> int:
        """This function returns the faller size"""
        return self.F_SIZE

    def get_faller_colors(self) -> list:
        """This function returns the faller list to the gui"""
        if not self._faller:
            return self._previous_faller.get_lst()
        else:
            return self._faller.get_lst()

    def is_faller(self, faller_row: int, faller_col: int) -> bool:
        """This function prints true when it is a faller"""
        start = self._faller.get_last_row()
        if start >= self._faller.FALLER_SIZE:
            end = start - self._faller.FALLER_SIZE
        else:
            end = -1

        for num in range(start, end, -1):
            if self._faller.get_column() == faller_col and num == faller_row:
                return True
        return False

    def active_faller(self) -> bool:
        """This function is the gamestate for the faller"""
        return self._active_faller

    def landed_faller(self) -> bool:
        """This function is the gamestate for the landed faller"""
        return self._landed_faller

    def faller_complete(self) -> bool:
        return self._faller_complete

    def new_faller(self, faller_lst: list, faller_column: int) -> None:
        """This function makes a new faller"""
        self._active_faller = True
        self._faller_complete = False
        self._faller = Faller(faller_lst, -1, faller_column)
        self.move_faller()

    def move_faller(self) -> None:
        """This function moves the faller if it can"""
        if self._active_faller and self.capable_to_move():
            self._faller.set_last_row(self._faller.get_last_row() + 1)
            start = self._faller.get_last_row()
            if start >= self._faller.FALLER_SIZE:
                end = start - self._faller.FALLER_SIZE - 1
            else:
                end = -1

            count = 0
            for num in range(start, end, -1):
                if start >= self._faller.FALLER_SIZE and num == end + 1:
                    self._field[num][self._faller.get_column()].change_contents(' ')
                else:
                    self._field[num][self._faller.get_column()].change_contents(self._faller.get_reversed_lst()[count])
                    count += 1

        elif self._one_step_delay:
            self._one_step_delay = False
            self._matched = True
            self.match_exists()

        elif self._matched:
            self.remove_matches()
            self.reset_match_set()
            self._matched = False
            if self.match_exists():
                self._one_step_delay = True
                self.reset_match_set()
            else:
                self.reset_faller()
                self._faller_complete = True

        elif not self._active_faller:
            self._landed_faller = False
            if self.match_exists():
                self._matched = True
            else:
                self._faller_complete = True
                self.reset_faller()

        elif not self.capable_to_move():
            self._landed_faller = True
            self._active_faller = False
            if self.game_over():
                self._active = not self._active

    def capable_to_move(self) -> bool:
        """This function checks whether it can move"""
        if self._faller.get_last_row() == (self._rows - 1):
            return False
        elif self._field[self._faller.get_last_row() + 1][self._faller.get_column()].get_contents() != ' ':
            return False
        else:
            return True

    def game_over(self) -> bool:
        """This function checks whether game is over"""
        if self._faller.get_last_row() < (self._faller.FALLER_SIZE - 1) and not self.match_with_faller():
            return True
        return False

    def match_exists(self) -> bool:
        """This function checks to see if a match exists"""
        horiz_check = self._check_horiz()
        vert_check = self._check_vert()
        diag_check = self._check_diag(self._rows, 0)

        if horiz_check or vert_check or diag_check:
            return True

    def match_with_faller(self) -> bool:
        """This function checks if there is a match with a faller"""
        if self.match_exists():
            col = self._faller.get_column()
            start = self._faller.get_last_row()
            if start >= self._faller.FALLER_SIZE:
                end = start - self._faller.FALLER_SIZE
            else:
                end = -1

            for row in range(start, end, -1):
                for element in self._match_set:
                    match_row, match_col = element
                    if row == match_row and col == match_col:
                        return True
        return False

    def _check_horiz(self) -> bool:
        """This function checks for a horizontal match"""
        match = False
        counter = 0
        char = ''
        first_elmnt = ()
        temp_set = set()

        for num1 in range(self._rows):
            for num2 in range(self._columns):
                element = self._field[num1][num2].get_contents()
                if char == element and element != ' ':
                    counter += 1
                    temp_set.add((num1, num2))

                    if counter >= self.MATCH_LEN:
                        self._match_set.update(temp_set)
                        self._match_set.add(first_elmnt)
                        match = True
                else:
                    counter, char, first_elmnt, temp_set = self._refresh_variables(counter, char, first_elmnt, temp_set)
                    char = element
                    first_elmnt = (num1, num2)
                    counter = 1

            counter, char, first_elmnt, temp_set = self._refresh_variables(counter, char, first_elmnt, temp_set)
        return match

    def _check_vert(self) -> bool:
        """This function checks for a vertical match"""
        match = False
        counter = 0
        char = ''
        first_elmnt = ()
        temp_set = set()

        for num1 in range(self._columns):
            for num2 in range(self._rows):
                element = self._field[num2][num1].get_contents()
                if char == element and element != ' ':
                    counter += 1
                    temp_set.add((num2, num1))

                    if counter >= self.MATCH_LEN:
                        self._match_set.update(temp_set)
                        self._match_set.add(first_elmnt)
                        match = True
                else:
                    counter, char, first_elmnt, temp_set = self._refresh_variables(counter, char, first_elmnt, temp_set)
                    char = element
                    first_elmnt = (num2, num1)
                    counter = 1

            counter, char, first_elmnt, temp_set = self._refresh_variables(counter, char, first_elmnt, temp_set)

        return match

    def _check_diag(self, row: int, col: int) -> bool:
        """This function checks for a diagonal match"""
        match = False

        # up toward the right
        temp_set = set()
        first_elmnt = ()
        counter = 0
        char = ''
        row = 0
        col = 0

        for num1 in range(self._rows):
            row = num1
            col = 0
            while not col > (self._columns - 1) and not row < 0:
                element = self._field[row][col].get_contents()
                if char == element and element != ' ':
                    counter += 1
                    temp_set.add((row, col))

                    if counter >= self.MATCH_LEN:
                        self._match_set.update(temp_set)
                        self._match_set.add(first_elmnt)
                        match = True
                else:
                    counter, char, first_elmnt, temp_set = self._refresh_variables(counter, char, first_elmnt, temp_set)
                    char = element
                    first_elmnt = (row, col)
                    counter = 1
                row -= 1
                col += 1
            counter, char, first_elmnt, temp_set = self._refresh_variables(counter, char, first_elmnt, temp_set)

        for num2 in range(self._columns):
            row = self._rows - 1
            col = num2
            while not col > (self._columns - 1) and not row < 0:
                # print('row:', row, 'col:',col)
                element = self._field[row][col].get_contents()
                if char == element and element != ' ':
                    counter += 1
                    temp_set.add((row, col))

                    if counter >= self.MATCH_LEN:
                        self._match_set.update(temp_set)
                        self._match_set.add(first_elmnt)
                        match = True
                else:
                    counter, char, first_elmnt, temp_set = self._refresh_variables(counter, char, first_elmnt, temp_set)
                    char = element
                    first_elmnt = (row, col)
                    counter = 1
                row -= 1
                col += 1
            counter, char, first_elmnt, temp_set = self._refresh_variables(counter, char, first_elmnt, temp_set)


        # up toward the left
        temp_set = set()
        first_elmnt = ()
        counter = 0
        char = ''
        row = 0
        col = self._columns - 1

        for num1 in range(self._rows):
            row = num1
            col = self._columns - 1
            while not col < 0 and not row < 0:
                element = self._field[row][col].get_contents()
                if char == element and element != ' ':
                    counter += 1
                    temp_set.add((row, col))

                    if counter >= self.MATCH_LEN:
                        self._match_set.update(temp_set)
                        self._match_set.add(first_elmnt)
                        match = True
                else:
                    counter, char, first_elmnt, temp_set = self._refresh_variables(counter, char, first_elmnt, temp_set)
                    char = element
                    first_elmnt = (row, col)
                    counter = 1
                row -= 1
                col -= 1
            counter, char, first_elmnt, temp_set = self._refresh_variables(counter, char, first_elmnt, temp_set)

        for num2 in range(self._columns - 1, -1, -1):
            row = self._rows - 1
            col = num2
            while not col < 0 and not row < 0:
                # print('row:', row, 'col:',col)
                element = self._field[row][col].get_contents()
                if char == element and element != ' ':
                    counter += 1
                    temp_set.add((row, col))

                    if counter >= self.MATCH_LEN:
                        self._match_set.update(temp_set)
                        self._match_set.add(first_elmnt)
                        match = True
                else:
                    counter, char, first_elmnt, temp_set = self._refresh_variables(counter, char, first_elmnt, temp_set)
                    char = element
                    first_elmnt = (row, col)
                    counter = 1
                row -= 1
                col -= 1
            counter, char, first_elmnt, temp_set = self._refresh_variables(counter, char, first_elmnt, temp_set)

        return match

    def _refresh_variables(self, counter: int, char: str, first_elmnt: tuple, temp_set: set) -> tuple:
        """This function refreshes variables for vert and horiz"""
        counter = 0
        char = ''
        first_elmnt = ()
        temp_set = set()
        return counter, char, first_elmnt, temp_set

    def remove_matches(self) -> None:
        """This function removes the matches"""
        for num1 in range(self._rows):
            for num2 in range(self._columns):
                for element in self._match_set:
                    row, col = element
                    if num1 == row and num2 == col:
                        self._field[num1][num2].change_contents(' ')
        self._check_for_drops()

    def _check_for_drops(self) -> None:
        """This function checks for drops"""
        game_piece_str = []
        first_row = 0
        space_found = False
        num_spaces = 0

        for num1 in range(self._columns):
            for num2 in range(self._rows - 1, -1, -1):
                element = self._field[num2][num1]
                if space_found and element.get_contents() == ' ':
                    num_spaces = 1
                elif element.get_contents() == ' ' and num_spaces == 0:
                    space_found = True
                    first_row = element.get_row()
                elif space_found and element.get_contents() != ' ':
                    game_piece_str.append(element.get_contents())

            # print(self._match_set)
            # if self.remaining_match_faller(num1):
            #     for item in self.remaining_match_faller(num1):
            #         game_piece_str.append(item)
            # print(game_piece_str)

            if len(game_piece_str) > 0:
                count = 0
                for num2 in range(first_row, -1, -1):
                    element = self._field[num2][num1]
                    if count < len(game_piece_str):
                        element.change_contents(game_piece_str[count])
                        count += 1
                    else:
                        element.change_contents(' ')
            game_piece_str = []
            first_row = ()
            space_found = False
            num_spaces = 0

    def remaining_match_faller(self, col: int) -> list:
        """This function finds the remaining letters to drop"""
        remaining = []
        temp = []

        if self._faller.get_column == col and self.match_exists():
            col = self._faller.get_column()
            start = self._faller.get_last_row()
            if start >= self._faller.FALLER_SIZE:
                end = start - self._faller.FALLER_SIZE
            else:
                end = -1

            count = 0
            for row in range(start, end, -1):
                for element in self._match_set:
                    # print(element)
                    match_row, match_col = element
                    if row == match_row and col == match_col:
                        temp.append(self._faller.get_reversed_lst()[count])
                count += 1
        for item in self._faller.get_lst():
            if item not in temp:
                remaining.append(item)

        return remaining

    def reset_match_set(self) -> None:
        """This function resets a match"""
        self._match_set = set()

    def reset_faller(self) -> None:
        self._previous_faller = self._faller
        self._faller = None

    def rotate_faller(self) -> None:
        """This function rotates a faller"""
        if self._active_faller:
            start = self._faller.get_last_row()
            if start >= self._faller.FALLER_SIZE:
                end = start - self._faller.FALLER_SIZE
            else:
                end = -1

            self._faller.rotate_lst()
            count = 0
            for num in range(start, end, -1):
                self._field[num][self._faller.get_column()].change_contents(self._faller.get_reversed_lst()[count])
                count += 1

    def move_faller_left(self) -> None:
        """This function moves a faller to the left"""
        if (self._active_faller and self._faller.get_column() > 0 and self._field
                [self._faller.get_last_row()][self._faller.get_column() - 1].get_contents() == ' '):
            self._clear_current_faller_pos()
            self._redraw_faller(self._faller.get_column() - 1)
            self._faller.set_column(self._faller.get_column() - 1)

    def move_faller_right(self) -> None:
        """This function moves a faller to the right"""
        if (self._active_faller and self._faller.get_column() < (self._columns - 1) and self._field
                [self._faller.get_last_row()][self._faller.get_column() + 1].get_contents() == ' '):
            self._clear_current_faller_pos()
            self._redraw_faller(self._faller.get_column() + 1)
            self._faller.set_column(self._faller.get_column() + 1)

    def _clear_current_faller_pos(self) -> None:
        """This function clears the current faller position"""
        start = self._faller.get_last_row()
        if start >= self._faller.FALLER_SIZE:
            end = start - self._faller.FALLER_SIZE
        else:
            end = -1

        for num in range(start, end, -1):
            self._field[num][self._faller.get_column()].change_contents(' ')

    def _redraw_faller(self, col: int) -> None:
        """This function redraws a faller"""
        if self._active_faller:
            start = self._faller.get_last_row()
            if start >= self._faller.FALLER_SIZE:
                end = start - self._faller.FALLER_SIZE
            else:
                end = -1

            count = 0
            for num in range(start, end, -1):
                self._field[num][col].change_contents(self._faller.get_reversed_lst()[count])
                count += 1


class Faller:
    """This class represents a Faller object"""
    FALLER_SIZE = 3

    def __init__(self, faller_list: list, last_row: int, column: int):
        self._faller_lst = faller_list
        self._last_row = last_row
        self._column = column

    def get_lst(self) -> list:
        """This function gets the faller list"""
        return self._faller_lst

    def get_reversed_lst(self) -> list:
        """This function gets the reversed faller list"""
        reversed_lst = []
        for num in range(self.FALLER_SIZE - 1, -1, -1):
            reversed_lst.append(self._faller_lst[num])

        return reversed_lst

    def rotate_lst(self) -> None:
        """This function gets the rotated list"""
        lst = [self._faller_lst[2]]

        for num in range(0, 2):
            lst.append(self._faller_lst[num])

        self._faller_lst = lst

    def set_lst(self, new_faller: list) -> None:
        """This function sets the list"""
        self._faller_lst = new_faller

    def get_last_row(self) -> int:
        """This function gets the last row of the last faller"""
        return self._last_row

    def set_last_row(self, new_last_row: int) -> None:
        """This function sets the last row of the faller"""
        self._last_row = new_last_row

    def get_column(self) -> int:
        """This function gets the column"""
        return self._column

    def set_column(self, new_column: int) -> None:
        """This function sets the column"""
        self._column = new_column


class GamePiece:
    """This class represents Game Piece"""

    def __init__(self, contents: str, row: int, col: int):
        self._element = contents
        self._row = row
        self._col = col

    def get_contents(self) -> str:
        """This function gets the contents"""
        return self._element

    def change_contents(self, new_content: str) -> None:
        """This function changes the contents"""
        self._element = new_content


    def get_row(self) -> int:
        """This function gets the rows"""
        return self._row

    def get_col(self) -> int:
        """This function gets the columns"""
        return self._col
