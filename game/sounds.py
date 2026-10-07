import pygame
import math
from array import array


class SoundManager:
    def __init__(self):
        # Make sure the audio mixer is initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init(
                frequency=44100,
                size=-16,
                channels=1,
                buffer=512
            )

        pygame.mixer.set_num_channels(8)

    def play_go(self):
        """Sound when the screen turns green."""
        self._play_tone(880, 250)

    def play_success(self):
        """Sound for a successful reaction."""
        self._play_tone(1200, 150)

    def play_false_start(self):
        """Warning sound for a false start."""
        self._play_tone(300, 400)

    def play_game_over(self):
        """Sound when the game is completed."""
        self._play_tone(600, 200)
        pygame.time.delay(80)
        self._play_tone(900, 250)

    def _play_tone(self, frequency, duration):
        """Generate and play an audible sine-wave tone."""

        sample_rate = 44100
        samples = int(sample_rate * duration / 1000)

        sound_data = array("h")

        for i in range(samples):
            value = int(
                32767
                * 0.8
                * math.sin(
                    2 * math.pi * frequency * i / sample_rate
                )
            )

            sound_data.append(value)

        sound = pygame.mixer.Sound(
            buffer=sound_data.tobytes()
        )

        sound.set_volume(1.0)
        sound.play()