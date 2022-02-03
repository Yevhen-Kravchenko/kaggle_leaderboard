import logging
import kaggle
import zipfile
import csv
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

BOT_TOKEN = ""

def start(update, context):

    update.message.reply_text('Hi!')


def top10(update, context):
    
    os.system('kaggle competitions leaderboard --download -c new-york-city-taxi-fare-prediction -p ./leaderboard')
    
    with zipfile.ZipFile("leaderboard/new-york-city-taxi-fare-prediction.zip","r") as zip_ref:
        zip_ref.extractall("")

    with open('new-york-city-taxi-fare-prediction-publicleaderboard.csv', mode='r') as infile:
        reader = csv.reader(infile)
        leaders = [rows[1] + ' : ' + rows[3] for rows in reader]

    update.message.reply_text('\n'.join(leaders[:10]))
    
def top_UCU(update, context):
    
    os.system('kaggle competitions leaderboard --download -c new-york-city-taxi-fare-prediction -p ./leaderboard')
    
    with zipfile.ZipFile("leaderboard/new-york-city-taxi-fare-prediction.zip","r") as zip_ref:
        zip_ref.extractall("")
        
    with open("ucu_teams.txt") as file:
        ucu_teams = file.readlines()
        ucu_teams = [t.strip() for t in ucu_teams]

    with open('new-york-city-taxi-fare-prediction-publicleaderboard.csv', mode='r') as infile:
        reader = csv.reader(infile)
        leaders = [[rows[1], rows[3]] for rows in reader]
    
    leaders_UCU = [line[0] + ' : ' + line[1] for line in leaders if line[0] in ucu_teams]

    update.message.reply_text('\n'.join(leaders_UCU))
    
    
def add(update, context):
    team_name = update.message.text
    team_name = team_name.split(' ', 1)[1]
    with open('ucu_teams.txt', 'a') as file:
        file.write(team_name + '\n')
    update.message.reply_text(team_name + " added to the list of UCU teams")

    
def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("top10", top10))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("top_UCU", top_UCU))
    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
