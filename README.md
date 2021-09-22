# booking_webscraper
This algorithm's purpose is to get data from hotels and apartments listed on booking.com and store them in a csv database to conduct both data exploration and analysis.
You can set the check-in date, as well as the check-out date, the place, and how many adults you want to find data for.

The project is composed by two main parts: the _webscraper_ and the _data visualization tool_. 

# How to use it
#### 1. You want to try just the visualization tool.
I uploaded the whole python program I created on a Heroku server with some data you can easily visualize. Here you can play with it: [Booking Webscraper](https://bookingwebscraper.herokuapp.com/data-visualization).

#### 2. You want to try just the webscraper.
In this case, git clone this repo on your computer and command 'python app.py' on the directory to succesfully start the program. The webpage will be available on localhost:8050. Check if you need to install missing packages.

#### 3. You want to try both the webscraper and the visualization tool.
Same as the previous case. Unfortunately, since the program is using multithreading the host is blocking the webscraping process because it takes a while to fully load, so you can only use it in local. Check if you need to install missing packages.



## Python Libraries used
Webscraping was possible thanks to **BeautifulSoup** library, which provided reliable css searching algorithms to find out all the html elements in the booking.com webpages that I needed.

I used the well-known **Pandas** and **Numpy** libraries to deal with raw data and to create 'csv' format datasets.

The entire webpage [Booking Webscraper](https://bookingwebscraper.herokuapp.com/data-visualization) has been made with **Plotly** (and Plotly Express), **Dash** and Dash Bootstrap, with the latter that gave me the opportunity to significantly enhance the website design quality. Plotly Callbacks were really useful when creating dynamic data visualizations and gave fast plotting speed combined with practicality (even though a study period has been necessary because of the system that wasn't (isn't) super intuitive).

## Variables in the datasets
Here is a brief list of the datasets columns and their datatype:
- **score** (float): it describes the review points the structure get from customers on booking.com;
- **n_reviews** (int): as the name suggests, it rapresents the total number of reviews given to a structure by people;
- **total_price** (float): this is the grand total a person has to pay to access a specific structure in the requested period;
- **category** (object): right after the booking.com data collection process, structures are grouped in five different categories (hotel, apartments, B&B, Holiday Home and Other);
- **city_center_dist** (float): this variables containes informations regarding how far the structure is from the city center;
- **neighborhood** (object): ever wondered what neighborhood a structure is in? This variable contains that info!
- **free_cancellation** (bool): is a structure listed with free cancellation on booking.com?
- **price_per_night** (float): this is simply the total price for the entire holiday divided by the number of nights you want to find informations for.

## Main problems and how I solved them
Webscraping a website like Booking.com isn't an easy task, mainly because of the scraping protections booking.com has built over time that don't let programs scrape data and save it for research purposes (spoiler: that doesn't mean it's an impossible task). 

### 1 - Speed 

While developing this project, one of the biggest problem has been the speed of the searching algoritm: the visualization part of the project is for the major part client side (so pretty fast), but the data gathering process was really slow: for every HTML get request, the python algorithm had to wait a response, then process it and send other HTML requests to the server to get the list of the structures. For small size samples this could be it, you don't need to implement any other functionality because it wouldn't be worth it. But doing some researches (if you're curious you can take a look at the log.txt file), I found out that over 75% of searches involved more than 800 potential structures listed on booking.com just for a specific city that you can set as an algorithm parameter. This led me to think that I absolutely had to fix this issue, otherwise the whole program would have been effective but extremely inefficient regarding time. I solved the problem implementing **multithreading**: with this simple but powerful python tool I speed the algorithm up by 15 times. Multithreading works sending multiple HTML get request at a time to booking.com website instead of waiting every X second for a single response from the server, then it waits for the response and appends the results to a pandas dataset. And poof! Problem solved! The median search time is about 60 seconds now.

### 2 - Booking.com is blocking my GET requests

This is what I spent plenty of hours on... but it was funny! Basically, the problem I stumbled upon was that even though I had implemented a multithreading algorithm I couldn't see any HTML response from the server. If it was a lucky day I could see one correct response out of 4-5 requests sent. What was the problem? I was sending raw HTML get requests using the requests python library and they were without headings. I strongly believe that booking.com has an anti-scraping system that detects if an HTML requests has correct headings and if it's coming from a trusted browser. To solve this issue, I artificially simulated GET requests with headings and random **user-agents** and the problem seemed solved. But I was wrong, in fact booking.com was detecting that I was sending hundred of thousands of HTML requests every hour from the same IP address and it heavily limited it. To get around this problem, I added to my previous html-heading-modifier algorithm a **proxy** functionality. So now, whenever you're using the algorithm you're sending a lot of request from different servers, with different user-agents.

### 3 - Raw data

Data the algorithm gathered was really messed up and lot of effort was required to set up an efficient cleaning system for the variables. One of the most challenging things was to deal with different data types because each one required a different treatment and has different complications, especially when computing operations between various of them. 

## Roadmap

22 Sept. 2021 | The website is now ready and everyone can visualize data via web interface.

17 Sept. 2021 | Developed a dashboard (only available in local) with HTML, Plotly and Dash both for webscraping and visualizing data.

10 Sept. 2021 | Added multithreading capabilities to speed the algorithm up.

## Known issues
Known issues: even though multithreading is implemented the algorithm is not so fast (especially with large cities with >1500 free structures) because it queries booking.com databases every time it needs to load other hotels or apartments. What should be done then? Find a way to tell which is the most efficient number of MAX_THREADS and search cycles to minimize the processing time.

Sometimes the algorithm stops working because booking.com detects the html request is fake and return an empty html page. If you want to solve this problem you just have to click on the 'retrieve data' button again to perform a new search.
