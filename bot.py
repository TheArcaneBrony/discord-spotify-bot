import requests
import discord
import json
from discord.ext.commands import Bot

#define a bot with the desired command_prefix
my_bot = Bot(command_prefix=">")

def get_artist_info(*args):
    """Retrieves the artist URL"""
    #input the arguements in a GET url
    artist_search = ("https://api.spotify.com/v1/search?q={}"
    "&type=artist&offset=0&limit=1".format(args))
    try:
        #assign a variable to the GET request response
        artist_response = requests.get(artist_search)
        #format json for artist_response
        response_json = artist_response.json()
        print("Found artist info.")
        return response_json
    except IndexError:
        print("Something went wrong")

def get_album_info(arg):
        response_json = (arg)
        #store artist id
        artistID = response_json['artists']['items'][0]['id']
        artist_album_search = "https://api.spotify.com/v1/artists/{}/albums".format(artistID)
        #format JSON response
        artist_album_response = requests.get(artist_album_search)
        artist_album_response_json =  artist_album_response.json()

        albums = artist_album_response_json['items']
        return albums

def get_related_artist_info(arg):
        response_json = (arg)
        artistID = response_json['artists']['items'][0]['id']
        related_artist_search = "https://api.spotify.com/v1/artists/{}/related-artists".format(artistID)
        related_artists_response = requests.get(related_artist_search)
        related_artists_response_json = related_artists_response.json()
        artists = related_artists_response_json['artists']
        return artists

def get_track_info(arg):
        response_json = arg
        artistID = response_json['artists']['items'][0]['id']
        #intialise the get request URL
        artist_tracks_search = "https://api.spotify.com/v1/artists/{}/top-tracks?country=US".format(artistID)
        print(artist_tracks_search)
        artist_tracks_response = requests.get(artist_tracks_search)
        #format response in JSON
        artist_tracks_response_json = artist_tracks_response.json()
        tracks = artist_tracks_response_json['tracks']
        return tracks

@my_bot.command(aliases=['a'])
async def artist(*args):
    """Retrieve artist URL"""
    response_json = get_artist_info(*args)
    artist_result_url = response_json['artists']['items'][0]['external_urls']['spotify']
    return await my_bot.say(artist_result_url)

@my_bot.command(aliases=['al'])
async def albums(arg, *args):
    """Use command >al <number> <artist> to retrieve album URL"""
    limit = 0
    if arg.isdigit() and int(arg)!= 0:
        print("arg is an int")
        response_json = get_artist_info(*args)
        albums = get_album_info(response_json)
        for album in albums:
            limit += 1
            await my_bot.say(album['external_urls']['spotify'])
            if limit == int(arg):
                break
    else:
        print("arg is an int")
        response_json = get_artist_info(*args)
        albums = get_album_info(response_json)
        for album in albums:
            limit += 1
            await my_bot.say(album['external_urls']['spotify'])
            if limit == 3:
                break

@my_bot.command(aliases=['ra'])
async def related_artist(arg, *args):
    """Retrieve related artist URL"""
    limit = 0
    if arg.isdigit() and int(arg)!= 0:
        print("Arg is an int")
        response_json = get_artist_info(*args)
        artists = get_related_artist_info(response_json)
        for artist in artists:
            limit += 1
            await my_bot.say(artist['external_urls']['spotify'])
            if limit == int(arg):
                break
    else:
        response_json = get_artist_info(*args)
        artists = get_related_artist_info(response_json)
        for artist in artists:
            limit += 1
            await my_bot.say(artist['external_urls']['spotify'])
            if limit == 3:
                break
    return 

@my_bot.command(aliases=['tr'],description='Return tracks')
async def tracks(arg, *args):
    """Retrieve artist tracks"""
    print(arg)
    limit = 0
    if arg.isdigit() and int(arg)!= 0:
        response_json = get_artist_info(*args)
        tracks = get_track_info(response_json)
        for track in tracks:
            await my_bot.say(track['external_urls']['spotify'])
            limit += 1
            if limit == int(arg):
                break
    else:
        print("Arg is not an int")
        response_json = get_artist_info(arg, *args)
        tracks = get_track_info(response_json)
        for track in tracks:
            limit += 1
            await my_bot.say(track['external_urls']['spotify'])
            if limit == 3:
                break

@my_bot.command()
async def user(*args):
    username = discord.User(*args)
    return await my_bot.say(username)

@my_bot.command()
async def info():
    return await my_bot.say("Hi! Allow me to introduce  myself. \nThis is "+ my_bot.user.name + "!")

@my_bot.command()
async def playlist(*args):
    response_json = get_artist_info(*args)
    track_ids = []
    tracks = get_track_info(response_json)
    for track in tracks:
        await my_bot.say(track["id"])
        track_ids.append(track['id'])
    print(len(track_ids))
    # for artist in all_related_artists_info:
        # print artist[]

my_bot.run("<insert token here>")

