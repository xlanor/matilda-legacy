from telegram.ext import Updater
import requests
import string
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser
class Commands():
	def commands (bot,update):
		bot.sendMessage(chat_id=update.message.chat_id, text="""Hi, this are the commands that I currently support \n 
																- /aboutme (about the bot) \n 
																- /cmds (command list) \n 
																- /st <article> (Straits Times Scrapper)""")
	def aboutme(bot,update):
		bot.sendMessage(chat_id=update.message.chat_id, text="Hi, I was created by my user, @fatalityx to learn more about Python, as well as scrape news articles from websites")

	def straitstimes(bot, update):
		try:

			url=update.message.text
			sturl = url[4:]
			checksturl = sturl[:28]
			print(checksturl)
			if checksturl != "http://www.straitstimes.com/":
				bot.sendMessage(chat_id=update.message.chat_id, text="""Please enter a valid url. For example, http://www.straitstimes.com/<article>""",parse_mode='Markdown')

			else:
				try:
					headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
					result = requests.get(sturl,headers=headers)
					print(result.status_code)
					if (result.status_code >= 400):
						bot.sendMessage(chat_id=update.message.chat_id, text="""This story does not exist!""",parse_mode='Markdown')
					else:
						print('hello')
						headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
						r = requests.get(sturl, headers=headers)
						c = r.content
						soup = BeautifulSoup(c,"html.parser")
						mydivs = soup.findAll("div", { "class" : "odd field-item" })
						titlediv = soup.findAll("h1", {"class" : "headline node-title"})
						publishdiv = soup.findAll("meta", {"property" : "article:published_time"})
						updatediv = soup.findAll("meta", {"property" : "article:modified_time"})
						bodyobject = []
						publishedobject = []
						modifiedobject = []
						for title in titlediv:
							bodyobject.append("*")
							bodyobject.append(title.text)
							bodyobject.append("*")
							bodyobject.append("\n")
							bodyobject.append("\n")
						for postdate in publishdiv:
							publishedobject.append('Published at: ')
							pubdate = parser.parse(postdate['content'])
							publishedobject.append(pubdate.strftime("%B %d, %Y %H:%M"))
						for modidate in updatediv:
							modifiedobject.append('Updated at: ')
							moddate = parser.parse(modidate['content'])
							modifiedobject.append(moddate.strftime("%B %d, %Y %H:%M"))
						bodyobject.append("_")
						bodyobject.extend(publishedobject)
						bodyobject.append("_")
						bodyobject.append("\n")
						bodyobject.append("_")
						bodyobject.extend(modifiedobject)
						bodyobject.append("_")
						bodyobject.append("\n")
						bodyobject.append("\n")
						for div in mydivs:
							blockquote = div.findAll('blockquote')
							for b in blockquote:
								b.decompose()
							a = div.findAll('span')
							for link in a:
								link.decompose()
							p = div.findAll('p',{"class": None})
							for para in p:
								if para.text is not "":
									bodyobject.append(para.text)
									bodyobject.append("\n")
									bodyobject.append("\n")
						str1 = ''.join(bodyobject)
						result = 0
						for char in str1:
							result +=1
						try:
							if (result) > 4096:
								n = 4000
								checklist=["false"]
								while "false" in checklist:
									del checklist[:]
									n = n-1
									msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
									for msg in msglist:
										lastchar = (msg.strip()[-1])
										if msg[-1] not in string.whitespace:
											checklist.append("false")
										else:
											checklist.append("true")
								msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
								for msg in msglist:
									bot.sendMessage(chat_id=update.message.chat_id, text=msg, parse_mode='Markdown')
							else:
								bot.sendMessage(chat_id=update.message.chat_id, text=str1, parse_mode='Markdown')
						except Exception as e: print(e)					
				except Exception as e: print(e)
		except Exception as e: print(e)

