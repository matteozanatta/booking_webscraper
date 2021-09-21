# booking_webscraper
This algorithm's purpose is to get data from hotels and apartments listed on booking.com and store them in a csv database to conduct both data exploration and analysis.
You can set the check-in date, as well as the check-out date, the place, and how many people you want to find data of.

As of now (22 Sept. 2021) you can choose between 5 Italian cities from which to retrieve data (check the cities_id.txt file) but soon there'll be more cities.

Here you can play with it: https://bookingwebscraper.herokuapp.com.

# Python Libraries used
Webscraping was possible thanks to **BeautifulSoup** library, which had reliable css searching algorithm to find out all the html elements in the booking.com webpages that we needed.  
We used the well-known **Pandas** and **Numpy** libraries to deal with raw data and to create 'csv' format datasets.
The entire webpage (https://bookingwebscraper.herokuapp.com) has been made with **Plotly** (and Plotly Express), **Dash** and Dash Bootstrap, with the latter that gives us the opportunity to significantly raise the website design quality. Plotly Callbacks were really useful when creating dynamic data visualizations and provided fast plotting speed combined with practicality (even though a study period has been necessary because of the system that wasn't (isn't) super intuitive).

# Roadmap
10 Sept. 2021 Added multithreading capabilities to speed up the algorithm.
17 Sept. 2021 Developed a dashboard with HTML, Plotly and Dash both for webscraping and visualizing data.  
22 Sept. 2021 The website is now ready and everyone can use the algorithm via web interface.

# Known issues
Known issues: even though multithreading is implemented the algorithm is not so fast (especially with large cities with >1500 free structures) because it queries booking.com databases every time it needs to load other hotels or apartments. What should we do then? Find a way to tell which is the most efficient number of MAX_THREADS and search cycles to minimize the processing time.
