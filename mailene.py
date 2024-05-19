from discord import Intents, Client, Message
import messages
import meetings
import config

intents: Intents = Intents.default()
intents.message_content = True
client: Client  = Client(intents=intents)


async def handleMessage(msg: Message, userMessage: str) -> None:

    if not checkAllowedChannelID(msg.channel.id):
        return

    if not userMessage:
        return
    
    if userMessage.startswith('!'):
        try:
            resp = getResponse(userMessage)
            await msg.channel.send(resp)
        except Exception as e:
            print(e)
    
async def sendReminder(msg: str):
    try:
        channel = client.get_channel(config.TEST_CHANNEL_ID)
        await channel.send(msg)
    except Exception as e:
        print(e)


def checkAllowedChannelID(channelID: int) -> bool:
    return channelID == config.CHANNEL_ID or channelID == config.TEST_CHANNEL_ID


def getResponse(input: str) -> str:
    msg = input.lower()
    command = msg.split(' ')[0][1:]

    match command:
        case 'help' | 'h' | 'hjælp':
            return handleHelpMessage()

        case 'meet' | 'meeting' | 'møde' | 'm':
            return handleNewMeeting()

        case 'emailstart' | 'email_start':
            return handleEmailStartReminder()

        case 'emailstop' | 'email_stop':
            return handleEmailEndReminder()

        case _:
            raise NotImplementedError()


def handleHelpMessage():
    return messages.helpMessage

def handleNewMeeting():
    # https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day
    meetings.createNewMeeting

def handleEmailStartReminder():
    pass

def handleEmailEndReminder():
    pass


@client.event
async def on_ready():
    print('Mailéne løber!')
    meetings.loadMeetingsAfterBoot()

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return
    
    await handleMessage(message, message.content)


def main() -> None:
    client.run(token=config.BOT_TOKEN)

if __name__ == '__main__':
    main()








