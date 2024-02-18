# Genova Discord Bot

Genova is a Discord bot that serves as an open-source project for beginner Python programmers to practice and learn about Python programming and API integration. Fork the repository and contribute to this project!

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [IMPORTANT](#important)
- [Resources](#resources)
- [License](#license)

## Introduction

Genova is designed to be a beginner-friendly Discord bot, welcoming contributions from the community to enhance its functionality. Whether you are new to Python or looking to gain experience with API integration, Genova provides an opportunity to learn and contribute to an open-source project. To learn the basics of the Discord API and how to get your own Discord Token, look at the *Resources* section below.

## Features

- **Spotipy**
  - Fetches and displays the top 5 songs of a specified artist on Spotify.
  - Responds to specific commands in Discord channels.
  - Uses the Discord and Spotify APIs for functionality.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3
- Discord.py library
- Spotipy library
- Spotify Developer account with client ID and client secret
- Discord bot token
- `.env` file with necessary credentials (do not share or commit this file)

## Installation

1. Clone the repository:
   '''git clone https://github.com/your-username/genova-discord-bot.git'''
   Make sure you've forked this original repository first!

2. Install Dependencies:
    '''pip install -r requirements.txt'''

3. Create a '.env' file within your project folder with these tokens  
    DISCORD_TOKEN='[Insert Token]'  
    SPOTIFY_CLIENT_ID='[Insert Token]'  
    SPOTIFY_CLIENT_SECRET='[Insert Token]'  
    *Keep in mind, you must have the tokens in order for the bot to run successfully, also add the file to your ".gitignore" file in order to prevent leaking your tokens for others to use and abuse*

4. Run the bot:
    python Genova.py

## Usage

To use the bot, first run the bot and when its connected to a server, go to a usable text channel and type a command that has been programmed. For example, the command for using the spotipy API to find the top 5 songs for an artist is "$top5 <Artist>", where '$' is the prefix for commands. As more commands are created that use different API's, Please continue to folow this syntax!

Sometimes, however, the bot can respond to things typed in chat normally without the prefix for commands. This is heavily dependent on what is programmed for the bot! Users can use the example in the on_message() event function in the Genova.py file.

Experiment with everything the discord API has to offer and mix it with other API's to create useful tools you can use in your own discord server.

## Contributing

If you would like to contribute to Genova to add more API examples/Usages and expand open information already available:

1. Fork the Repository

2. Add your contributions to your forked repository

3. Press "Contribute" in your forked repository and submit it to the Staging Branch! * This creates a "Pull Reqeust"

4. After review, the Pull Request may be approved or denied based on various reasons such as Improper Syntax, Innopropriate Content, Bad Documentation, etc. After the Pull Request is approved, it will be moved into staging for more testing before being commited into main!

## IMPORTANT

If you submit a contribution that includes more modules/dependencies for the project, make sure you add that to the requiements.txt! This allows for *easier* installation in the future. Also if their was a resource you used to create the use for your API for Genova, please link it in the Resources Section in the README.md file or link it in your pull request!

## Resources
Discord API and Token Walkthrough: [RealPython - Discord Bot](https://realpython.com/how-to-make-a-discord-bot-python/)  
Discord.py Documentation: [Discord.py](https://discordpy.readthedocs.io/en/latest/intro.html)  
Spotipy API and Spotify Developer Token: [Spotipy: How to Guide](https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b)  
Spotipy Documenation: [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/)


