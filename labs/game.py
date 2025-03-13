import pygame
import time
import os

pygame.init()
pygame.mixer.init()

music_dir = "music"

tracks = [file for file in os.listdir(music_dir) if file.endswith('.ogg')]
current_track = 0


bg = pygame.image.load("mickeyclock.jpeg")
arm = pygame.image.load("arm.png")

bg = pygame.transform.scale(bg, (1024, 888))
arm_min = pygame.transform.scale(arm, (40,360))
arm_sec = pygame.transform.scale(arm, (50,480))

minute_rect = arm_min.get_rect(center=(512, 444))
second_rect = arm_sec.get_rect(center=(512, 444))


screen = pygame.display.set_mode((1024, 1440))
pygame.display.set_caption("Mickey Mouse Clock")

pygame.mixer.music.load(os.path.join(music_dir, tracks[current_track]))

is_playing = False
is_paused = False

running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(bg, (0, 0))

    t = time.localtime()
    min_angle = -(t.tm_min % 60) * 6
    sec_angle = -(t.tm_sec % 60) * 6

    rotate_min = pygame.transform.rotate(arm_min, min_angle)
    rotate_sec = pygame.transform.rotate(arm_sec, sec_angle)

    _min_rect = rotate_min.get_rect(center=(512, 444))
    _sec_rect = rotate_sec.get_rect(center=(512, 444))

    screen.blit(rotate_min, _min_rect.topleft)
    screen.blit(rotate_sec, _sec_rect.topleft)



    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if is_playing:
                    pygame.mixer.music.pause()
                    is_paused = True
                    is_playing = False
                elif is_paused:
                   pygame.mixer.music.unpause()
                   is_playing = True
                   is_paused = False
                else:
                    pygame.mixer.music.play()
                    is_playing = True

            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
                is_playing = False
                is_paused = False

            elif event.key == pygame.K_RIGHT:  # Next Track
                current_track = (current_track + 1) % len(tracks)
                pygame.mixer.music.load(os.path.join(music_dir, tracks[current_track]))
                pygame.mixer.music.play()
                is_playing = True
                is_paused = False

            elif event.key == pygame.K_LEFT:  # Previous Track
                current_track = (current_track - 1) % len(tracks)
                pygame.mixer.music.load(os.path.join(music_dir, tracks[current_track]))
                pygame.mixer.music.play()
                is_playing = True
                is_paused = False


    pygame.time.delay(1000)

    
pygame.quit()