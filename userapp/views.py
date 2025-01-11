import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
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
      
      return Response({"message": "Usuario eliminado"})
    except User.DoesNotExist:
      return Response({'detail': 'Usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

class SpotifyAPIView(APIView):
  def get(self, request, pk):
    try:
      user = User.objects.get(pk=pk)
    except User.DoesNotExist:
      return Response({'detail': 'Usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
      

    artista_fav = user.preferences

    # Connect to spotify api
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

    rec = 'browse/new-releases' #url obtiene nuevos lanzamientos
    featured_playlists_url = ''.join([base_url,rec])

    response = requests.get(featured_playlists_url,headers=headers).json()['albums']['items']

    artistas = [res['artists'][0] for res in response]

    nombres_artista = [res2['name'] for res2 in artistas]

    art_index = [art for art in nombres_artista].index(artista_fav)

    info = {
     'artista': nombres_artista[art_index],
     'album': response[art_index]['name'],
     'fecha': response[art_index]['release_date'],
     'canciones': response[art_index]['total_tracks']
    }

    serializer = UserSerializer(info)
    
    return Response(info)