# **_Weather Report_** (CS50 Final Project)
by Fabrizio C. Porta [[Github]](https://github.com/fabporta)
### Video Demo:  <https://youtu.be/GuwJ5NX69zg>
### **What is Weather Report?**
Weather Report is a simple weather widget made using the [tkinter package](https://docs.python.org/3/library/tkinter.html) native to Python.\
It offers weather information - such as weather description, degrees, min/max temperature and others - from a specific entered location, using data provided through the [OpenWeatherMap API](https://openweathermap.org/current), displayed in the metric system. The graphical user interface is embellished by a dynamic background photo of the entered city, supplied via the [Unsplash API](https://unsplash.com/developers).

## **Functioning**
### project.py
The **project.py** file, as requested by CS50P final project specs, is the main file of the project.\
It contains the vital functions and the GUI configuration of the program, built through the Canvas-class system of tkinter:

#### main()
The **_main_** function kicks off by defining the necessary tkinter engine and some of its properties, such as its geometry, name and its borderless aspect. Additionally, the window is set to be invisible (`root.attributes('-alpha', 0.0)`) to give the program the necessary time to boot up before displaying the interface to the user.\
Then, the function generates the Canvas object that hosts all of the GUI components. Multiple elements are defined, such as the background (set to a default one), the close button and the text displaying the user's time, the latter organized into the `TimeDate` class; these are constantly refreshed through custom functions (`BgDisplay()` and the `TimeDate.display()` method). Thereafter, labeled under the _Searchbar section_ there are the `Entry()` object and the graphic elements related, including the button that ignites the **_search_** function. Similarly is initialized the remaining section of non-interactive elements, that is to say the icons and/or textboxes of the weather description, current temperature's Celsius notation (and minimum/maximum for the day), wind speed and direction, humidity rate and the sunrise/sunset time for the day; additionally is created the space for the dedicated, interactive text displaying credit for the background photo. All of these entries set empty by default.\
Then, _main_ ends by executing the _default_ function (see the dedicated section), centering the windows and resetting it to its maximum `alpha` value to make it fully visible.

<sub>Note: the decision to organize the info objects into the _main_ function, whereas the similar time-displaying object is organized inside a Class of its own, may raise an eyebrow. It is however dictated by the structure of the Canvas on which the program relies and its `create.image` method, that results more manageable and joinable with the rest of the functions by being outside of a Class.</sub>

#### search()
The **_search_** function is the pulsating heart behind Weather Report's interactivity. It is called by clicking the search button and gets as its argument the input prompted by the user in the searchbar. If the function is called without entering any location, it steadily displays an error warning and interrupts the research.\
Else, it feeds the entered location to the **_query_** function - which plugs it as the search term on the OpenWeatherMap API and, on condition that the city actually exists, returns the API response as a `.json` - and uses the returned data to create a `WeatherData` object: that is a Class that parses the fed data into multiple, easy-accessible variables and keeps them organized. Then, the initialized object gets passed to the `infoUpdate` function, which deals with updating the previously-created canvas elements with the new data obtained. Further, the `bgUpdate` and `creditUpdate` functions are called with the entered location as arguments (more on that below).

#### getImg()
The **_getImg_** function is created to factorize a common process in the program, that is opening a specific image from the directory, adapting it to a custom size and returning it as a tkinter-compatible image. Its arguments are pretty intuitive: it takes two `int` parameters (x, y), that are respectively the desider lenght and height to resize the opened file, and a third `str` parameter, which is the name of the desired image file to open (inclusive of the extension). ì

#### degToDirection()
The **_degToDirection_** function handles the convertion of wind direction measured in degrees (the format provided by the API) into a cardinal direction, through simple calculation and indexing.

#### xUpdate() and xDisplay()
The **_(obj)Update_** functions are called to update an on-screen information with newly acquired data, and they're strictly complementary of the **_(obj)Display_** functions, which constantly refresh specific Canvas elements in order to display their latest version.\
Between these, it is worth noting _creditUpdate_, which updates the credit hypertext for the background photo with each photographer's name and Unsplash profile, as per the [Unsplash API Guidelines](https://help.unsplash.com/en/articles/2511245-unsplash-api-guidelines).

#### default()
The **_default_** function chooses a random city (within an harcoded list) to initialize the program with, essentially replicating the _search_ function with the chosen city.

## background.py
In the **background.py** module are located some functions useful for the operations related to the Unsplash API.

**_backgroundResearch_** initializes a request to the Unsplash API using its argument as the search term, and chooses the first returned object (i.e. the first photo-page that appears when searching that term).\
**_getBackground_** gets the photo from the object returned by _backgroundResearch_, downloading it through **_getImage_**, then resizing it and applying a black semitransparent overlay to make it ideal as background through **_configure_**; ultimately it saves the image as `dynamicBg.png`.\
**_getAuthor_** gets the author's name and Unsplash page from the object returned by _backgroundResearch_, returning them as variables that will be used in the main file as arguments to _creditUpdate_.

## test_project.py
This is the required test file that contains the unit tests to run through [pytest](https://docs.pytest.org/en/7.4.x/).
\
\
\
\
**This was CS50P!**