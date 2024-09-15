from time import time
import wave
import pygame as pg
import pyaudio

W, H = 160, 120
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

pg.init()
screen = pg.display.set_mode((W, H))
p = pyaudio.PyAudio()

def write_frames(frames: list[bytes]) -> None:
    with wave.open('out.wav', 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def draw_recording(surf: pg.Surface) -> pg.Rect:
    return pg.draw.circle(surf, (255, 0, 0), (W // 2, H // 2), min(W, H) // 4)

stream = p.open(rate=RATE, channels=CHANNELS, format=FORMAT, input=True)

is_running = True
is_recording = False
frames: list[bytes] = []
t0 = time()
blink = True

while is_running:
    for event in pg.event.get():
        if event.type != pg.KEYUP: continue
        match event.key:
            case pg.K_q: is_running = False
            case pg.K_r:
                is_recording = not is_recording
                print(('stop', 'start')[is_recording], 'recording')
            case pg.K_s:
                write_frames(frames)
                print('saved')
                frames = []
    data = stream.read(1024)
    if is_recording:
        frames.append(data)
    screen.fill((0, 0, 0))
    if is_recording:
        if time() - t0 > 0.5:
            blink = not blink
            t0 = time()
        if blink: draw_recording(screen)
    pg.display.flip()

stream.close()
p.terminate()
