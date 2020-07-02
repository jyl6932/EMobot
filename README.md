# EMobot

With the development of modern society, people are facing serious mental problems such as depression, happiness, and lack of family connection. Expressing their real feeling is an important way to balance mental health. However, people are afraid to express their own feelings with other people. They usually need some comfort area to take off the fake masks such as a home. Therefore, there is a necessary need for people to create a comfort zone at home to express their real emotional feelings.

Out EMobot is your personal emotional health carer. It will create comfort, privacy, and comfort zone for you to express your own feelings. We go using humanize conversation to ask your current feelings and according to your feelings to recommend adequate music. Or you can just simply record your feeling through voice message and recall it later.

![](https://github.com/jyl6932/EMobot/blob/master/IntroImage/cut.png)

Demo Link:https://www.youtube.com/watch?v=OSAoHcLSiaE&t=6s

## Pre-requirement
### Hardware
Jetson Nano
![](https://github.com/jyl6932/EMobot/blob/master/IntroImage/jetson%20nano.jpg)

### Software(Library)
Arcade, boto3, selenium, Chromium driver

#### SETUP
```
pip3 install arcade
pip3 install boto3
pip3 install selenium
sudo apt-get install chromium-chromedriver
```

## System Flow
### Animation part
Using arcade to build visualization part. It supports a game animation loop and is able to render/display a sprite(PNG image with transparency) with rotation and scaling.



![](https://github.com/jyl6932/EMobot/blob/master/IntroImage/character.gif)



### Voice input/output
Previously I am using pyttsc3 as voice output. It sounds like an alien. Therefore, I decided to use Amazon Polly as the output voice. The voice quality is 100 times better and there is no noticeable delay.

### Function part
#### Music 
Recommend different music lists according to different users' emotions. I decided to play music through the Youtube platform.
Therefore, the search and click function is needed. The best way to do this is by using an automation test suite, which can control a web browser to perform a search on YouTube and play the video from the search result.

#### MessageBox
Recorded voice message and play it later

### Coordinate system
![](https://github.com/jyl6932/EMobot/blob/master/IntroImage/Work%20Flow.png)

This model is designed to combine all the separate parts altogether. And even the same commands are inputted different responses will be given according to different current states.
