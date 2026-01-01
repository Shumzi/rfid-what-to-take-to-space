import vlc
import json

class VideoPlayer:
    def __init__(self) -> None:
        self.instance = vlc.Instance("--fullscreen", "--no-video-title-show")
        self.player = self.instance.media_player_new()
        self.playlist_player = self.instance.media_list_player_new()
        self.playlist_player.set_media_player(self.player)
        self.config = json.load(open('config.json','r'))
        self.welcome_video = self.instance.media_new(self.config['welcome_video'])
        self.play_welcome()

    def _on_end(self, event):
        """
        since our playlist contains the video + welcome screen, 
        when we start a new media (i.e. the welcome screen), we want the playlist to repeat it infinitly.
        """
        self.playlist_player.set_playback_mode(vlc.PlaybackMode.repeat)

    def set_on_end(self,):
        event_manager = self.player.event_manager()
        self._end_callback = lambda event: self._on_end(event)
        event_manager.event_attach(vlc.EventType.MediaPlayerMediaChanged , self._end_callback)

    # def show_welcome(self):
    #     media = self.instance.media_new(self.config['welcome_video'])
    #     self.player.set_media(media)
    #     self.player.play()

    def play_video(self, path):
        self.playlist_player.set_playback_mode(vlc.PlaybackMode.default)
        media = self.instance.media_new(path)
        playlist = self.instance.media_list_new()
        playlist.add_media(media)
        playlist.add_media(self.welcome_video)
        self.playlist_player.set_media_list(playlist)
        self.playlist_player.play_item_at_index(0)

    def play_welcome(self):
        self.play_video(self.config['welcome_video'])

if __name__=="__main__":
    v = VideoPlayer()
    while True:
        res = input()
        v.play_video(r"data\images\video_short.mp4")
