# booking_webscraper
This algorithm's purpose is to get data from hotels and apartments listed on booking.com and store them in a csv database to conduct both data exploration and analysis.
You can set the check-in date, as well as the check-out date, the place, and how many adults you want to find data for.

As of now (22 Sept. 2021) you can choose between 5 Italian cities from which to retrieve data (check the cities_id.txt file) but soon there'll be more cities.

Here you can play with it: [Booking Webscraper](https://bookingwebscraper.herokuapp.com).

# Python Libraries used
Webscraping was possible thanks to **BeautifulSoup** library, which provided reliable css searching algorithm to find out all the html elements in the booking.com webpages that we needed.

We used the well-known **Pandas** and **Numpy** libraries to deal with raw data and to create 'csv' format datasets.

The entire webpage [Booking Webscraper](https://bookingwebscraper.herokuapp.com) has been made with **Plotly** (and Plotly Express), **Dash** and Dash Bootstrap, with the latter that gave us the opportunity to significantly enhance the website design quality. Plotly Callbacks were really useful when creating dynamic data visualizations and gave fast plotting speed combined with practicality (even though a study period has been necessary because of the system that wasn't (isn't) super intuitive).

# Main problems and how I solved them
Webscraping a website like Booking.com isn't an easy task, mainly because of the scraping protections booking.com has built over time that don't let programs scrape data and save it for research purposes (spoiler: that doesn't mean it's an impossible task). 

### 1 - Speed (Multithreading)

While developing this project, one of the biggest problem has been the speed of the searching algoritm: the visualization part of the project is for the major part client side (so pretty fast), but the data gathering process was really slow: for every HTML get request, the python algorithm had to wait a response, then process it and send other HTML requests to the server to get the list of the structures. For small size samples this could be it, you don't need to implement any other functionality because it wouldn't be worth it. But doing some researches (if you're curious you can take a look at the log.txt file), I found out that over 75% of searches involved more than 800 potential structures listed on booking.com just for a specific city that you can set as an algorithm parameter. This led me to think that I absolutely had to fix this issue, otherwise the whole program would have been effective but extremely inefficient regarding time. I solved the problem implementing multithreading: with this simple but powerful python tool I speed the algorithm up by 15 times. Multithreading works sending multiple HTML get request at a time to booking.com website instead of waiting every X second for a single response from the server, then it waits for the response and appends the results to a pandas dataset. And poof! Problem solved! The median search time is about 60 seconds now.

### 2 - Booking.com is blocking my GET requests (Proxy/Fake User-Agents)

This is what I spent plenty of hours on... but it was funny! Basically, the problem I stumbled upon was that even though I had implemented a multithreading algorithm I couldn't see any HTML response from the server, if it was a lucky day I could see one correct response out of requests 4-5 sent. What was the problem? I was sending raw HTML get requests using the requests python library and they were without headings. I strongly believe that booking.com has an anti-scraping system that detects if an HTML requests has correct headings and if it's coming from a trusted browser. To solve this issue, I artificially simulated GET requests with headings and random user-agents and the problem seemed solved. But I was wrong, in fact booking.com was detecting that I was sending hundred of thousands of HTML requests every hour from the same IP address and it heavily limited it. To get around this problem, I added to my previous html-heading-modifier algorithm a proxy functionality. So now, whenever you're using the algorithm you're sending a lot of request from different servers, with different user-agents.

# Roadmap
10 Sept. 2021 | Added multithreading capabilities to speed up the algorithm.

17 Sept. 2021 | Developed a dashboard with HTML, Plotly and Dash both for webscraping and visualizing data.

22 Sept. 2021 | The website is now ready and everyone can use the algorithm via web interface.

# Known issues
Known issues: even though multithreading is implemented the algorithm is not so fast (especially with large cities with >1500 free structures) because it queries booking.com databases every time it needs to load other hotels or apartments. What should we do then? Find a way to tell which is the most efficient number of MAX_THREADS and search cycles to minimize the processing time.

Sometimes the algorithm stops working because booking.com detects the html request is fake and return an empty html page. If you want to solve this problem you just have to click on the 'retrieve data' button again to perform a new search.
