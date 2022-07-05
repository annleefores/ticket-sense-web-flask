# Ticket Sense Web
#### Video Demo:  <URL HERE>
#### Description:


Ticket Sense Web is a tool I build to get notified about ticket sales of any upcoming movie in my area. I used to keep on refreshing these ticket booking sites when something exciting was coming up. But I was not always successful in this, sometimes I did miss out on getting that perfect seat.

That's when I got the idea of creating a bot to do this for me. so I build Ticket Sense Web which is a tool that lets me add notifications for a specific film at a specific theatre on a date of my choosing. This bot then at every 5 min interval loads up the website collects needed data and then cross-checks it with the trigger keywords. If it finds a match then a notification with the booking link is sent out to my telegram chat app using telegram bots. I can then just click on that link and book the ticket.

I first build the MVP of ticket sense back in December of 2021 to get notified about Spider-man Homecoming. The main problem was that there was no publically available API provided by the 2 most popular ticket booking websites ( BookMyShow & TicketNew) in my place. The other solution was to use a web scraper. Even though it’s not the best solution it was the only solution I had. It took me some time to figure out the scraping process using the selenium module. 

Once I had made the basic working code, I deployed it to AWS Lambda. Everything was hard-coded into a single code, which meant I had to physically go and change the data whenever I want to use the code for checking any other movie on any other date. At that time I didn’t bother about that, but that too became boring after a while. 

As a project that I use a lot, an update was necessary.

So as my final project for CS50X I decided to implement a website and database for Ticket Sense. The updated Ticket Sense is now called Ticket Sense Web.  I made the front-end of the website using HTML, CSS, Bootstrap & JavaScript. The front-end is just a form that collects details like the movie theatre booking link, the name of the movie, and the opening date.

When the details are submitted first it's verified to ensure that all the needed data is present. If the verification fails an error page is displayed. After that, the data is further formatted and stored inside an SQLite database. Then the code redirects the user to a submitted page that displays the trigger/notification set by the user. Users can submit more triggers by going back to the index page and adding the details. All the triggers will be displayed with a delete button that can be used to delete that data from the database. 

The web scraping, checking, and notifying about ticket sales are done using ticketsense.py. In this code, the python selenium module is used to automate the chrome web browser. This automated browser goes to the link and loads the booking page, a set of web selectors are used to extract needed information from this page. This information is then matched with the user's database and if found the same, a ticket found message is printed. At the same time, a message with the booking link is sent to a telegram app bot connected to the specific user thus notifying the user. The communication to telegram is done using the bot API and user id. 

At first, the messaging was done using Twilio API to WhatsApp, but this was charged per message. so in search of an alternative, I hooked up the telegram module, which to my surprise worked so much better and costs me nothing. The code ticketsense.py is run periodically at a preset time after the flask app is enabled. This is done by setting up a cron job within app.py using apscheduler module

These are some of the issues I faced while building this tool.

- Setting up the chrome driver and chrome to run selenium perfectly turned out to be a tough task. It took me some time to figure out the versions of the software I need and the directories where I should install them.
- The other thing was playing with the selectors to get the data in the format I could use them.
- Coding app.py in such a way that ticketsense.py can be accessed and controlled by it.

I still haven’t figured out why the program works flawlessly locally on my system, but for some reason, the web scraping portion crashes sometimes when I run it through codespace. Must be due to some limitations of the docker container.

Currently, only 2 websites are supported in this tool. I have plans to add more features in the future to this, like an autocomplete form, enabling control features through the telegram bot, ironing out some bugs, and hosting it on Heroku.

Create a project folder and a venv folder within:

```
$ mkdir myproject

$ cd myproject

$ python3 -m venv venv
```

Activate the environment
```
$ . venv/bin/activate
```

Install Flask
```
$ pip install Flask
```

Install dependencies
```
$ pip install python-dotenv && pip install watchdog
```

Create .flaskenv file and add to it:
```
FLASK_APP=app.py
FLASK_ENV=development
```

Go to the chromedriver releases page. Find the suitable version of the driver for your platform and download it.
Make sure the chrome browser version matches the driver version.

For example this is the link for Chromedriver matching chrome version 100.0.4896.60
https://chromedriver.storage.googleapis.com/index.html?path=100.0.4896.60/

```
wget https://chromedriver.storage.googleapis.com/100.0.4896.60/chromedriver_linux64.zip
```

Extract the file with:
```
unzip chromedriver_linux64.zip
```

Make it executable:
```
chmod +x chromedriver
```

Add the driver to your PATH so other tools can find it:
```
export PATH=$PATH:/path-to-extracted-file/.
```

OR

Move file to PATH
```
sudo mv chromedriver /usr/local/bin/
```

use 
```pyTelegramBotAPI==4.4.0
selenium==4.1.3
python-dotenv==0.20.0
pip install APScheduler```
