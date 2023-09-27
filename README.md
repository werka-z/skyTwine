# Intro
skyTwine is a tool designed to alleviate the confusion caused by multiple weather forecasts. 
It takes forecasts from different sources, shows them side-by-side and calculates their average. Currently available for Kraków, Poland.  

# Preview
![Alt Text](https://github.com/werka-z/skyTwine/blob/master/preview.png)  


# Technology Stack
Framework: Django.  
Styling: Bootstrap.  
Database: SQLite.  
Techniques: API requests and a shared task to fetch and process data.  


# Data Sources
OpenWeather: Provides a 5-day forecast with logs every 3 hours. Daily weather is calculated by taking the average from the logs.  
WeatherAPI: Daily weather is directly plugged into the model.  
Averaging Method: Employs arithmetic averages for most parameters, with manually picked cases for description and icons.  
Fetched From: openweather.com, weatherapi.com in JSON format.  

# Models and Management
A Django model 'weather' populates the database, supported by a highly functional model manager.  

# Libraries Used
Celery: Manages fetching data and updating the forecasts every hour.  
Bootstrap: Templates from startbootstrap.com, mdbootstrap.com.  
Weather Icons: Sourced from joypixels.com.  
Other: Standard libraries like datetime and decouple.  

# Future Improvements
Potential upgrades include adding more locations, weather sources and data tracking for statistics.
