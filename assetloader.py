import pygame
from constants import *
from utils import *


class AssetLoader:
    card_images = []
    sound_channels: list[pygame.mixer.Channel] = []
    free_stack_image = None
    full_stack_image = None
    pickup_sound = None
    place_sound = None
    music = None

    @staticmethod
    def play_sound(sound: pygame.mixer.Sound, volume=0.3, loop=False):
        for channel in AssetLoader.sound_channels:
            if channel.get_busy():
                continue
            channel.set_volume(volume)
            channel.play(sound, loops=-loop)
            break

    @staticmethod
    def init():
        for _ in range(5):
            AssetLoader.sound_channels.append(pygame.mixer.Channel(_+1))
        AssetLoader.pickup_sound = load_sound("pickup.ogg")
        AssetLoader.place_sound = load_sound("place.ogg")
        AssetLoader.music = load_sound("music.ogg")
        AssetLoader.play_sound(AssetLoader.music, loop=True)
        AssetLoader.card_images = [
            load_image("1.png"),
            load_image("2.png"),
            load_image("3.png"),
            load_image("4.png"),
            load_image("5.png"),
            load_image("6.png"),
            load_image("7.png"),
            load_image("8.png"),
            load_image("9.png"),
            load_image("10.png")
        ]
        AssetLoader.free_stack_image = load_image("free-slot.png")
        AssetLoader.full_stack_image = load_image("full-stack.png")