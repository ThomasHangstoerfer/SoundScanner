import os, sys, pygame, math, numpy

from pygame.locals import *

import pygame.camera

width = 640
height = 480
line_count = 5
line_height = height / line_count


def initSound(freq_l, freq_r):
    duration = 1.0          # in seconds
    # freqency for the left speaker
    #frequency_l = 440
    frequency_l = freq_l
    # frequency for the right speaker
    #frequency_r = 550
    frequency_r = freq_r

    # this sounds totally different coming out of a laptop versus coming out of headphones

    sample_rate = 44100

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

    return pygame.sndarray.make_sound(buf)

def draw_line(windowSurfaceObj, line_idx):
    pygame.draw.line(windowSurfaceObj, (255, 100, 100), (0, line_height*line_idx-2), (width, line_height*line_idx-2), 2)
    pygame.draw.line(windowSurfaceObj, (255, 0, 0), (0, line_height*line_idx), (width, line_height*line_idx), 1)
    pygame.draw.line(windowSurfaceObj, (255, 100, 100), (0, line_height*line_idx+1), (width, line_height*line_idx+1), 2)

bits = 16
pygame.mixer.pre_init(44100, -bits, 2)

image = None
cam = None
static_image = True
pygame.init()
pygame.camera.init()
if len(pygame.camera.list_cameras()) > 0 and not static_image:
    print('found')
    cam = pygame.camera.Camera("/dev/video0", (width, height))
    print('Cam: ', cam )
    cam.start()
    image = cam.get_image()

else:
    print('no camera found')
    image = pygame.image.load("test.png")

sound0 = initSound(523, 659)
sound1 = initSound(440, 554)
sound2 = initSound(261, 329)

channel0 = pygame.mixer.Channel(0)
channel1 = pygame.mixer.Channel(1)
channel2 = pygame.mixer.Channel(2)
channel3 = pygame.mixer.Channel(3)
channel4 = pygame.mixer.Channel(4)

channel0.play(sound0, loops = -1)
channel1.play(sound1, loops = -1)
channel2.play(sound2, loops = -1)
channel3.play(sound2, loops = -1)
channel4.play(sound2, loops = -1)

channel0.pause()
channel1.pause()
channel2.pause()
channel3.pause()
channel4.pause()

channels = [channel0, channel1, channel2, channel3, channel4]

scannerBar = pygame.Surface((10, height))
pa = pygame.PixelArray(scannerBar)
pa[0:1, :] = pygame.Color(100, 100, 255)
pa[1:4, :] = pygame.Color(180, 180, 255)
pa[4:6, :] = pygame.Color(255, 255, 255)
pa[6:8, :] = pygame.Color(100, 100, 255)
pa[8:9, :] = pygame.Color(180, 180, 255)
del pa

windowSurfaceObj = pygame.display.set_mode((width, height), 1, 16)
pygame.display.set_caption('Scanner')

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
                channel0.pause()
            if event.key == pygame.K_l:
                print('l')
                channel0.unpause()

    catSurfaceObj = image.copy()

    pa = pygame.PixelArray(image)
    scan_col = pa[scannerpos, :]

    for l in range(line_count):
        play_line = False
        for i in range(line_height):
            if scan_col[l*line_height + i] == 0:
                play_line = True

        #print('play_line %i: %i' % (l, play_line))
        if play_line:
            channels[l].unpause()
        else:
            channels[l].pause()

    del pa


    #print('scan_col : ', scan_col)

    catSurfaceObj.blit(scannerBar, (scannerpos, 0))

    scannerpos += scannerwidth
    if scannerpos > width:
        scannerpos = scannerpos % width
    if scannerpos % 10 == 0:
        if cam != None:
            image = cam.get_image()

    windowSurfaceObj.blit(catSurfaceObj, (0, 0))


    draw_line(windowSurfaceObj, 1)
    draw_line(windowSurfaceObj, 2)
    draw_line(windowSurfaceObj, 3)
    draw_line(windowSurfaceObj, 4)

    pygame.display.flip()
