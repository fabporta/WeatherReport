from time import strftime
from tkinter import *
from tkinter import messagebox
import Image, ImageTk
from background import getBackground, getAuthor
from webbrowser import open_new
from datetime import datetime
import requests
import random

APIKEY = "188601d4eba1a901871e7af694297b30"

DYNAMICBGDIR = r"/workspaces/150865231/WeatherReport/assets/dynamicBg.png"


class TimeDate():
    def __init__(self, canvas):
        self.lbl = canvas.create_text(350, 35, font=("Helvetica", "10", "bold"), fill="#d4d4d4", justify="c")

    def update(self, canvas):
        timeString = strftime(f'%A, %d %b, %H:%M')
        canvas.itemconfig(self.lbl, text=f"{timeString}")
        canvas.after(10, lambda: self.update(canvas))

    @classmethod
    def get(cls, canvas):
            return cls(canvas)


class WeatherData:
    def __init__(self, response):
        self.weather = response["weather"][0]['description'].capitalize()
        self.temp = response["main"]["temp"]
        #
        self.windspeed = response["wind"]["speed"] * 3.6
        wind_degrees = response["wind"]["deg"]
        self.wind_direction = degToDirection(wind_degrees)
        #
        self.humidity = response["main"]["humidity"]
        #
        country = response["sys"]["country"]
        name = response["name"]
        self.location = f"{name}, {country}"
        #
        temp_min = int(response["main"]["temp_min"])
        temp_max = int(response["main"]["temp_max"])
        self.temp_minmax = f"{temp_min}° / {temp_max}°"
        #
        self.timezone = response["timezone"]
        sunrise_date = datetime.utcfromtimestamp(response["sys"]["sunrise"]+self.timezone)
        sunset_date = datetime.utcfromtimestamp(response["sys"]["sunset"]+self.timezone)
        self.sunrise = sunrise_date.strftime(f"%H:%M")
        self.sunset = sunset_date.strftime(f"%H:%M")
        #
        icon_id = response["weather"][0]['icon']
        self.icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"


def main():
    root = Tk()
    root.attributes('-alpha', 0.0)
    root.title("WeatherReport")
    root.geometry("700x350")
    root.resizable(False,False)
    root.overrideredirect(True)

    ## MAIN CANVAS
    # create canvas
    global C
    C = Canvas(root, width="700", height="350", bd=1)
    C.pack(fill="both", expand=True)


    ## BACKGROUND
    # create empty image in canvas and update it to the default bg
    global bgLbl
    bgLbl = C.create_image(0, 0, anchor="nw")
    global bgImg
    bgImg = None
    C.itemconfig(bgLbl, image=bgImg)
    bgDisplay()


    ## CLOSE BUTTON
    closebuttonDefault = getImg(15, 15, "closebuttonDefault.png")
    closebuttonHighlight = getImg(15, 15, "closebuttonHighlight.png")
    closebuttonLbl = C.create_image(680, 20, image=closebuttonDefault)
    C.tag_bind(closebuttonLbl, '<Button-1>', lambda x: root.quit())
    C.tag_bind(closebuttonLbl, '<Enter>', lambda x: C.itemconfig(closebuttonLbl, image=closebuttonHighlight))
    C.tag_bind(closebuttonLbl, '<Leave>', lambda x: C.itemconfig(closebuttonLbl, image=closebuttonDefault))


    # TIME/DATE TEXT
    time = TimeDate.get(C)
    time.update(C)


    # UNSPLASH CREDIT
    global creditLbl
    creditLbl = C.create_text(350, 335, font=("Helvetica", "10"), fill="#a6a6a6")


    ## SEARCHBAR SECTION
    # searchbar.png
    sbarImg = getImg(255, 35, "searchbar.png")
    C.create_image(350, 80, image=sbarImg)
    # actual searchbar
    global searchCity
    searchCity = Entry(root, bd=0, width=20, font=("Helvetica", "12", "normal"), justify=CENTER)
    C.create_window(350, 80, window=searchCity)
    # mappointer.png
    mpImg = getImg(27, 27, "mappointer.png")
    mapIcon = Label(root, image=mpImg, bd=0, bg="#FFFFFF")
    C.create_window(250, 80, window=mapIcon)
    # search button
    sbuttonImg = getImg(25, 25, "searchicon.png")
    searchBttn = Button(root, image=sbuttonImg, bd=0, bg="#FFFFFF", command=lambda: search(searchCity.get()))
    C.create_window(448, 80, window=searchBttn)


    # WEATHER SECTION
    # weather description
    global weatherLbl
    weatherLbl = C.create_text(350, 115, font=("Helvetica", "12"), fill="#bcbcbc")
    # city display
    global cityLbl
    cityLbl = C.create_text(350, 145, font=("Helvetica", "18"), fill="#d4d4d4")
    # °C display
    global tempLbl
    tempLbl = C.create_text(350, 205, font=("Helvetica", "40"), fill="#FFFFFF")
    # min/max display
    global minmaxLbl
    minmaxLbl = C.create_text(350, 255, font=("Helvetica", "10"), fill="#bcbcbc")


    ## WEATHER ICON SECTION
    # icon bg
    iconBg = getImg(95, 95, "greyiconbg.png")
    C.create_image(200, 205, image=iconBg)
    # icon
    global iconLbl
    global iconImg
    iconImg = None
    iconLbl = C.create_image(200, 205, image=iconImg)
    iconDisplay()


    ## LEFT INFO SECTION (wind/humidity/sunrise-sunset)
    # wind icon
    windIcon = getImg(25, 25, "windicon.png")
    C.create_image(460, 175, image=windIcon)
    # wind text
    global windLbl
    windLbl = C.create_text(480, 175, font=("Helvetica", "10"), fill="#c9c9c9", anchor="w")
    # la goccia
    humidityIcon = getImg(20, 20, "humidityicon.png")
    C.create_image(462, 205, image=humidityIcon)
    # humidity text
    global humidityLbl
    humidityLbl = C.create_text(480, 205, font=("Helvetica", "10"), fill="#c9c9c9", anchor="w")
    # sunrise / sunset icon
    twilightIcon = getImg(25, 25, "twilighticon.png")
    C.create_image(462, 237, image=twilightIcon)
    # sunrise / sunset text
    global twilightLbl
    twilightLbl = C.create_text(480, 237, font=("Helvetica", "10"), fill="#c9c9c9", anchor="w")


    ## ROOT PROPERTIES and mainloop
    default()
    root.eval('tk::PlaceWindow . center')
    root.attributes('-alpha', 1.0)
    root.mainloop()


def search(city):
    if city == "":
        messagebox.showerror("Error", "Empty input")
        return None
    city = city.strip().lower()
    searchCity.delete(0 ,'end')
    response = query(city)
    if response == None:
        return None
    data = WeatherData(response)
    # update current on-screen info
    infoUpdate(data)
    # update background and credit
    bgUpdate(city)
    creditUpdate(city)


def query(city):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={APIKEY}&units=metric")
    if response.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    response = response.json()
    return response


def getImg(x: int, y: int, file="img.png"):
    imgDir = r"/workspaces/150865231/WeatherReport/assets/" + f"{file}"
    img = Image.open(imgDir)
    img = img.resize((x, y))
    img = ImageTk.PhotoImage(img)
    return img


def degToDirection(deg):
    if not 0 <= deg <= 360:
        raise ValueError("Degrees must be within 0 and 360")
    directions = ["N","N/NE","NE","E/NE","E","E/SE", "SE", "S/SE","S","S/SW","SW","W/SW","W","W/NW","NW","N/NW"]
    value=int((deg/22.5)) # since there are 360 degs and 16 directions, 360/16 = 22.5, so there's a new direction every 22,5
    return directions[value]


## UPDATE/DISPLAY FUNCTIONS

def iconDisplay():
    C.itemconfig(iconLbl, image=iconImg)
    C.after(10, iconDisplay)


def iconUpdate(url):
    global iconImg
    icon = Image.open(requests.get(url, stream=True).raw)
    iconImg = ImageTk.PhotoImage(icon)
    return True


def bgDisplay():
    C.itemconfig(bgLbl, image=bgImg)
    C.after(10, bgDisplay)


def bgUpdate(city="Rome, IT"):
    global bgImg
    getBackground(city)
    bgImg = ImageTk.PhotoImage(Image.open(DYNAMICBGDIR))


def creditUpdate(city="Rome, IT"):
    author_name, author_url = getAuthor(city)
    C.itemconfig(creditLbl, text=f"Photo by {author_name} on Unsplash")
    C.tag_bind(creditLbl, '<Button-1>', lambda x: open_new(author_url))
    C.tag_bind(creditLbl, '<Enter>', lambda x: C.itemconfig(creditLbl, fill="#efefef"))
    C.tag_bind(creditLbl, '<Leave>', lambda x: C.itemconfig(creditLbl, fill="#a6a6a6"))



# update on-screen info with current data
def infoUpdate(data):
    C.itemconfig(weatherLbl, text=f"{data.weather}")        # update weather description
    C.itemconfig(cityLbl, text=f"{data.location}")          # update city text
    C.itemconfig(tempLbl, text=f"{int(data.temp)}")         # update °C
    C.itemconfig(minmaxLbl, text=f"{data.temp_minmax}")     # update min/max
    C.itemconfig(windLbl, text=f"{int(data.windspeed)} km/h, {data.wind_direction}") # update wind
    C.itemconfig(humidityLbl, text=f"{data.humidity}%")     # update humidity
    C.itemconfig(twilightLbl, text=f"{data.sunrise} / {data.sunset}") # update sunrise / sunset
    iconUpdate(data.icon_url)                               # update icon


##

def default():
    city = random.choice(["Bari", "Rome, IT", "Firenze", "Pisa", "Milan", "Lugano", "Zurich", "Paris", "Vienna", "London", "Madrid", "New York"])
    response = query(city)
    data = WeatherData(response)
    infoUpdate(data)
    bgUpdate(city)
    creditUpdate(city)


if __name__=="__main__":
    main()
