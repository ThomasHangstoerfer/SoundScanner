import os, sys, pygame, math, numpy

from pygame.locals import *

import pygame.camera

width = 640
height = 480


bits = 16
pygame.mixer.pre_init(44100, -bits, 2)

pygame.init()
# pygame.camera.init()
# cam = pygame.camera.Camera("/dev/video0", (width, height))
# cam.start()





duration = 1.0          # in seconds
# freqency for the left speaker
frequency_l = 440
# frequency for the right speaker
frequency_r = 550

# this sounds totally different coming out of a laptop versus coming out of headphones

sample_rate = 44100

print('HIER')

n_samples = int(round(duration*sample_rate))

# setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
max_sample = 2**(bits - 1) - 1

for s in range(n_samples):
    t = float(s)/sample_rate    # time in seconds

    # grab the x-coordinate of the sine wave at a given time,
    # while constraining the sample to what our mixer is set to with "bits"
    buf[s][0] = int(round(max_sample*math.sin(2*math.pi*frequency_l*t)))        # left
    buf[s][1] = int(round(max_sample*0.5*math.sin(2*math.pi*frequency_r*t)))    # right

sound = pygame.sndarray.make_sound(buf)
# play once, then loop forever
# sound.play(loops = -1)

channel1 = pygame.mixer.Channel(0) # argument must be int
channel2 = pygame.mixer.Channel(1)
channel1.play(sound, loops = -1)

print('HIER')





windowSurfaceObj = pygame.display.set_mode((width, height), 1, 16)
pygame.display.set_caption('Scanner')

# image = cam.get_image()
image = pygame.image.load("test.png")
# cam.stop()

catSurfaceObj = image
windowSurfaceObj.blit(catSurfaceObj, (0, 0))

ticks = pygame.time.get_ticks()

clck = pygame.time.Clock()
scannerpos = 50
scannerwidth = 4

pygame.display.update()
while True:
    clck.tick(40)
    # print("ticks: %i" % ticks)
    for event in pygame.event.get():
        # print('event: ', event)
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            print('KEYDOWN event.unicode = %s' % event.unicode)
            # print('KEYDOWN pygame.K_q = %s' % pygame.K_q)
            if event.key == pygame.K_q:
                print('Q')
                sys.exit()
            if event.key == pygame.K_p:
                print('p')
                channel1.pause()
            if event.key == pygame.K_l:
                print('l')
                channel1.unpause()

    # if pygame.time.get_ticks() - ticks > 50:
    # ballrect = ballrect.move(speed)
    #    ticks = pygame.time.get_ticks()

    #if ballrect.left <= 0 or ballrect.right >= width:
    #    beschleunige()
    #    speed[0] = -speed[0]
    # if ballrect.top <= 0 or ballrect.bottom >= height:
    #    beschleunige()
    #    speed[1] = -speed[1]

    # screen.fill(black)
    # screen.blit(text, (320 - text.get_width() // 2, 240 - text.get_height() // 2))
    # screen.blit(text, (0, 0))

    # screen.blit(wolf, wolfrect)
    # screen.blit(sheep, sheeprect)

    catSurfaceObj = image.copy()
    # with pygame.PixelArray(catSurfaceObj) as pa:
        # pa[100:110, 100:110] = pygame.Color(255, 0, 255)
        # pa.close()

    pa = pygame.PixelArray(catSurfaceObj)
    pa[scannerpos:scannerpos + scannerwidth, :] = pygame.Color(255, 100, 100)
    pa[scannerpos-1:scannerpos, :] = pygame.Color(255, 0, 255)
    pa[scannerpos+scannerwidth+1:scannerpos+scannerwidth+2, :] = pygame.Color(255, 0, 255)

    # TODO scanner-bar as own surface and use Surface.scroll() to move it over the screen
    scannerpos += scannerwidth
    scannerpos = scannerpos % width
    del pa
    windowSurfaceObj.blit(catSurfaceObj, (0, 0))
    # windowSurfaceObj.blit(image, (0, 0))

    pygame.display.flip()
