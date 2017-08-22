from telegram.ext import Updater
import requests
import string
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser
from telegram.utils.helpers import escape_html, escape_markdown
import html2text
import html

class Commands():
	def supported (bot,update):
		bot.sendMessage(chat_id=update.message.chat_id, text="""Hi, these are the sites currently supported by Matilda \nPlease type /cmd for more information! \n- Straits Times \n- TodayOnline \n- CNA \n- Mothership""", parse_mode='Markdown')
	def commands (bot,update):
		bot.sendMessage(chat_id=update.message.chat_id, text="""Hi, this are the commands that I currently support \n- /aboutme (about the bot) \n- /cmd (command list) \n- /st <article> (Straits Times Scraper) \n- /today <article> (TodayOnline Scraper) \n- /cna <article> (Channel News Asia Scraper) \n- /laobu <article> (Mothership.sg Scraper)""", parse_mode='Markdown')
	def aboutme(bot,update):
		bot.sendMessage(chat_id=update.message.chat_id, text="Hi, I was created by my user, @fatalityx to learn more about Python, as well as scrape news articles from websites")

	def straitstimes(bot, update):
		try:

			url=update.message.text
			sturl = url[4:]
			checksturl = sturl[:28]
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
									parastring = escape_markdown(para.text)
									bodyobject.append(parastring)
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
	def todayonline(bot, update):
		try:

			url=update.message.text
			todayurl = url[7:]
			checktodayurl = todayurl[:27]
			if checktodayurl != "http://www.todayonline.com/":
				bot.sendMessage(chat_id=update.message.chat_id, text="""Please enter a valid url. For example, http://www.todayonline.com/<article>""",parse_mode='Markdown')

			else:
				try:
					headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
					result = requests.get(todayurl,headers=headers)
					print(result.status_code)
					if (result.status_code >= 400):
						bot.sendMessage(chat_id=update.message.chat_id, text="""This story does not exist!""",parse_mode='Markdown')
					else:
						headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
						r = requests.get(todayurl, headers=headers)
						c = r.content
						soup = BeautifulSoup(c,"html.parser")
						mydivs = soup.findAll("div", { "class" : "content" })
						titlediv = soup.findAll("meta", {"property" : "og:title"})
						publishdiv = soup.findAll("div", {"class" : "authoring full-date"})
						updatediv = soup.findAll("meta", {"property" : "article:modified_time"})
						bodyobject = []
						publishedobject = []
						modifiedobject = []
						dateval = soup.findAll("span", {"class" : "date-value"})
						dateobj = []
						for date in dateval:
							dt = parser.parse(date.text)
							dateobj.append(dt)
						if len(dateobj) > 1:
							pubdate = min(dateobj)
							moddate = max(dateobj)
						else:
							pubdate = min(dateobj)
						for title in titlediv:
							articletitle = title['content']
							bodyobject.append("*")
							bodyobject.append(articletitle)
							bodyobject.append("*")
							bodyobject.append("\n")
							bodyobject.append("\n")
						for postdate in publishdiv:
							datelbl = postdate.findAll("span", {"class" : "date-label"})
							for lbl in datelbl:
								print(lbl.text)
								if "Published:" in lbl.text:
									publishedobject.append('Published at: ')
									publishedobject.append(pubdate.strftime("%B %d, %Y %H:%M"))
								else:
									modifiedobject.append('Updated at: ')
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
							s = div.findAll('sup')
							for sup in s:
								sup.decompose()
							p = div.findAll('p',{"class": None})
							for para in p:
								if para.text is not "":
									parastring = escape_markdown(para.text)
									bodyobject.append(parastring)
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
	def cna(bot, update):
		try:
			url=update.message.text
			cnaurl = url[5:]
			checkcnaurl = cnaurl[:31]
			if checkcnaurl != "http://www.channelnewsasia.com/":
				bot.sendMessage(chat_id=update.message.chat_id, text="""Please enter a valid url. For example, http://www.channelnewsasia.com/<article>""",parse_mode='Markdown')

			else:
				try:
					headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
					result = requests.get(cnaurl,headers=headers)
					print(result.status_code)
					if (result.status_code >= 400):
						bot.sendMessage(chat_id=update.message.chat_id, text="""This story does not exist!""",parse_mode='Markdown')
					else:
						headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
						r = requests.get(cnaurl, headers=headers)
						c = r.content
						soup = BeautifulSoup(c,"html.parser")
						mydivs = soup.findAll("div", { "class" : "c-rte--article" })
						titlediv = soup.findAll("h1", {"class" : "article__title"})
						publishdiv = soup.findAll("meta", {"name" : "cXenseParse:recs:publishtime"})
						updatediv = soup.findAll("time")
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
							if modidate['datetime'] is not '':
								modifiedobject.append('Updated at: ')
								modifdate = parser.parse(modidate['datetime'])
								modifiedobject.append(modifdate.strftime("%B %d, %Y %H:%M"))
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
							br = div.findAll('br/')
							for b in br:
								b.decompose()
							innerdiv = div.findAll('div')
							for inn in innerdiv:
								inn.decompose()	
							strong = div.findAll('strong')
							for s in strong:
								s.decompose()	
							a = div.findAll('span')
							for link in a:
								link.decompose()
							f = div.findAll('figure')
							for figure in f:
								figure.decompose()
							pic = div.findAll('div',{"data-css":"c-picture"})
							for picture in pic:
								picture.decompose()
							p = div.findAll('p',{"class": None})
							for para in p:
								if para.text is not "":
									if para.text.strip() is not "":
										parastring = escape_markdown(para.text)
										#strip1 = parastring.replace("*","")
										#strip2 = strip1.replace("_","")
										#strip3 = strip2.replace("`","")
										bodyobject.append(parastring)
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
								print(str1)
								bot.sendMessage(chat_id=update.message.chat_id, text=str1, parse_mode='Markdown')
						except Exception as e: print(e)					
				except Exception as e: print(e)
		except Exception as e: print(e)
	def laobu(bot, update):
		try:

			url=update.message.text
			msurl = url[7:]
			checkmsurl = msurl[:22]
			if checkmsurl != "https://mothership.sg/":
				bot.sendMessage(chat_id=update.message.chat_id, text="""Please enter a valid url. For example, https://mothership.sg/<article>""",parse_mode='Markdown')

			else:
				try:
					headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
					result = requests.get(msurl,headers=headers)
					print(result.status_code)
					if (result.status_code >= 400):
						bot.sendMessage(chat_id=update.message.chat_id, text="""This story does not exist!""",parse_mode='Markdown')
					else:
						headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
						r = requests.get(msurl, headers=headers)
						c = r.content
						soup = BeautifulSoup(c,"html.parser")
						mydivs = soup.findAll("div", { "class" : "content-article-wrap" })
						subtitlediv = soup.findAll("div", { "class" : "article original" })
						titlediv = soup.findAll("meta", {"property" : "og:title"})
						bodyobject = []
						publishedobject = []
						modifiedobject = []
						for title in titlediv:
							bodyobject.append("*")
							bodyobject.append(title['content'])
							bodyobject.append("*")
							bodyobject.append("\n")
						for sub in subtitlediv:
							header = sub.findAll('div',{"class":"header"})
							bar= sub.findAll('div',{"class":"side-bar"})
							for side in bar:
								side.decompose()
							adv = sub.findAll('div',{"class":"related-stories"})
							for ad in adv:
								ad.decompose()
							rel = sub.findAll('div',{"class":"related-articles"})
							for re in rel:
								re.decompose()
							for p in header:
								pclass = p.findAll('p',{"class":"subtitle"})
								for pc in pclass:
									bodyobject.append(pc.text)
									bodyobject.append("\n")
									bodyobject.append("\n")
							for date in header:
								dclass = date.findAll('span',{"class":"publish-date"})
								for d in dclass:
									publishedobject.append("Published: ")
									publishedobject.append(d.text)
						bodyobject.append("_")
						bodyobject.extend(publishedobject)
						bodyobject.append("_")
						bodyobject.append("\n")
						bodyobject.append("\n")
						for div in mydivs:
							adv = div.findAll('div')
							for ad in adv:
								ad.decompose()
							fig = div.findAll('figure')
							for f in fig:
								f.decompose()
							htmltext = str(div)
							newhtmltext = htmltext[33:]
							h = html2text.HTML2Text()
							h.ignore_links = True
							handledtext = h.handle(newhtmltext)
							h3 = div.findAll('h3')
							if len(h3) > 0:
								for each in h3:
									text = each.text
									replacement = "*"+text+"*"
									print(replacement)
									div.h3.replace_with(replacement)
							h4 = div.findAll('h4')
							if len(h4) > 0:
								for each in h4:
									text = each.text
									replacement = "*"+text+"*"
									print(replacement)
									div.h4.replace_with(replacement)
							h5 = div.findAll('h5')
							if len(h5) > 0:
								for each in h5:
									text = each.text
									replacement = "*"+text+"*"
									print(replacement)
									div.h5.replace_with(replacement)
							h1 = div.findAll('h1')
							if len(h1) > 0:
								for each in h1:
									text = each.text
									replacement = "*"+text+"*"
									print(replacement)
									div.h1.replace_with(replacement)
							h2 = div.findAll('h2')
							if len(h2) > 0:
								for each in h2:
									text = each.text
									replacement = "*"+text+"*"
									print(replacement)
									div.h2.replace_with(replacement)
							bodyobject.append(div.text)
							bodyobject.append("\n")
							bodyobject.append("\n")
						str1 = ''.join(bodyobject)
						result = 0
						for char in str1:
							result +=1
						
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
							bot.sendMessage(chat_id=update.message.chat_id, text=str1, parse_mode= 'Markdown')
				except:
					headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
					result = requests.get(msurl,headers=headers)
					print(result.status_code)
					if (result.status_code >= 400):
						bot.sendMessage(chat_id=update.message.chat_id, text="""This story does not exist!""",parse_mode='Markdown')
					else:
						headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
						r = requests.get(msurl, headers=headers)
						c = r.content
						soup = BeautifulSoup(c,"html.parser")
						mydivs = soup.findAll("div", { "class" : "content-article-wrap" })
						subtitlediv = soup.findAll("div", { "class" : "article original" })
						titlediv = soup.findAll("meta", {"property" : "og:title"})
						bodyobject = []
						publishedobject = []
						modifiedobject = []
						for title in titlediv:
							bodyobject.append("*")
							bodyobject.append(title['content'])
							bodyobject.append("*")
							bodyobject.append("\n")
						for sub in subtitlediv:
							header = sub.findAll('div',{"class":"header"})
							bar= sub.findAll('div',{"class":"side-bar"})
							for side in bar:
								side.decompose()
							adv = sub.findAll('div',{"class":"related-stories"})
							for ad in adv:
								ad.decompose()
							rel = sub.findAll('div',{"class":"related-articles"})
							for re in rel:
								re.decompose()
							for p in header:
								pclass = p.findAll('p',{"class":"subtitle"})
								for pc in pclass:
									bodyobject.append(pc.text)
									bodyobject.append("\n")
									bodyobject.append("\n")
							for date in header:
								dclass = date.findAll('span',{"class":"publish-date"})
								for d in dclass:
									publishedobject.append("Published: ")
									publishedobject.append(d.text)
						bodyobject.append("_")
						bodyobject.extend(publishedobject)
						bodyobject.append("_")
						bodyobject.append("\n")
						bodyobject.append("\n")
						for div in mydivs:
							adv = div.findAll('div')
							for ad in adv:
								ad.decompose()
							fig = div.findAll('figure')
							for f in fig:
								f.decompose()
							htmltext = str(div)
							newhtmltext = htmltext[33:]
							h = html2text.HTML2Text()
							h.ignore_links = True
							handledtext = h.handle(newhtmltext)
							h3 = div.findAll('h3')
							if len(h3) > 0:
								for each in h3:
									text = each.text
									replacement = "*"+text+"*"
									print(replacement)
									div.h3.replace_with(replacement)
							h4 = div.findAll('h4')
							if len(h4) > 0:
								for each in h4:
									text = each.text
									replacement = "*"+text+"*"
									print(replacement)
									div.h4.replace_with(replacement)
							h5 = div.findAll('h5')
							if len(h5) > 0:
								for each in h5:
									text = each.text
									replacement = "*"+text+"*"
									print(replacement)
									div.h5.replace_with(replacement)
							h1 = div.findAll('h1')
							if len(h1) > 0:
								for each in h1:
									text = each.text
									replacement = "*"+text+"*"
									print(replacement)
									div.h1.replace_with(replacement)
							h2 = div.findAll('h2')
							if len(h2) > 0:
								for each in h2:
									text = each.text
									replacement = "*"+text+"*"
									print(replacement)
									div.h2.replace_with(replacement)
							bodyobject.append(escape_markdown(div.text))
							bodyobject.append("\n")
							bodyobject.append("\n")
						str1 = ''.join(bodyobject)
						result = 0
						for char in str1:
							result +=1
						
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
							bot.sendMessage(chat_id=update.message.chat_id, text=str1, parse_mode= 'Markdown')
		except Exception as e: print(e)
