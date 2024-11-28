from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, Forbidden
from responses import get_response
from datetime import datetime

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
VERROLE = 1310671864024272957


intents: Intents = Intents.default()
intents.message_content = True
intents.members = True
client: Client = Client(intents=intents)

# async def send_message(message: Message, user_message: str) -> None:
#     if not user_message:
#         print('(Message was empty because intents were not enabled properly.)')
#         return
    
#     if is_private := user_message[0] == '?':
#         user_message = user_message[1:]


#     try:
#         response: str = get_response(user_message)
#         await message.author.send(response) if is_private else await message.channel.send(response)
#     except Exception as e:
#         print(e)
            

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return
    try:
        dob = message.content.strip()
        birth_date = datetime.strptime(dob, "%d/%m/%Y")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        if age >= 18:
            role = message.guild.get_role(VERROLE)
            if role is None:
                await message.channel.send(f'Role with ID {VERROLE} not found.')
                return
            
            await message.author.add_roles(role)

        else:
            try:
                await message.author.send("You were removed from the server because you must be at least 18 years old to join.")
            except Forbidden:
                await message.channel.send(f"{message.author.mention}, I couldn't DM you. Please enable DMs to receive messages.")

            await message.author.kick(reason="User is under 18 years old")

    except ValueError:
        await message.channel.send('Incorrect format. Please use the DD/MM/YYYY format.')

    except Exception as e:
        await message.channel.send(f"An error occured: {str(e)}")
        
client.run(TOKEN)