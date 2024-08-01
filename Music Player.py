import os
import pygame
from tkinter import Tk, Frame, Button, filedialog

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("300x200")

        self.frame = Frame(self.root)
        self.frame.pack()

        self.play_button = Button(self.frame, text="Play", command=self.play)
        self.play_button.pack(side="left")

        self.pause_button = Button(self.frame, text="Pause", command=self.pause)
        self.pause_button.pack(side="left")

        self.stop_button = Button(self.frame, text="Stop", command=self.stop)
        self.stop_button.pack(side="left")

        self.open_button = Button(self.frame, text="Open Folder", command=self.open_folder)
        self.open_button.pack(side="left")

        pygame.init()
        pygame.mixer.init()

        self.is_paused = False
        self.music_files = []
        self.current_index = 0

    def play(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            if not pygame.mixer.music.get_busy():
                self.load_and_play()

    def pause(self):
        pygame.mixer.music.pause()
        self.is_paused = True

    def stop(self):
        pygame.mixer.music.stop()

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.music_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.mp3', '.wav', '.ogg'))]
            self.music_files.sort()
            self.current_index = 0
            if self.music_files:
                self.load_and_play()

    def load_and_play(self):
        if self.music_files:
            pygame.mixer.music.load(self.music_files[self.current_index])
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            self.root.after(100, self.check_music_end)

    def check_music_end(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.current_index = (self.current_index + 1) % len(self.music_files)
                self.load_and_play()
        self.root.after(100, self.check_music_end)

if __name__ == "__main__":
    root = Tk()
    app = MusicPlayer(root)
    root.mainloop()
