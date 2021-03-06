import requests
import time
from gtts import gTTS
from sys import argv, exit
import ssl


def run():
    if len(argv) == 0:
        print('Args list:\n'
              + '-ru If u have problem with connection or telegram is blocked in your country. Uses proxy.\n'
              + '-t "token" to use your bot token (without token you cant use this script).\n')
        return

    # Setup proxies for tg if call arg is '-ru'.
    proxies = {}
    if '-ru' in argv:
        proxies = {
          'https': 'http://207.246.64.79:80',
        }

    # Url of telegram bot api
    url = 'https://api.telegram.org/bot'

    # Get bot token from arg after '-t'.
    if '-t' in argv:
        index = argv.index('-t') + 1
        token = argv[index]
        print('-t given')
    else:
        print('Sorry, we can\'t start bot without a token')
        return

    # All messages before start of script will not be answered.
    # Create list of answered messages id.
    answered_update_id = []

    # Check connection.
    try:
        r = requests.get(url + token + '/getUpdates', proxies=proxies)
    except requests.exceptions.SSLError:
        print('Connection error: try use -ru argument.')
        return

    response = r.json()
    for update in response['result']:
        update_id = update['update_id']
        answered_update_id.append(update_id)
    print("Ignore this ids lower than: ", answered_update_id[-1])

    # Start answer cycle.
    while True:
        # Get new messages.
        r = requests.get(url + token + '/getUpdates', proxies=proxies)
        response = r.json()
        for update in response['result']:
            update_id = update['update_id']
            if update_id not in answered_update_id:
                answered_update_id.append(update_id)
                user_message = update['message']['text'][:1000]
                if user_message == '/start':
                    user_message = 'Напиши любой текст и я его озвучу.'
                if update['message']['from']['id'] == 244378615:
                    user_message = 'коля пук @ коля пук @ коля пук @'
                print("Answering for ", update_id, ' user message is ', user_message[:20])

                # Create mp3 from user message using gTTS.
                tts = gTTS(user_message, lang='ru')
                tts.save('hello.mp3')
                chat_id = update['message']['chat']['id']
                mp3_file = {'audio': open('hello.mp3', 'rb')}
                requests.post(url + token + '/sendAudio?chat_id=' + str(chat_id), proxies=proxies, files=mp3_file)
                print("Send audio result:", r)
        time.sleep(10)


if __name__ == '__main__':
    run()
