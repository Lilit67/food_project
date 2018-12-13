from scheduling.scheduler import Scheduler
import pytest

recipe_schedule = [('premix', 30, False, True),
                   ('StretchFold', 150, True, True),
                   ('bulk fermentation', 14*60, True, False),
                   ('rest', 30, False, True),
                   ('shape', 30, True, True),
                   ('proof', 4*60, False, False),
                   ('bake', 40, False, True)]

recipe_schedule2 = [('premix', 30, False, True),
                   ('StretchFold', 150, True, True),
                   ('bulk fermentation', 14*60, True, False),
                   ('rest', 30, False, True),
                   ('shape', 30, True, True),
                   ('proof', 4*60, False, False),
                   ('bake', 40, False, True)]


my_schedule = [('Nov 22 2018  5:30PM', 'Nov 22 2018  10:30PM'),
('Nov 23 2018  5:30PM', 'Nov 23 2018  11:30PM')]

my_schedule2 = [('Nov 22 2018  5:30PM', 'Nov 22 2018  10:30PM'),
('Nov 23 2018  5:30PM', 'Nov 23 2018  11:30PM'),
               ('Nov 26 2018  5:30PM', 'Nov 23 2018  9:30PM')]

def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
    )


@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--cmdopt")


def test_1():
    tt = Scheduler()


    res = tt.calc_schedule(recipe_schedule, my_schedule)
    print (res)
    assert res

def test_2():
    tt = Scheduler()

    res = tt.calc_schedule(recipe_schedule2, my_schedule2)
    print (res)
    assert res