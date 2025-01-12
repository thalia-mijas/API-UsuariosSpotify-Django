import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import User
from .serializers import UserSerializer
from .environment import client_id, client_secret
 
class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def destroy(self, request, pk=None):
    try:
      user = User.objects.get(pk=pk)
      user.delete()
      return Response({'detail': 'Usuer eliminaded'})
    except User.DoesNotExist:
      return Response({'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

class SpotifyAPIView(APIView):
  def get(self, request, pk):

    try:
      user = User.objects.get(pk=pk)
    except User.DoesNotExist:
      return Response({'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
      
    fav_artist = user.preferences

    # Connect to spotify API
    auth_url = 'https://accounts.spotify.com/api/token'

    data = {
      'grant_type': 'client_credentials',
      'client_id': client_id,
      'client_secret': client_secret,
    }

    auth_response = requests.post(auth_url, data=data)

    access_token = auth_response.json().get('access_token')

    base_url = 'https://api.spotify.com/v1/'

    headers = {
      'Authorization': 'Bearer {}'.format(access_token)
    }

    rec = 'browse/new-releases' #url has new releases
    featured_playlists_url = ''.join([base_url,rec])

    response = requests.get(featured_playlists_url,headers=headers).json()['albums']['items']

    artists = [res['artists'][0] for res in response]

    artist_name = [res2['name'] for res2 in artists]

    try:
      art_index = [art for art in artist_name].index(fav_artist)
    except:
      return Response({'detail': 'Artist has no new releases'}, status=status.HTTP_200_OK)

    info = {
     'artista': artist_name[art_index],
     'album': response[art_index]['name'],
     'fecha': response[art_index]['release_date'],
     'canciones': response[art_index]['total_tracks']
    }
    
    return Response(info)