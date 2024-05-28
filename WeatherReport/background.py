from PIL import Image
from PIL.ImageOps import fit
from urllib.request import urlretrieve
import requests

unsplashKey = r"XWB7lmShQSXy0tQIpOw44rGf4INXJQ41sIWixmnW3g4"
imgDir = r"/workspaces/150865231/WeatherReport/assets/temp.jpg"
overlayDir = r"/workspaces/150865231/WeatherReport/assets/overlay.png"
dest = r"/workspaces/150865231/WeatherReport/assets/dynamicBg.png"

def backgroundResearch(city="Rome, IT"):
    if city == None:
        raise TypeError("Invalid input")
    response = requests.get(f"https://api.unsplash.com/search/photos?per_page=1&total=1&query={city}&client_id={unsplashKey}").json()
    obj = response["results"][0]
    return obj


def getBackground(city="Rome, IT"):
    obj = backgroundResearch(city)
    img = getImage(obj)
    img = configure(imgDir)
    img.save(dest, "PNG")


def getAuthor(city="Rome, IT"):
    obj = backgroundResearch(city)
    author_name = obj["user"]["name"]
    author_url = obj["user"]["links"]["html"]
    return author_name, author_url


def configure(image):
    image = Image.open(image)
    image = fit(image, (700, 350)) # resize it
    overlay = Image.open(overlayDir) # open overlay
    image.paste(overlay, (0, 0), overlay) # paste it onto the original
    return image


def getImage(obj):
    photo_url = obj["urls"]["raw"]
    img = urlretrieve(photo_url, r"/workspaces/150865231/WeatherReport/assets/temp.jpg")
    return img


def main():
    city = "Rome, IT"
    getBackground(city)
    getAuthor(city)

if __name__=="__main__":
    main()

