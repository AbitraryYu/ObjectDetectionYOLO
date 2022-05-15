# Object Detection by YOLO

This serves an complete walkthrough of how the author (AbitraryYu) accomplish his YOLO project in his FYP. The purpose of this guideline is to provide a concrete ground for newcomers to know YOLO, and possibly extend, research the project (or parts of the YOLO project) as a whole.



[TOC]

## Foreword

This repository contains all deliverables of an FYP, including proposal, interim report, final report and presentations. Since this project is conduct online, there is also an pre-recorded demo in this repository. For people whom wish to get a glance of how YOLO works, you can simply read this document. If you wish to follow through the implementation process, there are videos which are segmented into chapters.

- [ ] Videos
- [x] Deliverables
- [ ] Documentation

**This project is done in 2021/4/14 and will not be maintained. If you experience installation failure or program crash due to OS/library updates, you may need to consult the latest darknet/opencv repository, OS troubleshooting guide or handle it your own.**

# Introduction

YOLO (You only look once) is an object detection algorithm for real time usage. I am using [AlexeyAB's repository](https://github.com/AlexeyAB/darknet) for my primary reference. 



# Training your own custom dataset

You can refer to my [collab notebook](https://colab.research.google.com/drive/1qke-dIgsnCK5DXHN-or_DMBZxGJ64TAe?usp=sharing) if you want to get to know how training YOLO models are like.

# Demonstration

You can refer to [my repository](https://github.com/AbitraryYu/ObjectDetectionYOLO) to get a quick glimpse of running YOLO in real time.

There are three scripts that you can run.

```
python yolo.py -w <your weights> -cfg <your cfg file> -l <obj names> -u
```

omit -u if you have no gpu opencv install from source.

```
python sendmsgtobot.py
```

```
python telegrambot.py
```

`telegrambot.py` use to receive updates and stuff `sendmsgtobot.py` will send msg to bot when `yolo.py` detects something.
