# These are all the modules we will be using! Continue to add to them as we expand the Bot!
import asyncio
import discord
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext import commands
import os
from dotenv import load_dotenv

#Let's grab the .env file (If you do not have one, I suggest making one!)
load_dotenv()

#Discord Setup
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True  # Fix: Correct attribute name
bot = commands.Bot(command_prefix='$', intents=intents)
#Spotify Setup
spotifyClientID = (os.getenv('SPOTIFY_CLIENT_ID'))
spotifyClientSecret = (os.getenv('SPOTIFY_CLIENT_SECRET'))
client_credentials_manager = SpotifyClientCredentials(client_id=spotifyClientID, client_secret=spotifyClientSecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

####################This is for the OpenAI API, which isnt currently in use###############################
#Cannot use until money is payed :(
# @bot.command()
# async def test(ctx, arg):
#     completion = openaiClient.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helper bot in a discord named Genova."},
#             {"role": "user", "content": {arg}}
#         ]
#     )
#     await ctx.send(completion.choices[0].message)
##########################################################################################################

#This is a bot command, give it a try in discord! Type "$top5 "Drake"" - make sure the artist is in q
@bot.command(name='top5')
async def top5(ctx, arg):
    offsetNumber = 0
    while True:
        arg = arg.upper()
        print("In command" + arg)
        result = sp.search(q=f'artists: {arg}', type='artist', limit=50, offset= offsetNumber, market=None)
        if result['artists']['total'] == 0:
            arg = arg.lower()
            result = sp.search(q=f'artists: {arg}', type='artist', limit=50, offset= offsetNumber , market=None)

        # Check if any artists are found
        if not result['artists']['items']:
            #await ctx.send(f"No artists found for '{arg}'.")
            return

        # Find the matching artist
        artist_id = None
        artist_name = None
        for artist in result:
            print(result[artist])
        for artist in result['artists']['items']:
            print('{:<20} {:>10}'.format(artist['name'], artist['id'], int(artist['popularity'])))
            if artist['name'].lower() == arg and int(artist['popularity']) > 40:
                artist_name = artist['name']
                artist_id = artist['id']
                break
            elif artist['name'].upper() == arg and int(artist['popularity']) > 40: 
                artist_name = artist['name']
                artist_id = artist['id']
                break
        # Check if a matching artist was found
        if artist_id is None:
           # await ctx.send(f"No artist found with the name '{arg}'.")
            offsetNumber = offsetNumber + 1
        else:
            # Retrieve top tracks for the artist
            top_tracks = sp.artist_top_tracks(artist_id, country='US')
            if not top_tracks['tracks']:
                await ctx.send("No top tracks found for the artist.")
            else:# Send the top 5 tracks to the Discord channel
                await ctx.send(f"Top 5 songs for the artist {artist_name}:")
                for i, track in enumerate(top_tracks['tracks'][:5]):
                    await ctx.send(f"{i + 1}. {track['name']} - {', '.join(artist['name'] for artist in track['artists'])}")
                return
        



@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return

    if message.content.lower().startswith('hey genova,') or \
       message.content.lower().startswith('genova'):
        author = message.author
        channel = message.channel
        async with message.channel.typing():
            await asyncio.sleep(2)
        await message.channel.send("What's Up?")
        message = await bot.wait_for('message')
        print(message.content)
        if message.author == author and message.channel == channel \
        and 'songs by' in message.content.lower():
            async with message.channel.typing():
                await asyncio.sleep(2)
            await message.channel.send("Unfortunatley, You must use the command '$Top5' <Artist Name>")
        else:
            async with message.channel.typing():
                await message.add_reaction('😭')
                await asyncio.sleep(2)
            await message.channel.send("*i dont know how to do that*")







# This allows the bot to run commands
bot.run(os.getenv('DISCORD_TOKEN'))
# This allows it to scan chat and whatnot    
#client.run(os.getenv('DISCORD_TOKEN'))