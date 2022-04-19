import rumps
import subprocess
import pypresence, time, requests, json, platform # for presence
import os, os.path

default_conf = {
    "client_id": "replaceWithYourClientID",
}

WORKING_DIRECTORY = os.path.join(os.getenv("HOME"), "Library","Application Support","Glance")

# make it a json
def load_conf():
    noConfig = True
    while noConfig:
        if os.path.isfile(f'{os.path.join(WORKING_DIRECTORY, "config.json")}'):
            with open(f'{os.path.join(WORKING_DIRECTORY, "config.json")}', "r") as f:
                conf = json.load(f)
                noConfig = False
        else:
            conf = default_conf
            with open(f'{os.path.join(WORKING_DIRECTORY, "config.json")}', 'x') as fp:
                pass

            with open(f'{os.path.join(WORKING_DIRECTORY, "config.json")}', "w") as f:

                json.dump(conf, f)
                input("Press ENTER to open the new config file in TextEdit. Please fill it in with your client ID, and come back here.\n\
If you need help, please visit https://byemc.xyz/glance/help/gettingstarted#config")
                subprocess.Popen(["open", f'{os.path.join(WORKING_DIRECTORY, "config.json")}'])
                input("Press ENTER to continue after saving the file.")
    return conf

config = load_conf()


r = pypresence.Presence(config["client_id"])
r.connect()

class getSongFrom:
    def spotify():
        # Use OSAscript to get the song name
        # and artist name
        # returns a tuple of (song, artist)
        # if no song is playing, returns None
        try:
            song = subprocess.check_output(['osascript', '-e', 'tell application "Spotify" to name of current track'])
            artist = subprocess.check_output(['osascript', '-e', 'tell application "Spotify" to artist of current track'])
            status = subprocess.check_output(['osascript', '-e', 'tell application "Spotify" to player state as string'])
            return (song.decode('utf-8').strip(), artist.decode('utf-8').strip(), status.decode('utf-8').strip())
        except subprocess.CalledProcessError:
            pass
    def music():
        # still using osascript
        # returns a tuple of (song, artist)

        try:
            song = subprocess.check_output(['osascript', '-e', 'tell application "Music" to name of current track'])
            artist = subprocess.check_output(['osascript', '-e', 'tell application "Music" to artist of current track'])
            status = subprocess.check_output(['osascript', '-e', 'tell application "Music" to player state as string'])
            return (song.decode('utf-8').strip(), artist.decode('utf-8').strip(), status.decode('utf-8').strip())
        except subprocess.CalledProcessError:
            pass
    def itunes():
        # returns a tuple of (song, artist)
        try:
            song = subprocess.check_output(['osascript', '-e', 'tell application "iTunes" to name of current track'])
            artist = subprocess.check_output(['osascript', '-e', 'tell application "iTunes" to artist of current track'])
            status = subprocess.check_output(['osascript', '-e', 'tell application "iTunes" to player state as string'])
            return (song.decode('utf-8').strip(), artist.decode('utf-8').strip(), status.decode('utf-8').strip())
        except:
            return "iTunes isn't open"


class GlanceApp(rumps.App):
    def __init__(self):
        super(GlanceApp, self).__init__("Glance", "", "music.png")
        self.menu = ["MUSIC", "Spotify", "iTunes"]

        self.player = "Music"
        self.song = None
        self.artist = None


    @rumps.clicked("MUSIC")
    @rumps.clicked("Spotify")
    @rumps.clicked("iTunes")
    def changePlayer(self, sender):
        self.player = sender.title
        if sender.title == "MUSIC":
            self.player = "Music"
        
        self.title = f"Changing player..."
        self.status = f"{self.player}"
        # set icon
        if self.player == "Spotify":
            self.icon = "spotify.png"
        elif self.player == "iTunes":
            self.icon = "itunes.png"
        else:
            self.icon = "music.png"

    @rumps.timer(1)
    def update(self, _):
        if self.player == "Spotify":
            song = getSongFrom.spotify()
            self.title = song[0]
            self.status = song[1]
        elif self.player == "iTunes":
            song = getSongFrom.itunes()
            if song == "iTunes isn't open":
                self.title = "iTunes isn't open"
                self.status = "iTunes isn't open"
            self.title = song[0]
            self.status = song[1]
        elif self.player == "Music":
            song = getSongFrom.music()
            self.title = song[0]
            self.status = song[1]
        else:
            self.title = "Error"

        if self.title != self.song or self.status != self.artist:
            self.song = self.title
            self.artist = self.artist

        if song[2] == "playing":
            pass
        elif song[2] == "paused":
            self.title = f"{self.title} (Paused)"
        elif song[2] == "stopped":
            self.title = f"Stopped"

        r.update(state=self.title, details=self.status, small_image=f"{self.player.lower()}")

if __name__ == "__main__":
    GlanceApp().run()