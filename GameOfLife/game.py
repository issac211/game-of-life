# coverage - 100%
import random
import re


class InputError(Exception):
    pass


class Cell:
    def __init__(self, row_num, col_num):
        self.loc = (row_num, col_num)
        self.value = 0
        self.neighbors = []
        self._change_next_gen = None

    def set_neighbor(self, n_cell):
        if n_cell is None:
            return False
        self.neighbors.append(n_cell)
        return True

    def _get_neighbors_val(self):
        return [nei.value for nei in self.neighbors]

    def get_neighbors_loc(self):
        return [nei.loc for nei in self.neighbors]

    def change_value(self, rules, force=True):
        birth = int(rules['birth'])
        surv = (int(rules['surv1']), int(rules['surv2']))
        neighbors_val = self._get_neighbors_val()
        ones = neighbors_val.count(1)
        if self.value == 0 and ones == birth:
            if force:
                self.value = 1
            else:
                self._change_next_gen = 1
        elif (self.value == 1) and (ones < surv[0] or ones > surv[1]):
            if force:
                self.value = 0
            else:
                self._change_next_gen = 0
    
    def make_change(self):
        if self._change_next_gen is not None:
            self.value = self._change_next_gen
            self._change_next_gen = None

    def __str__(self):
        return str(self.value)


class LifeTable:
    SIZE = 50

    def __init__(self, rules="B3/S23"):
        RULES = re.compile(r"B(?P<birth>\d)\/S(?P<surv1>\d)(?P<surv2>\d)")
        the_rules = RULES.fullmatch(rules)
        if the_rules is None:
            raise InputError("input needs to be: 'B{num}/S{num}{num}'", rules)
        self.rules = the_rules.groupdict()
        self.table = self._make_table(self.SIZE)
        self._init_table()
        self.started = False

    def _make_table(self, size):
        table = []
        for row_num in range(size):
            row = [Cell(row_num, col_num) for col_num in range(size)]
            table.append(row)
        return table

    def _init_table(self):
        table = self.table
        for row in table:
            for cell in row:
                locations_list = self._fetch_cell_neighbors_locations(*cell.loc)
                for loc in locations_list:
                    n_cell = None
                    if loc is not None:
                        n_cell = self.get_cell(*loc)
                    cell.set_neighbor(n_cell)

    def _fetch_cell_neighbors_locations(self, row_num, col_num):
        left_n = None
        left_up = None
        left_down = None
        right_n = None
        right_up = None
        right_down = None
        up_n = None
        down_n = None

        if col_num > 0:
            left_n = (row_num, col_num - 1)
            if row_num > 0:
                left_up = (row_num - 1, col_num - 1)
            if row_num < self.SIZE - 1:
                left_down = (row_num + 1, col_num - 1)

        if col_num < self.SIZE - 1:
            right_n = (row_num, col_num + 1)
            if row_num > 0:
                right_up = (row_num - 1, col_num + 1)
            if row_num < self.SIZE - 1:
                right_down = (row_num + 1, col_num + 1)

        if row_num > 0:
            up_n = (row_num - 1, col_num)
        if row_num < self.SIZE - 1:
            down_n = (row_num + 1, col_num)

        return (left_n, left_up, left_down, right_n, right_up, right_down, up_n, down_n)
    
    def get_cell(self, row_num, col_num):
        if not (0 <= row_num < self.SIZE) or not (0 <= col_num < self.SIZE):
            return None
        return self.table[row_num][col_num]

    def start_game(self, place=None, number=5):
        if place is None:
            place = (int(self.SIZE / 2), int(self.SIZE / 2))
        row_num, col_num = place
        cell = self.get_cell(row_num, col_num)
        if cell is None:
            return False
        locations_list = cell.get_neighbors_loc()
        if number > len(locations_list):
            number = len(locations_list)
        if number < 0:
            number = 1
        random_choices = random.sample(locations_list, k=number)
        for loc in random_choices:
            n_cell = self.get_cell(*loc)
            if n_cell is not None:
                n_cell.value = 1
        self.started = True
        return True
    
    def next_generation(self):
        if not self.started:
            return False
        active_cells = self._check_active_cells()
        for cell in active_cells:
            cell.make_change()
        return True

    def _check_active_cells(self):
        table = self.table
        for row in table:
            for cell in row:
                if cell.value == 1:
                    locations_list = cell.get_neighbors_loc()
                    for loc in locations_list:
                        n_cell = self.get_cell(*loc)
                        n_cell.change_value(self.rules, force=False)
                        yield n_cell
                    cell.change_value(self.rules, force=False)
                    yield cell

    def __str__(self):
        cursor = "-" * 50
        printing = ""
        for row in self.table:
            for cell in row:
                printing = printing + str(cell)
            printing = printing + "\n"
        printing = printing + cursor
        return printing


def play_game(repeat_num):
    t = LifeTable()
    print(t)
    t.start_game()
    print(t)
    for _ in range(repeat_num):
        t.next_generation()
        print(t)


play_game(20)