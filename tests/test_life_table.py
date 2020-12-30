from GameOfLife.game import Cell, InputError, LifeTable
import pytest


@pytest.fixture
def life_table():
    return LifeTable()


@pytest.mark.life_table
def test_life_table_init(life_table):
    assert life_table.rules == {'birth': '3', 'surv1': '2', 'surv2': '3'}
    assert len(life_table.table) == life_table.SIZE
    assert len(life_table.table[0]) == life_table.SIZE
    cell = life_table.table[0][0]
    assert isinstance(cell, Cell)
    assert cell.value == 0
    assert not life_table.started


@pytest.mark.life_table
def test_life_table_init_inputerror():
    with pytest.raises(InputError) as e:
        LifeTable(rules="B1/S3")
    assert 'input needs to be:' in str(e.value)


@pytest.mark.life_table
def test_get_cell(life_table):
    middle = int(life_table.SIZE / 2)
    cell = life_table.get_cell(middle, middle)
    assert isinstance(cell, Cell)
    assert cell.value == 0
    assert cell.loc == (middle, middle)


place_num = [
    ((0, 0), 1),
    (None, 5),
    ((10, 10), 10),
    ((-1, 5), 2),
    ((1, 1000), 2),
    ((5, 5), 0),
    ((5, 5), -1)
]


@pytest.mark.life_table
@pytest.mark.parametrize('place, number', place_num)
def test_start_game(life_table, place, number):
    start = life_table.start_game(place=place, number=number)
    all_ones = [cell.value for row in life_table.table for cell in row if cell.value == 1]
    if place is None:
        place = (int(life_table.SIZE / 2), int(life_table.SIZE / 2))
    if place[0] < 0 or place[1] < 0 or place[0] > life_table.SIZE - 1 or place[1] > life_table.SIZE - 1:
        assert not start
        assert len(all_ones) == 0
    else:
        assert start
        if number > 8:
            assert len(all_ones) == 8
        elif number < 0:
            assert len(all_ones) == 1
        else:
            assert len(all_ones) == number


@pytest.mark.life_table
def test_next_generation(life_table):
    table = life_table.table
    table[0][0].value = 1
    table[0][1].value = 1
    table[1][0].value = 1
    assert not life_table.next_generation()
    life_table.started = True
    assert life_table.next_generation()
    assert table[1][1].value == 1


@pytest.mark.life_table
def test_str(life_table):
    assert "0" in str(life_table)
    assert "-" in str(life_table)
    assert "1" not in str(life_table)
    life_table.table[0][0].value = 1
    assert "1" in str(life_table)