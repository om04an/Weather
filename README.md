# Weather website
This is a weather site that provides all the necessary data about the current weather in the city, which can be selected using the search on the site.

  *Site link:* **_( https://personal-weather.ru/ )_**
  
  *Site Preview:*
![This image](https://github.com/om04an/Weather/blob/main/WM-Screenshots-20230127201941.png)

## API
This site also provides api.

Standard request:
```
https://personal-weather.ru/api/
```
This query shows the weather in the city where it is located, which it specifies using ip.

Request by specific city:
```
https://personal-weather.ru/api/?city=Saint-Petersburg
```

#

Json response example:
```
{"weather":
  [{"model": "weather.city", 
    "pk": 1, 
    "fields": 
      {"city": "Saint Petersburg", 
       "temperature": "-2", 
       "temperature_feelslike": "-3", 
       "precipitation": "Overcast", 
       "wind": "1", 
       "cloudiness": "100", 
       "date": "2023-01-27", 
       "humidity": "80", 
       "localtime": "20:27:00", 
       "population": "5351935"}
       }]}
