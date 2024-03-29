# These are all the modules we will be using! Continue to add to them as we expand the Bot!
import asyncio
import random
import discord
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext import commands
import os
from dotenv import load_dotenv
import yt_dlp
import requests


#Let's grab the .env file (If you do not have one, I suggest making one!)
load_dotenv()
####################################### This is where we set up all of out API's that we are gonna use ###################################
#Make sure to comment the API your setting up

#Discord Setup
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
bot.remove_command("help")

#Spotify Setup
spotifyClientID = (os.getenv('SPOTIFY_CLIENT_ID'))
spotifyClientSecret = (os.getenv('SPOTIFY_CLIENT_SECRET'))
client_credentials_manager = SpotifyClientCredentials(client_id=spotifyClientID, client_secret=spotifyClientSecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#Giphy Setup
giphyAPIKey = (os.getenv('GIPHY_API_KEY'))
########################################################################################################################################

#This is a bot command, give it a try in discord! Type "$top5 Drake" If the artist is a 2 word name, surround them in quotes
#Command to get the top5 tracks from an artist - Might not work for some due to the search algorithm provided by spotipy
@bot.command(name='top5')
async def top5(ctx, arg):
    arg = arg.upper()
    result = sp.search(q=f'artists: {arg}', type='artist', limit=50, market=None)
    if result['artists']['total'] == 0:
        arg = arg.lower()
        result = sp.search(q=f'artists: {arg}', type='artist', limit=50, market=None)

    # Check if any artists are found
    if not result['artists']['items']:
        #await ctx.send(f"No artists found for '{arg}'.")
        return

    # Find the matching artist
    artist_id = None
    artist_name = None
    for artist in result['artists']['items']:
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
         await ctx.send(f"No artist found with the name '{arg}'.")
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
        
# Command to Join the Channel of the Requestor
@bot.command(name="join")
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()
# Command to Leave the Channel
@bot.command(name="leave")
async def leave(ctx):
    await ctx.voice_client.disconnect()
# Command to stop any audio coming from the bot
@bot.command(name="stop")
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client.is_playing():
        voice_client.stop()
# Command to play requested song by mp3 file/youtube url
@bot.command(name="play")
async def play(ctx, source):
    voice_channel = ctx.author.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not voice_client.is_connected:
        await voice_channel.connect()

    if voice_client.is_playing():
        voice_client.stop()

    if source.startswith("http"):
        # If the source is a YouTube URL
        ydl_opts = {'format': 'bestaudio'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(source, download=False)
            url = info['formats'][0]['url']
            source = discord.FFmpegPCMAudio(url)
            
    else:
        # If the source is a local file
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source), volume=0.5)

    voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)


# New command to get a random dog image
@bot.command(name='randomdog')
async def random_dog(ctx):
    # Dog API endpoint for random dog images
    dog_api_url = 'https://dog.ceo/api/breeds/image/random'

    # Make a GET request to the Dog API
    response = requests.get(dog_api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Get the URL of the random dog image
        dog_image_url = data['message']

        # Send the dog image to the Discord channel
        await ctx.send(f"Here's a random dog for you: {dog_image_url}")
    else:
        await ctx.send("Sorry, I couldn't fetch a random dog image at the moment. Try again later.")

# New command to get a random joke
@bot.command(name='joke')
async def joke(ctx):
    # Joke API endpoint for joke
    joke_url = 'https://official-joke-api.appspot.com/random_joke'

    #make a GET request for the joke api
    response = (requests.get(joke_url))
    # chekc if the request was succesful (status code 200)
    if response.status_code == 200:
        # this just parses the data and send it to the channel
        data = response.json()
        setup = data["setup"]
        punchline = data["punchline"]
        await ctx.send(f"{setup}\n{punchline}")
    else:
        await ctx.send("Failed to retrieve joke, Sorry :(")

@bot.command(name='gif')
async def gif(ctx, *search_terms):
    # Convert search terms to a single string
    query = ' '.join(search_terms)
    
    # Get a random offset to fetch a random GIF
    offset = random.randint(0, 100)

    # Giphy API endpoint URL
    api_url = f'https://api.giphy.com/v1/gifs/search?q={query}&api_key={giphyAPIKey}&limit=1&limit=1&offset={offset}'

    # Make a GET request to the Giphy API
    response = requests.get(api_url)

    if response.status_code == 200:
        # Parse the JSON response
        gif_data = response.json()
        gif_url = gif_data['data'][0]['images']['original']['url']  # Adjust this based on the actual JSON structure

        # Send the GIF to the Discord channel
        await ctx.send(gif_url)
    else:
        await ctx.send('Failed to fetch a GIF. Please try again later.')



# This logs in the console that the bot is ready
# To Clarify, The @bot.event looks for the specified event, such as on_ready
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print('Below in the console is all the Chat logs for the bot. Included is the Channel it came from, the user that sent the message,  and the message itself ')



# This function looks into the messages for either keywords or entire messages depending on its implimentation
# Keep in mind, this runs everytime a message is sent, including its own, so make sure to keep the first
# conditional statement to ensure the bot doesnt respond to itself, but otherwise, add your own implimentations!
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    print(str(message.guild.name) + " - " + str(message.channel) + " - " + str(message.author) + ": " + message.content)
    if message.content.lower().startswith('hey genova,'):
        author = message.author
        channel = message.channel
        async with message.channel.typing():
            await asyncio.sleep(2)
        await message.channel.send("What's Up?")
        message = await bot.wait_for('message')
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
    if "say hi genova!" in message.content.lower():
        await message.add_reaction('😀')
        async with message.channel.typing():
            await asyncio.sleep(2)
        await message.channel.send("Hi Everyone, Glad to be here!")
    if "tell us about yourself genova" in message.content.lower():
        async with message.channel.typing():
            await asyncio.sleep(4)
        await message.channel.send("Im a discord bot! I was created to be an open source project to be an up to date example \
about how to create a discord bot and use different API's to increase my functionality. You can find more information \
here: https://github.com/Jordan-Scherf/Genova_DiscordBot")

############################################# This Section is for the help command #######################################################################################
# This section takes a bit of explaing but go ahead and run the "$help" command in your server and see what shows up, you can follow whats happening from there
@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "Help", description = "Use $help <command> for extended description of the command", color = discord.Color.from_rgb(255, 0, 0))

    em.add_field(name = "Spotify", value = "top5")
    em.add_field(name = "Voice Channel", value = "join, leave")
    em.add_field(name = "Youtube/Audio", value = "play, stop")
    em.add_field(name= "Text/Images", value="joke, gif")

    await ctx.send(embed = em)

@help.command()
async def top5(ctx):
    em = discord.Embed(title = "Top5", description = "Displays the Top 5 songs from the given artist", color = discord.Color.from_rgb(255, 51, 255))
    em.add_field(name = "**Syntax**", value = "$top5 <artist>")
    await ctx.send(embed = em)


@help.command()
async def join(ctx):
    em = discord.Embed(title = "Join", description = "Joins the Current Voice Channel of the Requestor", color = discord.Color.from_rgb(255, 51, 255))
    em.add_field(name = "**Syntax**", value = "$join")
    await ctx.send(embed = em)

@help.command()
async def leave(ctx):
    em = discord.Embed(title = "Leave", description = "Leaves the Current Channel the Bot is Currently In", color = discord.Color.from_rgb(255, 51, 255))
    em.add_field(name = "**Syntax**", value = "$Leave")
    await ctx.send(embed = em)

@help.command()
async def play(ctx):
    em = discord.Embed(title = "Play", description = "Plays audio from either a preloaded mp3 file or a youtube link (IMPORTANT: Youtube links not working at the moment)", color = discord.Color.from_rgb(255, 51, 255))
    em.add_field(name = "**Syntax**", value = "$play <mp3 file/url>")
    await ctx.send(embed = em)

@help.command()
async def stop(ctx):
    em = discord.Embed(title = "Stop", description = "Stops any current audio coming from the bot", color = discord.Color.from_rgb(255, 51, 255))
    em.add_field(name = "**Syntax**", value = "$stop")
    await ctx.send(embed = em)  

@help.command()
async def joke(ctx):
    em = discord.Embed(title = "Joke", description = "Sends a random joke to the text channel it was requested from", color = discord.Color.from_rgb(255, 51, 255))
    em.add_field(name = "**Syntax**", value = "$joke")
    await ctx.send(embed = em)  

@help.command()
async def gif(ctx):
    em = discord.Embed(title = "gif", description = "Sends a random gif based on the query to the channel it was requested from", color = discord.Color.from_rgb(255, 51, 255))
    em.add_field(name = "**Syntax**", value = "$gif <query>")
    await ctx.send(embed = em)      


#########################################################################################################################################################################


# This allows the bot to run commands
bot.run(os.getenv('DISCORD_TOKEN'))
