
#http//quotes.toscrape.com
import requests
from bs4 import BeautifulSoup
from csv import writer
from time import sleep # when we are scraping the server of the website from where we are scraping willbe affected so w should insert a time delay
from random import choice
##########################scraping##########################################
all_quotes = [] # we have created a list wherein we will save all the quotes, author and the link to their bio
base_url = "http://quotes.toscrape.com/"		#this part of the url is constant
url = "/page/1"			#this part of the url will keep changing according to the page
#instead of while true we are using while url to update the value of the url (page number)  
while url:
	res = requests.get(f"{base_url}{url}")#making the request from the url #concating both the urls
	print(f"Now Scraping{base_url}{url}")
	soup = BeautifulSoup(res.text,"html.parser")
	quotes = soup.find_all(class_="quote")#exctracting all the elements with a class = quote
#we have created a dictionary wherein we have stored the quotes, the author and the link to their bio which we will append(save in) the list named all_quotes
	for quote in quotes: 
		all_quotes.append({
			"text":quote.find(class_="text").get_text(),#quote exist inside the span tag having class=text
			"author":quote.find(class_="author").get_text(),#author's name exist inside the class author
			"bio-link":quote.find("a")["href"] # bio link is provided in the a tag having attribut href
			}) 
	next_btn = soup.find(_class="next")#in the link provided we can go to the next page using the next button, inspect it.. we will find that it is available inside a tag having attribute href
	url = next_btn.find("a")["href"] if next_btn else None # find the next page if it exists
	sleep(2)
#print(all_quotes)
######################game logic################################
quote = choice(all_quotes)
remaining_guesses = 4
print("Here's a quote:  ")
print(quote["text"])
print(quote["author"])
guess = ''
while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
	guess = input(f"Who said this quote? Guesses remaining {remaining_guesses}")
	if guess == quote["author"]:
		print("CONGRATULATIONS!!! YOU GOT IT RIGHT")
		break
	remaining_guesses-=1
	if remaining_guesses==3:
		res = requests.get(f"{base_url}{quote['bio-link']}")
		soup = BeautifulSoup(res.text, "html.parser")
		birth_date = soup.find(class_="author-born-date").get_text()
		birth_place = soup.find(class_="author-born-location").get_text()
		print(f"Here's a hint: The author was born on {birth_date}{birth_place}")
	elif remaining_guesses==2:
		print(f"Here's a hint: The author's first name starts with: {quote['author'][0]}")
	elif remaining_guesses==1:
		last_initial = quote["author"].split(" ")[1][0]
		print(f"Here's a hint: The author's last name starts with: {last_initial}")
	else:
		print(f"Sorry, you ran out of guesses. The answer was {quote['author']}")
################################refactoring###########################################
#again = ''
#hile again not in ('y', 'yes' ,'n','no'):
#	again = input("Would you like to play again (y/n)?")
#if (again.lower =='y'):
#	print("Ok you play again")
#else:
	#print("ok...Good bye!!!")
