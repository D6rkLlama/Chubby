import discord, requests, json, os, datetime

if not os.path.exists('data'):
    os.makedirs('data')

if os.path.exists('data/user_data.json'):
    with open('data/user_data.json', 'r') as f:
        user_data = json.load(f)
else:
    user_data = {}


def save_user_data():
    with open('data/user_data.json', 'w') as f:
        json.dump(user_data, f)


def get_meme():
    response = requests.get('https://meme-api.com/gimme')
    json_data = json.loads(response.text)
    return json_data['url']


intents = discord.Intents.default()
intents.message_content = True

current_datetime = datetime.datetime.now()
    

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return

        # XP add
        user_id = str(message.author.id)
        user_data.setdefault(user_id, {'xp': 0, 'level': 1})
        user_data[user_id]['xp'] += 1

        # Did the user level up?
        if user_data[user_id]['xp'] >= user_data[user_id]['level'] * 30:
            user_data[user_id]['level'] += 1
            await message.channel.send(
                f'Congratulations {message.author.mention}! You leveled up to level {user_data[user_id]["level"]}!')

        save_user_data()  # Save user data after every message

        # Meme stuff
        if message.content.startswith('$meme'):
            await message.channel.send(get_meme())

        # Hello stuff
        if message.content.startswith('$hello'):
            await message.channel.send(f'Hello {message.author.mention} ! Hope you have a great day :)')

        
        #Date stuff
        if message.content.startswith('$date'):
            await message.channel.send('Current date and time: ' + str(current_datetime) )
  
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('Sorry not giving u my bot token :P')  
