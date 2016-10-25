import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
from telegram import (ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)


from selenium import webdriver ##Imports the selenium web driver
driver = webdriver.Firefox() ##Create a Firefox Webdriver

url = "https://www.google.com/finance"


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



update_id = None

def main():
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot('242123094:AAEiPIxnQ5eoeXyTvRXh1vdWzE92HsD71JA')
    
    '''
    updater = Updater("242123094:AAEiPIxnQ5eoeXyTvRXh1vdWzE92HsD71JA")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    ''' # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1
#def start():
    
def echo(bot):
    global update_id
    # Request updates after the last update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        # chat_id is required to reply to any message
        chat_id = update.message.chat_id
        update_id = update.update_id + 1
	answer=StockVal(bot,update.message.text)
        if update.message:  # your bot can receive updates without messages
            # Reply to the message
		#if answer[0]==0:
            		update.message.reply_text(answer[1])
	
'''
def multi(bot,answer):
    global update_id
    # Request updates after the last update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        # chat_id is required to reply to any message
        chat_id = update.message.chat_id
        update_id = update.update_id + 1
	
   	print "if ch he"
        if update.message:  
		update.message.reply_text(answer)
'''
            
def StockVal(bot,stock):
	driver.get(url)
	

	continue_link = driver.find_element_by_xpath("//input[@id='gbqfq']") 
	continue_link.clear()
	continue_link.send_keys(stock)

	print driver.find_elements_by_css_selector(".gbqfi")[0].click()

	if stock == "/start" :
		strng =  'Welcome to IndiaStock bot. Hi! I am Tarun, naam toh suna hi hoga.... Put in any commodity and you will be told about its values on the National/Bombay Stock Exchange.  NOTE : If the commodity is listed in both NSE and  BSE the stock value tod shall be from BSE.'
		return [0,strng]


	
	lst_all=""
	try:
		i=1
		while i>0:
			drs = 	"//a[@id='rc-"+str(i)+"']"
				
			continue_link = driver.find_element_by_xpath(drs)
			com_ls = continue_link.text
			print "hello"
			lst_all += str(i)+" "+com_ls+"\n"
			
			#multi(bot,lst_all)
			i+=1
		
	except:
		if lst_all != "":
			return [1,lst_all]
		print "Found Directly"
	
	

	try:
		continue_link = driver.find_element_by_xpath("//div[@class= 'appbar-snippet-primary' ]")
		nameStock = continue_link.text
		print nameStock


		continue_link = driver.find_element_by_xpath("//span[@class='pr']")
		value = continue_link.text
		return [0,value+"\n"+nameStock]
	except:
		strng = "Commodity not found. "
		return [0,strng]


if __name__ == '__main__':
    main()
