Title: Dynamic Scraping with Python
Date: 2013-03-30

The library that I am discussing is meant for testing a website but it COULD also be used for scraping. It is YOUR responsibility that you scrape websites responsibly, not mine.
scraping static websites is easy. to protect themselves against scrapers (and because of the load on the servers) many websites implement javascript to load data asynchronosly when a user requests a website. in such a situation the client needs to wait before all the javascript is executed before all html is generated. in these cases you cannot use libraries like urllib and requests to retreive the html data.

### Enter selenium

Fortunately, there is a nice python library called selenium that emulates a browser for you which will still allow you to automate the collection of online data. In it's origin it is a java library but you can install the python bindings via pip. Selenium will use firefox as it's default browser, so make sure it's installed before installing selenium.

	$ sudo pip install selenium

Let's do a hello world example. We will get selenium to open google.com and make it return the browser windows title. open up a python terminal and run the following script;

	from selenium import webdriver  
	browser = webdriver.Firefox()  
	browser.get('http://www.google.com')  
	print browser.title  
	browser.quit()  

You should see a firefox window open and close. Because we have an actual browser window we get it along with a full javascript interpreter. If the page has javascript that needs to run, you can have python wait for it to finish;

	from selenium import webdriver  
	import time  
	browser = webdriver.Firefox()  
	browser.get('http://www.google.com')  
	time.sleep(1)  
	print browser.title  
	browser.quit() 
	full javascript control

Selenium gives you a lot of control over the browser. We can have a browser run and wait untill any javascript that needs to be run is loaded. We can even run any javascript we want from python in the browser;

	from selenium import webdriver  
	browser = webdriver.Firefox()  
	browser.get('http://www.google.com')  
	browser.execute_script("return document.cookie")  
	browser.execute_script("return navigator.userAgent")  
	browser.quit()  

You are able to have anything returned to python that javascript can access. You could even cause click events or query through css selectors with this library

	from selenium import webdriver  
	browser = webdriver.Firefox()  
	browser.get('http://www.google.com')  
	input =  browser.find_element_by_css_selector('input[type="text"]')
	input.send_keys('koaning.com')
	button =  browser.find_element_by_css_selector('button')
	button.click()
	browser.quit()  

Instead of using the click event on the button you could achieve a similar thing by sending keyboard information

	from selenium import webdriver  
	from selenium.webdriver.common.keys import Keys
	browser = webdriver.Firefox()  
	browser.get('http://www.google.com')  
	input =  browser.find_element_by_css_selector('input[type="text"]')
	input.send_keys('koaning.com')
	inputElement.send_keys(Keys.ENTER)
	browser.quit()  

Notice that you could also use `inputElement.submit()` to submit text to the inputelement instead of passing it a `Keys.ENTER` object.

### Automation

If you want to automate this approach you will most likely want to outsource the scraping to a server (the javascript can take some time). Initially you might notice that this script doesn't always work run when you run it through ssh on another machine. This is because selenium needs a window to operate from. It cannot just run the entire browser from a console. To get selenium to work we need to fake a window, this can be done with pyvirtualdisplay.

You can install it via;

	$ sudo pip install pyvirtualdisplay

If you log into a server through ssh then the following python script will work:

	from pyvirtualdisplay import Display  
	from selenium import webdriver  
	display = Display(visible=0, size=(800, 600))  
	display.start()  
	browser = webdriver.Firefox()  
	browser.get('http://www.google.com')  
	print browser.title  
	browser.quit()  
	display.stop()  

This can be useful for some small scrape jobs, be nice to the internet though. Both the client and the server need to do extra work through this trick. If you're gonna scrape, scrape responsibly. 

{% endfilter %}
{% endblock body %}
