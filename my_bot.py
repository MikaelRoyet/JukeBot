# Work with Python 3.6
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord import opus
from discord import Game
import asyncio
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import names
import sys
import pprint
import spotipy    # la librairie pour manipuler l'api spotify
import spotipy.util as util
import simplejson as json  #pour manipuler les réponses json
import time  #pour créer une playlist horodatée
from datetime import datetime
from random import shuffle #pour attribuer un classement aléatoire aux morceaux
import spotipy.oauth2 as oauth2
from discord.ext import commands
prefix = "!"
bot = commands.Bot(command_prefix=prefix)

username="JukeBot"
clientId= "a59b157c52974cb4a79a865279f9eb88"
clientSecret="6ca65813991c48be9ea53fbd3ae0bd5b"
scope = 'playlist-read-privateplaylist-modify-public playlist-modify-private playlist-read-collaborative user-read-private user-read-birthdate user-read-email     user-read-playback-state user-read-currently-playing user-modify-playback-state app-remote-control streaming user-follow-modify user-follow-read user-top-read user-read-recently-played user-library-read user-library-modify'


if len(sys.argv) > 1:
     username = sys.argv[1]
else:
     print("Usage: %s username" % (sys.argv[0],))
     sys.exit()
     
auth = oauth2.SpotifyClientCredentials(
	client_id=clientId,
	client_secret=clientSecret
)

token = auth.get_access_token()


ntoptrack=5
nb_recos=10
	
def gender_features(word): 
    return {'last_letter': word[-1]}

def call_spotify(artist):
	final_top_track=[]
	if token:
		sp = spotipy.Spotify(auth=token)
		sp.trace = False

		results_search=sp.search(q=artist, type="artist", limit=10)
		artistid=results_search['artists']['items'][0]['uri']
		print("\n\n\n\n")
		print(artistid)
		related = sp.artist_related_artists(artistid)
		# on cherche les artistes associés 
		for artistrelated in related['artists']:
			artistrelated_id = artistrelated['id']
			artistrelated_uri=artistrelated['uri']
		#Pour chaque artiste lié on récupère un nombre de chanson recommandées (pas forcément de cet artiste)
		reco=sp.recommendations(market='fr', seed_artists=[artistrelated_uri], limit=nb_recos)
		for trackreco in reco['tracks'] : 
			trackreco_id="Name : " + trackreco['name'] + " | Artiste : " + trackreco['artists'][0]['name']
			print(trackreco['artists'][0]['name'])
			final_top_track.append(trackreco_id)
			
		print(final_top_track)
		ret = ""
		for track in final_top_track:
			ret += "\n" + track
			
		
	 
	else:
		 print("Can't get token for", username)
	return ret


TOKEN = 'NTEyMzgxNjIyODgwOTYwNTEz.Ds66FA.72uG98AbUTMBOF-phXYedkMigGM'

client = discord.Client()


@client.event
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return

	if message.content.startswith('!members'):
		"""msg = 'Hello {0.author.mention}'.format(message)"""
		"""await client.send_message(message.channel, msg)"""
		msg = await list_members()
		await client.send_message(message.channel, msg)
	elif message.content.startswith('!jukebox'):
		#words = word_tokenize(message.content)
		#ps = PorterStemmer()
		msg = call_spotify(message.content[9:])
		await client.send_message(message.channel, msg)
		
	elif message.content.startswith('!call'):
		author = message.author
		vc = await joinvoice(author)
		print('jarrive')
	elif message.content.startswith('!leave'):
		author = message.author
		await leavevoice(message.server)


@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client	.user.id)
	print('------')
    
    
@client.event
async def list_members():
	print('Liste des membres')
	msg = 'liste des membres \n'
	for server in bot.servers:
		for member in server.members:
			msg += "" + member.name + "\n"
			
	print('------')
	return msg
	
@client.event
async def joinvoice(author):
	#"""Joins your voice channel"""
	voice_channel = author.voice_channel
	return await client.join_voice_channel(voice_channel)

@client.event
async def leavevoice(server):
	print(server)
	voice_client = client.voice_client_in(server)
	print(voice_client)
	if voice_client:
		await voice_client.disconnect()
		print("Bot left the voice channel")
	else:
		print("Bot was not in channel")

client.run(TOKEN)
