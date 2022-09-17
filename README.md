# Ticket Sense Web (flask)
#### Video Demo:  <URL HERE>
#### Description:


Ticket Sense Web (flask) is a tool I build to get notified about ticket sales of any upcoming movie in my area.
  
Currently, only 2 websites are supported in this tool. I have plans to add more features in the future to this, like an autocomplete form, enabling control features through the telegram bot, ironing out some bugs, and hosting it on Heroku.
---
Update [17 Sept 2022]: I have rebuild this entire project using Django, Next.js and Scrapy with some of the features I talked about adding in the future. [Check it out](https://ticketsense.annleefores.com/)
---

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
