import asyncio
import discord
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext import commands
import os
from dotenv import load_dotenv

#Let's grab the .env file
load_dotenv()

#Discord Setup
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True  # Fix: Correct attribute name
#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)
#Spotify Setup
spotifyClientID = (os.getenv('SPOTIFY_CLIENT_ID'))
spotifyClientSecret = (os.getenv('SPOTIFY_CLIENT_SECRET'))
client_credentials_manager = SpotifyClientCredentials(client_id=spotifyClientID, client_secret=spotifyClientSecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

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

@bot.command(name='top5')
async def top5(ctx, arg):
    print("In command" + arg)
    result = sp.search(q=f'artists: {arg}', type='artist', limit=50, market='US')
    print(result['artists']['items'])
    for artist in result['artists']['items'][:50]:
        if(artist['name'] == arg):
            #Testing print
            #print('{:<20} {:>10}'.format(artist['name'], artist['id']))
            artist_name = artist['name']
            artist_id = artist['id']
        else:
            await ctx.send("Artist Not Found")
    top_tracks = sp.artist_top_tracks(artist_id, country='US')

    if not top_tracks['tracks']:
        await ctx.send("No top tracks found for the artist.")
        return

    await ctx.send(f"Top 5 songs for the artist {artist_name}):")
    for i, track in enumerate(top_tracks['tracks'][:5]):
        await ctx.send(f"{i + 1}. {track['name']} - {', '.join(artist['name'] for artist in track['artists'])}")


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