# This essentially does the same thing as pygame.time.Clock.

import pygame

class FrameTimer:
    def __init__(self, target_fps):
        self.target_fps = target_fps
        self.__ms_per_frame = 1000.0 / self.target_fps
        self.start_time = 0
        self.end_time = 0
        self.elapsed_time = 0

    def begin_frame(self):
        self.start_time = pygame.time.get_ticks()

    def end_frame(self):
        self.end_time = pygame.time.get_ticks()
        self.elapsed_time = self.end_time - self.start_time
        wait_time = self.__ms_per_frame - self.elapsed_time
        if wait_time < 0:
            print("Experiencing lag: " + str(wait_time) + "s")
        elif wait_time > 1:
            pygame.time.delay(int(wait_time))
        pygame.time.wait(0)
