
import base64
import requests 
import datetime
from urllib.parse import urlencode
import json
import os
from flask import Flask, redirect, session, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
import pandas as pd


client_id = "85993565020a4cdca06d4681fe494fb7"
client_secret = "5f9d8c9792994c2a87dffb0eb5a69279"

class SpotifyAPI(object):
  access_token = None
  access_token_expires = datetime.datetime.now()
  access_token_did_expire = True
  client_id = None
  client_secret = None
  token_url = "https://accounts.spotify.com/api/token"

  def __init__(self, client_id, client_secret, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.client_id = client_id
    self.client_secret = client_secret

  def client_credentials(self):
      
      #Returns a base64 encoded string
      
      client_id = self.client_id
      client_secret = self.client_secret
      if client_secret == None or client_id == None:
          raise Exception("You must set client_id and client_secret")
      client_creds = f"{client_id}:{client_secret}"
      client_creds_b64 = base64.b64encode(client_creds.encode())
      return client_creds_b64.decode()

  def token_headers(self):
      client_creds_b64 = self.client_credentials()
      return {
        "Authorization": f"Basic {client_creds_b64}" 
      }

  def token_data(self):
      return {
        "grant_type": "client_credentials"
      }

  def perform_auth(self):
      token_url = self.token_url
      token_data = self.token_data()
      token_headers = self.token_headers()
      r = requests.post(token_url, data=token_data, headers=token_headers)
      if r.status_code not in range(200, 299): 
          raise Exception("Could not authenticate client")
          #return False
      data = r.json()
      now = datetime.datetime.now()
      access_token = data['access_token']
      expires_in = data['expires_in'] # seconds
      expires = now + datetime.timedelta(seconds=expires_in)
      self.access_token = access_token
      self.access_token_expires = expires 
      self.access_token_did_expire = expires < now
      return True
    
  def get_access_token(self):
      token = self.access_token
      expires = self.access_token_expires
      now = datetime.datetime.now()
      if expires < now:
          self.perform_auth()
          return self.get_access_token()
      elif token == None:
          self.perform_auth()
          return self.get_access_token()
      return token

  def resource_header(self):
      access_token = self.get_access_token()
      headers = {
          "Authorization": f"Bearer {access_token}"
      }      
      return headers

  def base_search(self, query_params):
      headers = self.resource_header()
      endpoint = "https://api.spotify.com/v1/search"
      lookup_url = f"{endpoint}?{query_params}"
      print(lookup_url)
      r = requests.get(lookup_url, headers=headers)
      if r.status_code not in range(200, 299):
          return {}  
      return r.json()

  def search(self, query=None, operator=None, operator_query=None, search_type='artist'):
      if query == None:
          raise Exception("A query is required")
      if isinstance(query, dict):
          query = " ".join([f"{k}:{v}" for k,v in query.items()])
      if operator != None and operator_query != None:
          if operator.lower() == "or" or operator == "not":
              operator = operator.upper()
              if isinstance(operator_query, str):
                  query = f"{query} {operator} {operator_query}"
      query_params = urlencode({"q": query,"type": search_type.lower()})
      print(query_params)
      return self.base_search(query_params)


client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode())
client_creds_b64

token_url = "https://accounts.spotify.com/api/token"
method = "POST"

token_data = {
    "grant_type":"client_credentials"
}

token_headers = {
    "Authorization": f"Basic {client_creds_b64.decode()}"
}

token_headers

req = requests.post(token_url,data=token_data, headers=token_headers)
token_response_data = req.json()
req.status_code

token_response_data = req.json()
access_token = token_response_data['access_token']
expire_in = token_response_data['expires_in'] #seconds
token_type = token_response_data['token_type']
token_response_data


def token_headers(self):
    client_creds_b64 = self.client_credentials()
    return {
        "Authorization": f"Basic {client_creds_b64}"
    }

def authenticate(self):
    token_url = self.token_url
    token_data = self.token_data()
    token_headers =self.token_headers()
    req = requests.post(token_url,data=token_data, headers=token_headers)
    print(req.json)

    token_response_data = req.json()
    access_token = token_response_data['access_token']
    expires_in = token_response_data['expire_in']

    self.access_token = access_token
    return token_response_data

spotify_client = SpotifyAPI(client_id,client_secret)

print(spotify_client.__init__(client_id,client_secret))
print(spotify_client.client_credentials())
print(spotify_client.token_data())
print(spotify_client.token_headers())
print(spotify_client.perform_auth())


base_url = 'https://api.spotify.com/v1/'
user_id = 'xa5jpotdh03zb469lofbv9u0m'  # User ID of Groover Obsessions Spotify user

# Endpoint to get a user's playlists
user_playlists_endpoint = f'users/{user_id}/playlists'

# URL to fetch the user's playlists
user_playlists_url = f'{base_url}{user_playlists_endpoint}'

# Include the access token in the request headers
headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

# Send the API request to get the user's playlists
response = requests.get(user_playlists_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Extract the playlists from the response JSON
    playlists = response.json()['items']
    
    # Sort the playlists by the number of followers in descending order
    playlists.sort(key=lambda x: x['tracks']['total'], reverse=True)
    
    # Extract the top three playlists by followers
    top_three_playlists = playlists[:3]
    
    # Print the top three playlists
    for playlist in top_three_playlists:
        print(playlist['name'], playlist['tracks']['total'])

else:
    print("Error:", response.status_code)

# IDs of the top 3 playlists obtained
#'id': '0sroJWVhI6U6hgEzKto0DD', 'name': 'Groover Obsessions - All recent releases ✨' 1681
# 'id': '6bGugXBtyrq6iwebS7RCL5' , Groover Radio • Playlist 1332
#'id': '4EAqp1RxBerLLlMu9Tj1xd' , Groover Obsessions - Discover 969

# Define a function to retrieve artist popularity metrics
def get_artist_popularity(artist_id):
    # Endpoint to get artist information
    artist_endpoint = f'artists/{artist_id}'
    artist_url = f'{base_url}{artist_endpoint}'
    
    # Send the API request
    response = requests.get(artist_url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract popularity metrics from the response JSON
        artist_data = response.json()
        popularity = artist_data.get('popularity')
        return popularity
    else:
        return None

# Iterate over the top three playlists
for playlist in top_three_playlists:
    playlist_name = playlist['name']
    print(f"Playlist: {playlist_name}")
    
    # Get the playlist ID
    playlist_id = playlist['id']
    
    # Endpoint to get playlist tracks
    playlist_tracks_endpoint = f'playlists/{playlist_id}/tracks'
    playlist_tracks_url = f'{base_url}{playlist_tracks_endpoint}'
    
    # Send the API request to get playlist tracks
    response = requests.get(playlist_tracks_url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract the list of tracks from the response JSON
        tracks = response.json()['items']
        
        # Extract artist IDs from each track and store them in a set to remove duplicates
        artist_ids = set()
        for track in tracks:
            artist_data = track['track']['artists']
            for artist in artist_data:
                artist_ids.add(artist['id'])
        
        # Iterate over the unique artist IDs
        for artist_id in artist_ids:
            # Retrieve the artist popularity metric
            popularity = get_artist_popularity(artist_id)
            
            # Print the artist ID and popularity metric
            if popularity is not None:
                print(f"Artist_ID: {artist_id}, Popularity: {popularity}")
            else:
                print(f"Failed to retrieve popularity for artist ID: {artist_id}")
    else:
        print(f"Error fetching tracks for playlist {playlist_name}: {response.status_code}")



################
################
playlist_data = [
    {
        "playlist_name": "Groover Obsessions - All recent releases ✨",
        "artists": [
            {"Artist_ID": "2xr7qMt5JEYYyxSL3WnhoH", "Popularity": 13},
            {"Artist_ID": "4i8YmrvKe2CSIUT08ewdpF", "Popularity": 17},
            {"Artist_ID": "7x4SkMPeQe5oXLlUxkbjVG", "Popularity": 7},
            {"Artist_ID": "32SXond7qEk5OOXU9M8Sq7", "Popularity": 26},
            {"Artist_ID": "0JzGwXJbpoPu17Q9YSCXgN", "Popularity": 13},
            {"Artist_ID": "1cxvTBZk2FxR8hgtF25sK2", "Popularity": 22},
            {"Artist_ID": "3p5keqAzDnuOoAVya8laK6", "Popularity": 18},
            {"Artist_ID": "3LdkXiDerzaw7NOzShvP7b", "Popularity": 7},
            {"Artist_ID": "0g7ytn3IEIrPXnXSQm08av", "Popularity": 8},
            {"Artist_ID": "4q96Knz1ZNcPNmfccBDUjw", "Popularity": 4},
            {"Artist_ID": "4sOLJi96MhdlMv5Iz9YZT9", "Popularity": 43},
            {"Artist_ID": "0G1NAb9YOyaKF2i6eYKpaD", "Popularity": 14},
            {"Artist_ID": "3IvaAkEg7LEtQHppHQvl4B", "Popularity": 16},
            {"Artist_ID": "1TdXwGMZuFrMWwqGqDSIZq", "Popularity": 21},
            {"Artist_ID": "1BXs8rkknL8fgvRsErY9pY", "Popularity": 9},
            {"Artist_ID": "7wDjdS9h3CXK18Y1H1hO5I", "Popularity": 34},
            {"Artist_ID": "0l38euGQtLByxRRKXtN0RP", "Popularity": 10},
            {"Artist_ID": "0Dtc3SOdrw9iDth59UPO60", "Popularity": 24},
            {"Artist_ID": "1k9huPx7MuSDw1pkZvHqIj", "Popularity": 12},
            {"Artist_ID": "4KPdER6eNWruPkJ8ps4f6c", "Popularity": 16},
            {"Artist_ID": "1OVMF4LXI8xkr4lHiDL8W4", "Popularity": 10},
            {"Artist_ID": "55BTCefOxzfRNX7CbxCkhm", "Popularity": 5},
            {"Artist_ID": "0nRWv1xU9ooWFExNxKTKef", "Popularity": 40},
            {"Artist_ID": "70fFvvSC8a3zZU0t9uVeEm", "Popularity": 7},
            {"Artist_ID": "1znEU6ZKZcYBGxyRLMQhVc", "Popularity": 4},
            {"Artist_ID": "4P87NMJZeQOJjVy3W5mnAy", "Popularity": 0},
            {"Artist_ID": "6yfcoVGojS0XOgw8dVAb0R", "Popularity": 25},
            {"Artist_ID": "3HxWmWHxjwwnpP8Clqz31t", "Popularity": 26},
            {"Artist_ID": "7se9xztf5FhPyzKpnqzuxZ", "Popularity": 2},
            {"Artist_ID": "4zpQwRAlCIdPEA6DYiPxQ4", "Popularity": 24},
            {"Artist_ID": "6IjSW1JQwRHB9cPFyu2tn5", "Popularity": 30},
            {"Artist_ID": "6krsiTtc4T9aJEkwT3lyP5", "Popularity": 20},
            {"Artist_ID": "010wxklenCFtHumkvnpUXg", "Popularity": 8},
            {"Artist_ID": "70CoeVOqQha3tFdbrpUYEy", "Popularity": 4},
            {"Artist_ID": "0OhPRNmylTtIPYgk4Zxh0e", "Popularity": 24},
            {"Artist_ID": "3axjOJUhll8B2Cpd22sLpa", "Popularity": 33},
            {"Artist_ID": "2hRBCthhgnmfAAp3omscIE", "Popularity": 8},
            {"Artist_ID": "5S9RapV1xdVZ4zB3hkf2WM", "Popularity": 15},
            {"Artist_ID": "0et7l4k6xGlM34MIWStLE4", "Popularity": 9},
            {"Artist_ID": "3VNZGO4ExFAzJYf4ovJOqq", "Popularity": 16},
            {"Artist_ID": "4veGqOoNH9WGhFS0kUiVxG", "Popularity": 6},
            {"Artist_ID": "1cTINVmi2me8JBpCwR2K16", "Popularity": 18},
            {"Artist_ID": "5KOerBNbTPn8iarMOLJStg", "Popularity": 0},
            {"Artist_ID": "7CLlZl0i0kCbkMSLmzYqS6", "Popularity": 16},
            {"Artist_ID": "3yJSOftpPmcSSpZLQQQ5Fl", "Popularity": 10},
            {"Artist_ID": "5eATUoLTafitqpoDRpRbwR", "Popularity": 16},
            {"Artist_ID": "0yVnVpHr5djmPUqPtg3efc", "Popularity": 21},
            {"Artist_ID": "4v8etUh3qt9jHliW6kg697", "Popularity": 7},
            {"Artist_ID": "1KdcI8A2GWwz1NX7V7dYi6", "Popularity": 12},
            {"Artist_ID": "0ynYpASVUDUPjJr1S246ag", "Popularity": 6},
            {"Artist_ID": "4YYpLfkip4IqhW0t4xa4LY", "Popularity": 14},
            {"Artist_ID": "47dBw2gSUHXmI7ss3DpqVU", "Popularity": 10},
            {"Artist_ID": "4rQlulN63iChFAhcoYfvFv", "Popularity": 16},
            {"Artist_ID": "7LkPJJITZP0cl5WTJrh1uX", "Popularity": 2},
            {"Artist_ID": "6qpFuV7BdV4Fk0N5UW5BRO", "Popularity": 1},
            {"Artist_ID": "7JF6azwNk0WAYCsPSEOT0N", "Popularity": 19},
            {"Artist_ID": "2uabCS4A3GEtyIi3WPzIMn", "Popularity": 7},
            {"Artist_ID": "2sFPQins7c1Mx7COcPdBUV", "Popularity": 35},
            {"Artist_ID": "1MoD5leV9TnswO1PRlaUkM", "Popularity": 13},
            {"Artist_ID": "1JdFzT3HVVdNNvpdIyfOPS", "Popularity": 10},
            {"Artist_ID": "6wFVOWAlaKr2IrJI4csaZS", "Popularity": 5},
            {"Artist_ID": "7d1JBEtg04rXtzEa2f6s4t", "Popularity": 13},
            {"Artist_ID": "3gbwYBV6Cyp7BbhXU44gQe", "Popularity": 8},
            {"Artist_ID": "6Te81qcP1wIVOh1v6mJAFb", "Popularity": 14},
            {"Artist_ID": "17smx8eXQnsNDCWgy6hNHC", "Popularity": 10},
            {"Artist_ID": "7fYneKDOF1b32rZSRdn6Zd", "Popularity": 11},
            {"Artist_ID": "7MZuK7vnEfwviocPQOTCfu", "Popularity": 13},
            {"Artist_ID": "13PQC9YAcZKTggJOoHLF7O", "Popularity": 5},
            {"Artist_ID": "2O7fbpcASuwdL6nGvWsAFQ", "Popularity": 6},
            {"Artist_ID": "7MkdDRirzB2d9UZh6ZMb8p", "Popularity": 15},
            {"Artist_ID": "2bcuuLj3Gp7wAbU529W4aB", "Popularity": 12},
            {"Artist_ID": "7mrcoS7PSLRXyq7ctzvXFb", "Popularity": 5},
            {"Artist_ID": "20ZHmYNQXa3NoerXEAADpl", "Popularity": 14},
            {"Artist_ID": "5BhAXhQRxK6rZH6EPKCrph", "Popularity": 5},
            {"Artist_ID": "5OFLwoxk5jmOkgjxbgAWOO", "Popularity": 25},
            {"Artist_ID": "6jPobIjQSlByVyUcbKkrSe", "Popularity": 4},
            {"Artist_ID": "3haF6AWaxsmmcHPyqZmN9g", "Popularity": 15},
            {"Artist_ID": "40NHF5NVrMIvMJAX3vGyy1", "Popularity": 16},
            {"Artist_ID": "7HTAT1UO48NHZYhFJrRBDm", "Popularity": 13},
            {"Artist_ID": "6reIXWDPghdbaioV4bUuOn", "Popularity": 7},
            {"Artist_ID": "57U2GAhyD67rqAPQaT2wnb", "Popularity": 5},
            {"Artist_ID": "6EWfSiI0vfs5OzyNrKAHIJ", "Popularity": 22},
            {"Artist_ID": "44LRBwzsc5F1ZIWcCStTOh", "Popularity": 5},
            {"Artist_ID": "2cL3xi8TbN7DrsHmUSNAJ9", "Popularity": 2},
            {"Artist_ID": "24XJwyJK0xNSpsXmKcNxpA", "Popularity": 5},
            {"Artist_ID": "38SeOdMQ30omkzUolT5d4m", "Popularity": 30},
            {"Artist_ID": "6BStglzFvs6FDKMzHbZzV0", "Popularity": 17},
            {"Artist_ID": "7lOC6WJxv8tB3tJWLCw0HK", "Popularity": 6},
            {"Artist_ID": "0HSZWleTsKOcWUQuDXizYk", "Popularity": 7},
            {"Artist_ID": "72yg6tWrGwoPqpiUD25BK7", "Popularity": 19},
            {"Artist_ID": "6IUKOT5oMnQ8ZUyJlZFxO2", "Popularity": 32},
            {"Artist_ID": "16NfZBJxDfPQXRUNI9sG8k", "Popularity": 9}
            
        ]
    },
    {
        "playlist_name": "Groover Radio • Playlist ⚡️",
        "artists": [
            {"Artist_ID": "2xr7qMt5JEYYyxSL3WnhoH", "Popularity": 13},
            {"Artist_ID": "4i8YmrvKe2CSIUT08ewdpF", "Popularity": 17},
            {"Artist_ID": "6wjhAQSDQAl0QNsE0rJKIi", "Popularity": 11},
            {"Artist_ID": "7x4SkMPeQe5oXLlUxkbjVG", "Popularity": 7},
            {"Artist_ID": "32SXond7qEk5OOXU9M8Sq7", "Popularity": 26},
            {"Artist_ID": "0JzGwXJbpoPu17Q9YSCXgN", "Popularity": 13},
            {"Artist_ID": "3p5keqAzDnuOoAVya8laK6", "Popularity": 18},
            {"Artist_ID": "3LdkXiDerzaw7NOzShvP7b", "Popularity": 7},
            {"Artist_ID": "5WTR6ZwfribWN2jL9YwbXN", "Popularity": 9},
            {"Artist_ID": "0g7ytn3IEIrPXnXSQm08av", "Popularity": 8},
            {"Artist_ID": "4q96Knz1ZNcPNmfccBDUjw", "Popularity": 4},
            {"Artist_ID": "4sOLJi96MhdlMv5Iz9YZT9", "Popularity": 43},
            {"Artist_ID": "0G1NAb9YOyaKF2i6eYKpaD", "Popularity": 14},
            {"Artist_ID": "3IvaAkEg7LEtQHppHQvl4B", "Popularity": 16},
            {"Artist_ID": "1TdXwGMZuFrMWwqGqDSIZq", "Popularity": 21},
            {"Artist_ID": "1BXs8rkknL8fgvRsErY9pY", "Popularity": 9},
            {"Artist_ID": "7wDjdS9h3CXK18Y1H1hO5I", "Popularity": 34},
            {"Artist_ID": "0l38euGQtLByxRRKXtN0RP", "Popularity": 10},
            {"Artist_ID": "0Dtc3SOdrw9iDth59UPO60", "Popularity": 24},
            {"Artist_ID": "1k9huPx7MuSDw1pkZvHqIj", "Popularity": 12},
            {"Artist_ID": "7p2G64vSMKhAvNQZ2auGMQ", "Popularity": 3},
            {"Artist_ID": "4KPdER6eNWruPkJ8ps4f6c", "Popularity": 16},
            {"Artist_ID": "1OVMF4LXI8xkr4lHiDL8W4", "Popularity": 10},
            {"Artist_ID": "55BTCefOxzfRNX7CbxCkhm", "Popularity": 5},
            {"Artist_ID": "0nRWv1xU9ooWFExNxKTKef", "Popularity": 40},
            {"Artist_ID": "70fFvvSC8a3zZU0t9uVeEm", "Popularity": 7},
            {"Artist_ID": "1znEU6ZKZcYBGxyRLMQhVc", "Popularity": 4},
            {"Artist_ID": "4P87NMJZeQOJjVy3W5mnAy", "Popularity": 0},
            {"Artist_ID": "6yfcoVGojS0XOgw8dVAb0R", "Popularity": 25},
            {"Artist_ID": "3XMIARRaGCAqYbKX1RhQkv", "Popularity": 8},
            {"Artist_ID": "3HxWmWHxjwwnpP8Clqz31t", "Popularity": 26},
            {"Artist_ID": "7se9xztf5FhPyzKpnqzuxZ", "Popularity": 2},
            {"Artist_ID": "5lAZTyHLWuqddQudiftzIE", "Popularity": 8},
            {"Artist_ID": "4zpQwRAlCIdPEA6DYiPxQ4", "Popularity": 24},
            {"Artist_ID": "6IjSW1JQwRHB9cPFyu2tn5", "Popularity": 30},
            {"Artist_ID": "6krsiTtc4T9aJEkwT3lyP5", "Popularity": 20},
            {"Artist_ID": "010wxklenCFtHumkvnpUXg", "Popularity": 8},
            {"Artist_ID": "70CoeVOqQha3tFdbrpUYEy", "Popularity": 4},
            {"Artist_ID": "0OhPRNmylTtIPYgk4Zxh0e", "Popularity": 24},
            {"Artist_ID": "3axjOJUhll8B2Cpd22sLpa", "Popularity": 33},
            {"Artist_ID": "5ous6yeH8iN6RIL3NPTyEw", "Popularity": 2},
            {"Artist_ID": "2hRBCthhgnmfAAp3omscIE", "Popularity": 8},
            {"Artist_ID": "5S9RapV1xdVZ4zB3hkf2WM", "Popularity": 15},
            {"Artist_ID": "0et7l4k6xGlM34MIWStLE4", "Popularity": 9},
            {"Artist_ID": "3VNZGO4ExFAzJYf4ovJOqq", "Popularity": 16},
            {"Artist_ID": "0EzrGrgoaRfFelIQgRBIt7", "Popularity": 42},
            {"Artist_ID": "4veGqOoNH9WGhFS0kUiVxG", "Popularity": 6},
            {"Artist_ID": "1cTINVmi2me8JBpCwR2K16", "Popularity": 18},
            {"Artist_ID": "5KOerBNbTPn8iarMOLJStg", "Popularity": 0},
            {"Artist_ID": "7CLlZl0i0kCbkMSLmzYqS6", "Popularity": 16},
            {"Artist_ID": "3yJSOftpPmcSSpZLQQQ5Fl", "Popularity": 10},
            {"Artist_ID": "5eATUoLTafitqpoDRpRbwR", "Popularity": 16},
            {"Artist_ID": "0yVnVpHr5djmPUqPtg3efc", "Popularity": 21},
            {"Artist_ID": "4v8etUh3qt9jHliW6kg697", "Popularity": 7},
            {"Artist_ID": "1KdcI8A2GWwz1NX7V7dYi6", "Popularity": 12},
            {"Artist_ID": "0ynYpASVUDUPjJr1S246ag", "Popularity": 6},
            {"Artist_ID": "4YYpLfkip4IqhW0t4xa4LY", "Popularity": 14},
            {"Artist_ID": "47dBw2gSUHXmI7ss3DpqVU", "Popularity": 10},
            {"Artist_ID": "4rQlulN63iChFAhcoYfvFv", "Popularity": 16},
            {"Artist_ID": "7LkPJJITZP0cl5WTJrh1uX", "Popularity": 2},
            {"Artist_ID": "6qpFuV7BdV4Fk0N5UW5BRO", "Popularity": 1},
            {"Artist_ID": "7JF6azwNk0WAYCsPSEOT0N", "Popularity": 19},
            {"Artist_ID": "2uabCS4A3GEtyIi3WPzIMn", "Popularity": 7},
            {"Artist_ID": "2sFPQins7c1Mx7COcPdBUV", "Popularity": 35},
            {"Artist_ID": "1MoD5leV9TnswO1PRlaUkM", "Popularity": 13},
            {"Artist_ID": "1JdFzT3HVVdNNvpdIyfOPS", "Popularity": 10},
            {"Artist_ID": "6wFVOWAlaKr2IrJI4csaZS", "Popularity": 5},
            {"Artist_ID": "7d1JBEtg04rXtzEa2f6s4t", "Popularity": 13},
            {"Artist_ID": "3gbwYBV6Cyp7BbhXU44gQe", "Popularity": 8},
            {"Artist_ID": "3ptIQpLhRHZmWTSk5vjIco", "Popularity": 4},
            {"Artist_ID": "6Te81qcP1wIVOh1v6mJAFb", "Popularity": 14},
            {"Artist_ID": "17smx8eXQnsNDCWgy6hNHC", "Popularity": 10},
            {"Artist_ID": "7fYneKDOF1b32rZSRdn6Zd", "Popularity": 11},
            {"Artist_ID": "7MZuK7vnEfwviocPQOTCfu", "Popularity": 13},
            {"Artist_ID": "13PQC9YAcZKTggJOoHLF7O", "Popularity": 5},
            {"Artist_ID": "2O7fbpcASuwdL6nGvWsAFQ", "Popularity": 6},
            {"Artist_ID": "7MkdDRirzB2d9UZh6ZMb8p", "Popularity": 15},
            {"Artist_ID": "2bcuuLj3Gp7wAbU529W4aB", "Popularity": 12},
            {"Artist_ID": "7mrcoS7PSLRXyq7ctzvXFb", "Popularity": 5},
            {"Artist_ID": "20ZHmYNQXa3NoerXEAADpl", "Popularity": 14},
            {"Artist_ID": "5BhAXhQRxK6rZH6EPKCrph", "Popularity": 5},
            {"Artist_ID": "5OFLwoxk5jmOkgjxbgAWOO", "Popularity": 25},
            {"Artist_ID": "6jPobIjQSlByVyUcbKkrSe", "Popularity": 4},
            {"Artist_ID": "3haF6AWaxsmmcHPyqZmN9g", "Popularity": 15},
            {"Artist_ID": "40NHF5NVrMIvMJAX3vGyy1", "Popularity": 16},
            {"Artist_ID": "7HTAT1UO48NHZYhFJrRBDm", "Popularity": 13},
            {"Artist_ID": "6reIXWDPghdbaioV4bUuOn", "Popularity": 7},
            {"Artist_ID": "57U2GAhyD67rqAPQaT2wnb", "Popularity": 5},
            {"Artist_ID": "6EWfSiI0vfs5OzyNrKAHIJ", "Popularity": 22},
            {"Artist_ID": "44LRBwzsc5F1ZIWcCStTOh", "Popularity": 5},
            {"Artist_ID": "56JkEilM5CosUvJEHSuLjb", "Popularity": 10},
            {"Artist_ID": "24XJwyJK0xNSpsXmKcNxpA", "Popularity": 5},
            {"Artist_ID": "38SeOdMQ30omkzUolT5d4m", "Popularity": 30},
            {"Artist_ID": "4eOtKEhBAs3AEoz2rtlbDA", "Popularity": 5},
            {"Artist_ID": "6BStglzFvs6FDKMzHbZzV0", "Popularity": 17},
            {"Artist_ID": "7lOC6WJxv8tB3tJWLCw0HK", "Popularity": 6},
            {"Artist_ID": "0HSZWleTsKOcWUQuDXizYk", "Popularity": 7},
            {"Artist_ID": "72yg6tWrGwoPqpiUD25BK7", "Popularity": 19},
            {"Artist_ID": "6IUKOT5oMnQ8ZUyJlZFxO2", "Popularity": 32},
            {"Artist_ID": "16NfZBJxDfPQXRUNI9sG8k", "Popularity": 9}
        ]
    },
    {
        "playlist_name": "Groover Obsessions - Discover",
        "artists": [
            {"Artist_ID": "3haF6AWaxsmmcHPyqZmN9g", "Popularity": 15},
            {"Artist_ID": "1cTINVmi2me8JBpCwR2K16", "Popularity": 18},
            {"Artist_ID": "2xr7qMt5JEYYyxSL3WnhoH", "Popularity": 13},
            {"Artist_ID": "4i8YmrvKe2CSIUT08ewdpF", "Popularity": 17},
            {"Artist_ID": "6wjhAQSDQAl0QNsE0rJKIi", "Popularity": 11},
            {"Artist_ID": "7x4SkMPeQe5oXLlUxkbjVG", "Popularity": 7},
            {"Artist_ID": "32SXond7qEk5OOXU9M8Sq7", "Popularity": 26},
            {"Artist_ID": "0JzGwXJbpoPu17Q9YSCXgN", "Popularity": 13},
            {"Artist_ID": "3p5keqAzDnuOoAVya8laK6", "Popularity": 18},
            {"Artist_ID": "3LdkXiDerzaw7NOzShvP7b", "Popularity": 7},
            {"Artist_ID": "5WTR6ZwfribWN2jL9YwbXN", "Popularity": 9},
            {"Artist_ID": "6oqDqZlET7T3JO9YWD2pVW", "Popularity": 39},
            {"Artist_ID": "0g7ytn3IEIrPXnXSQm08av", "Popularity": 8},
            {"Artist_ID": "4sOLJi96MhdlMv5Iz9YZT9", "Popularity": 43},
            {"Artist_ID": "4q96Knz1ZNcPNmfccBDUjw", "Popularity": 4},
            {"Artist_ID": "0G1NAb9YOyaKF2i6eYKpaD", "Popularity": 14},
            {"Artist_ID": "3IvaAkEg7LEtQHppHQvl4B", "Popularity": 16},
            {"Artist_ID": "1TdXwGMZuFrMWwqGqDSIZq", "Popularity": 21},
            {"Artist_ID": "7wDjdS9h3CXK18Y1H1hO5I", "Popularity": 34},
            {"Artist_ID": "1BXs8rkknL8fgvRsErY9pY", "Popularity": 9},
            {"Artist_ID": "0l38euGQtLByxRRKXtN0RP", "Popularity": 10},
            {"Artist_ID": "0Dtc3SOdrw9iDth59UPO60", "Popularity": 24},
            {"Artist_ID": "1k9huPx7MuSDw1pkZvHqIj", "Popularity": 12},
            {"Artist_ID": "7p2G64vSMKhAvNQZ2auGMQ", "Popularity": 3},
            {"Artist_ID": "4KPdER6eNWruPkJ8ps4f6c", "Popularity": 16},
            {"Artist_ID": "1OVMF4LXI8xkr4lHiDL8W4", "Popularity": 10},
            {"Artist_ID": "55BTCefOxzfRNX7CbxCkhm", "Popularity": 5},
            {"Artist_ID": "0nRWv1xU9ooWFExNxKTKef", "Popularity": 40},
            {"Artist_ID": "70fFvvSC8a3zZU0t9uVeEm", "Popularity": 7},
            {"Artist_ID": "1znEU6ZKZcYBGxyRLMQhVc", "Popularity": 4},
            {"Artist_ID": "4P87NMJZeQOJjVy3W5mnAy", "Popularity": 0},
            {"Artist_ID": "6yfcoVGojS0XOgw8dVAb0R", "Popularity": 25},
            {"Artist_ID": "3XMIARRaGCAqYbKX1RhQkv", "Popularity": 8},
            {"Artist_ID": "3HxWmWHxjwwnpP8Clqz31t", "Popularity": 26},
            {"Artist_ID": "7se9xztf5FhPyzKpnqzuxZ", "Popularity": 2},
            {"Artist_ID": "5lAZTyHLWuqddQudiftzIE", "Popularity": 8},
            {"Artist_ID": "4zpQwRAlCIdPEA6DYiPxQ4", "Popularity": 24},
            {"Artist_ID": "6IjSW1JQwRHB9cPFyu2tn5", "Popularity": 30},
            {"Artist_ID": "6krsiTtc4T9aJEkwT3lyP5", "Popularity": 20},
            {"Artist_ID": "010wxklenCFtHumkvnpUXg", "Popularity": 8},
            {"Artist_ID": "70CoeVOqQha3tFdbrpUYEy", "Popularity": 4},
            {"Artist_ID": "0OhPRNmylTtIPYgk4Zxh0e", "Popularity": 24},
            {"Artist_ID": "3axjOJUhll8B2Cpd22sLpa", "Popularity": 33},
            {"Artist_ID": "5ous6yeH8iN6RIL3NPTyEw", "Popularity": 2},
            {"Artist_ID": "2hRBCthhgnmfAAp3omscIE", "Popularity": 8},
            {"Artist_ID": "5S9RapV1xdVZ4zB3hkf2WM", "Popularity": 15},
            {"Artist_ID": "0et7l4k6xGlM34MIWStLE4", "Popularity": 9},
            {"Artist_ID": "3VNZGO4ExFAzJYf4ovJOqq", "Popularity": 16},
            {"Artist_ID": "0EzrGrgoaRfFelIQgRBIt7", "Popularity": 42},
            {"Artist_ID": "4veGqOoNH9WGhFS0kUiVxG", "Popularity": 6},
            {"Artist_ID": "1cTINVmi2me8JBpCwR2K16", "Popularity": 18},
            {"Artist_ID": "5KOerBNbTPn8iarMOLJStg", "Popularity": 0},
            {"Artist_ID": "7CLlZl0i0kCbkMSLmzYqS6", "Popularity": 16},
            {"Artist_ID": "3yJSOftpPmcSSpZLQQQ5Fl", "Popularity": 10},
            {"Artist_ID": "5eATUoLTafitqpoDRpRbwR", "Popularity": 16},
            {"Artist_ID": "0yVnVpHr5djmPUqPtg3efc", "Popularity": 21},
            {"Artist_ID": "4v8etUh3qt9jHliW6kg697", "Popularity": 7},
            {"Artist_ID": "1KdcI8A2GWwz1NX7V7dYi6", "Popularity": 12},
            {"Artist_ID": "0ynYpASVUDUPjJr1S246ag", "Popularity": 6},
            {"Artist_ID": "4YYpLfkip4IqhW0t4xa4LY", "Popularity": 14},
            {"Artist_ID": "47dBw2gSUHXmI7ss3DpqVU", "Popularity": 10},
            {"Artist_ID": "4rQlulN63iChFAhcoYfvFv", "Popularity": 16},
            {"Artist_ID": "7LkPJJITZP0cl5WTJrh1uX", "Popularity": 2},
            {"Artist_ID": "6qpFuV7BdV4Fk0N5UW5BRO", "Popularity": 1},
            {"Artist_ID": "7JF6azwNk0WAYCsPSEOT0N", "Popularity": 19},
            {"Artist_ID": "2uabCS4A3GEtyIi3WPzIMn", "Popularity": 7},
            {"Artist_ID": "1MoD5leV9TnswO1PRlaUkM", "Popularity": 13},
            {"Artist_ID": "1JdFzT3HVVdNNvpdIyfOPS", "Popularity": 10},
            {"Artist_ID": "6wFVOWAlaKr2IrJI4csaZS", "Popularity": 5},
            {"Artist_ID": "7d1JBEtg04rXtzEa2f6s4t", "Popularity": 13},
            {"Artist_ID": "3gbwYBV6Cyp7BbhXU44gQe", "Popularity": 8},
            {"Artist_ID": "3ptIQpLhRHZmWTSk5vjIco", "Popularity": 4},
            {"Artist_ID": "6Te81qcP1wIVOh1v6mJAFb", "Popularity": 14},
            {"Artist_ID": "1oBXXRTPzynCh1tLDOmlkI", "Popularity": 12},
            {"Artist_ID": "17smx8eXQnsNDCWgy6hNHC", "Popularity": 10},
            {"Artist_ID": "7fYneKDOF1b32rZSRdn6Zd", "Popularity": 11},
            {"Artist_ID": "7MZuK7vnEfwviocPQOTCfu", "Popularity": 13},
            {"Artist_ID": "13PQC9YAcZKTggJOoHLF7O", "Popularity": 5},
            {"Artist_ID": "2O7fbpcASuwdL6nGvWsAFQ", "Popularity": 6},
            {"Artist_ID": "7MkdDRirzB2d9UZh6ZMb8p", "Popularity": 15},
            {"Artist_ID": "2bcuuLj3Gp7wAbU529W4aB", "Popularity": 12},
            {"Artist_ID": "7mrcoS7PSLRXyq7ctzvXFb", "Popularity": 5},
            {"Artist_ID": "20ZHmYNQXa3NoerXEAADpl", "Popularity": 14},
            {"Artist_ID": "5BhAXhQRxK6rZH6EPKCrph", "Popularity": 5},
            {"Artist_ID": "5OFLwoxk5jmOkgjxbgAWOO", "Popularity": 25},
            {"Artist_ID": "6jPobIjQSlByVyUcbKkrSe", "Popularity": 4},
            {"Artist_ID": "3haF6AWaxsmmcHPyqZmN9g", "Popularity": 15},
            {"Artist_ID": "40NHF5NVrMIvMJAX3vGyy1", "Popularity": 16},
            {"Artist_ID": "7HTAT1UO48NHZYhFJrRBDm", "Popularity": 13},
            {"Artist_ID": "6reIXWDPghdbaioV4bUuOn", "Popularity": 7},
            {"Artist_ID": "57U2GAhyD67rqAPQaT2wnb", "Popularity": 5},
            {"Artist_ID": "6EWfSiI0vfs5OzyNrKAHIJ", "Popularity": 22},
            {"Artist_ID": "44LRBwzsc5F1ZIWcCStTOh", "Popularity": 5},
            {"Artist_ID": "56JkEilM5CosUvJEHSuLjb", "Popularity": 10},
            {"Artist_ID": "24XJwyJK0xNSpsXmKcNxpA", "Popularity": 5},
            {"Artist_ID": "38SeOdMQ30omkzUolT5d4m", "Popularity": 30},
            {"Artist_ID": "4eOtKEhBAs3AEoz2rtlbDA", "Popularity": 5},
            {"Artist_ID": "6BStglzFvs6FDKMzHbZzV0", "Popularity": 17},
            {"Artist_ID": "7lOC6WJxv8tB3tJWLCw0HK", "Popularity": 6},
            {"Artist_ID": "0HSZWleTsKOcWUQuDXizYk", "Popularity": 7},
            {"Artist_ID": "72yg6tWrGwoPqpiUD25BK7", "Popularity": 19},
            {"Artist_ID": "16NfZBJxDfPQXRUNI9sG8k", "Popularity": 9}
        ]
    }
]

# Create an empty list to hold the data
data = []

# Iterate over each playlist data and extract the required information
for playlist in playlist_data:
    playlist_name = playlist["playlist_name"]
    for artist in playlist["artists"]:
        artist_id = artist["Artist_ID"]
        popularity = artist["Popularity"]
        data.append({"Playlist Name": playlist_name, "Artist_ID": artist_id, "Popularity": popularity})

df = pd.DataFrame(data)

print(df)


df.head()



