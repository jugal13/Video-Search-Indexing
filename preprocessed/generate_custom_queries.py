from read_rgb import cut_rgb_video

params = [
    ['dataset/videos/video4.rgb', './tough-queries/tough4_1.rgb', 306, 721],
    ['dataset/videos/video4.rgb', './tough-queries/tough4_2.rgb', 27735, 28308],
    ['dataset/videos/video4.rgb', './tough-queries/tough4_3.rgb', 28471, 28616],
    ['dataset/videos/video10.rgb', './tough-queries/tough10_1.rgb', 2383, 2908],
    ['dataset/videos/video11.rgb', './tough-queries/tough11_1.rgb', 10998, 11266],
    ['dataset/videos/video11.rgb', './tough-queries/tough11_2.rgb', 6966, 7478]
]

for p in params:
    cut_rgb_video(*p)
    