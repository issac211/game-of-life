from GameOfLife.game import Cell
import pytest


@pytest.fixture(scope="module")
def cell():
    row_num = 4
    col_num = 5
    return Cell(row_num, col_num)


@pytest.fixture(scope="module")
def n_cells():
    n1_cell = Cell(4, 4)
    n2_cell = Cell(5, 5)
    n1_cell.value = 1
    n2_cell.value = 0
    n_cells = (n1_cell, n2_cell)
    return n_cells


@pytest.mark.cell
def test_cell_init(cell):
    assert cell.loc == (4, 5)
    assert cell.value == 0
    assert cell.neighbors == []
    assert cell._change_next_gen is None


@pytest.mark.cell
def test_set_neighbor(cell, n_cells):
    assert cell.set_neighbor(n_cells[0])
    assert len(cell.neighbors) == 1
    cell.set_neighbor(n_cells[1])
    assert len(cell.neighbors) == 2


@pytest.mark.cell
def test_get_neighbors_val(cell, n_cells):
    n_val_1 = n_cells[0].value
    n_val_2 = n_cells[1].value
    assert cell._get_neighbors_val() == [n_val_1, n_val_2]


@pytest.mark.cell
def test_get_neighbors_loc(cell, n_cells):
    n_loc_1 = n_cells[0].loc
    n_loc_2 = n_cells[1].loc
    assert cell.get_neighbors_loc() == [n_loc_1, n_loc_2]


@pytest.mark.cell
def test_change_value(cell, n_cells):
    rules_list = [
    {'birth': 3, 'surv1': 2, 'surv2': 3},
    {'birth': 2, 'surv1': 3, 'surv2': 3},
    ]
    assert cell.value == 0
    for n_cell in n_cells:
        n_cell.value = 1
    cell.change_value(rules_list[0], force=True)
    assert cell.value == 0
    cell.change_value(rules_list[1], force=True)
    assert cell.value == 1
    cell.change_value(rules_list[1], force=True)
    assert cell.value == 0
    cell.change_value(rules_list[1], force=False)
    assert cell.value == 0


@pytest.mark.cell
def test_make_change(cell):
    assert cell.value == 0
    cell.make_change()
    assert cell.value == 1
    cell.make_change()
    assert cell.value == 1


@pytest.mark.cell
def test_str(cell):
    assert str(cell) == "1"
    cell.value = 0
    assert str(cell) == "0"