from project import *
from pytest import raises

root = Tk()
canvas = Canvas(root, width="700", height="350", bd=1)


def test_TimeDate():
    assert TimeDate.get(canvas)
    with raises(AttributeError):
        TimeDate.get("Foo")
        TimeDate.get(123)


def test_WeatherData():
    with raises(TypeError):
        assert WeatherData()
        assert WeatherData("Foo")
        assert WeatherData(123)


def test_query():
    assert query("Hyrule") == None
    with raises(TypeError):
        assert query()
        assert query(1)


def test_getImg():
    with raises(TypeError):
        assert getImg()
        assert getImg(25, 25)
        assert getImg(25, "mappicon.png")
    with raises(FileNotFoundError):
        assert getImg(25, 25, "non_existent.png")


def test_degToDirection():
    assert degToDirection(10) == "N"
    assert degToDirection(100) == "E"
    with raises(AssertionError):
        assert degToDirection(100) == "N"
        assert degToDirection(10) == "E"
    with raises(TypeError):
        degToDirection()
    with raises(ValueError):
        degToDirection(-1)
        degToDirection(400)


def test_iconUpdate():
    assert iconUpdate(r"http://openweathermap.org/img/wn/10d@2x.png") == True
    with raises(requests.exceptions.MissingSchema):
        assert iconUpdate(10)
        assert iconUpdate("Mario")


def test_infoUpdate():
    with raises(TypeError):
        assert infoUpdate()
        assert infoUpdate("Foo")
        assert infoUpdate(123)
