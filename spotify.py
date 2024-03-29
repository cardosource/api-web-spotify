import json
import requests
import base64

class Spotify:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, client_id, client_secret, user):
        if not hasattr(self, 'client_id'):
            self.client_id = client_id
            self.client_secret = client_secret
            self.login(client_id, client_secret, user)
            self.user = user

    def authorizationBasic(self, sec):
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Authorization': f'Basic {sec}'}
        return headers

    def accessToken(self, token):
        return {'Authorization': 'Bearer ' + token}

    def encode(self, client_id, client_secret):
        to_encode = client_id + ':' + client_secret
        return base64.b64encode(to_encode.encode()).decode()

    def login(self, client_id, client_secret, userIS):
        security = self.encode(client_id, client_secret)
        headers = self.authorizationBasic(security)
        params = {'grant_type': 'client_credentials'}
        r = requests.post('https://accounts.spotify.com/api/token', headers=headers, params=params)
        data = json.loads(r.text)
        print("+--------------------------+")
        for i in data.keys():
            print(i, " : ", data[i])
        token = data['access_token']
        print("+--------------------------+")
        print(" [ TOKEN ] : %s " % token)
        header = self.accessToken(token)
        self.user(header, userIS)

    def connect(self, url, headers):
        return requests.get(url=url, headers=headers)

    def status(self, carg, art):
        if carg == 200:
            print("[ --> badabim <-- ]")
            return json.loads    (art.text)
        elif carg == 400:
            print("Ohhh not")
            return json.loads(art.text)

    def user(self, acess, userIS):
        perfil = self.connect(f"https://api.spotify.com/v1/users/{userIS}", acess)
        info = self.status(perfil.status_code, perfil)
        print("+======================================|")
        print('| *user : ', info['display_name'])
        print('| *followers : ', info['followers']['total'])
        print('| *page : ', info['external_urls']['spotify'])
        print("+======================================|")
        self.search(acess)

    def search(self, acess):

       

        my_pref = "rammstein" #<:------------------------- pesquisa
        my_music = self.connect("https://api.spotify.com/v1/search?q=" + my_pref + "&type=artist", headers=acess)
        lindo = self.status(my_music.status_code, my_music)
        # print(lindo)
        for i in lindo["artists"]['items']:  # < -------list \o/
            followers = i['followers']
            banda = i['name']
            idART = i['id']
            popularity = i['popularity']
            url = i["external_urls"]
            print("- . name : ", banda)
            print("+ . popularity : ", popularity)
            print("++. url : ", url['spotify'])
            print("+. followers :", followers['total'])
            print(":==> Genere : ")

            for i in i['genere']:
                print("*. ", i)

        def album(acesso):
            nonlocal idART
            album = self.connect(f"https://api.spotify.com/v1/artists/{idART}/albums", acesso)
            print("----------")
            statusALBUM = self.status(album.status_code, album)
            print("Data Album   |  faixas")
            for alb in statusALBUM['items']:
                data = alb['release_date']

                albumData = f'{data[8:12]}/{data[5:7]}/{data[0:4]}'
                print("%s       %s" % (albumData, alb["total_tracks"]))

        album(acesso=acess)

class SpotifySingleton(Spotify):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

client_id = ""
client_secret = ""
user = ""
