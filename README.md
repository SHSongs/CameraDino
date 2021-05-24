# CameraDino

## Play chrome dino with camera
This is a JUMP detection using optical flow.

## [[Blog]Algorithms](https://shsongs.github.io/CameraDino/)
Summary  
Calculate the momentum using the optical flow. Momentum above the threshold, it is judged to be a jump.  
Threshold is the average of the previous 50 frame momentum.  

## How To Play
1. Chrominm address bar  
```
chrome://dino/
```
2. Excute python
```
python Game.py
```
3. Focus Chrome dino game page

### Demo
#### Raspberry Pi 4
<img src="1Play.gif" height="300">  
<img src="2Play.gif" height="300">  

#### Intel laptop
<img src="Demo.png" height="400">  
<img src="Demo.gif" height="400">

## Dependencies
python3 
```
OpenCV
pynput
```
Chorme