# EMobot

With the development of modern society, people are facing serious mental problems such as depression, happiness, and lack of family connection. Expressing their real feeling is an important way to balance mental health. However, people are afraid to express their own feelings with other people. They usually need some comfort area to take off the fake masks such as a home. Therefore, there is a necessary need for people to create a comfort zone at home to express their real emotional feelings.

Out EMobot is your personal emotional health carer. It will create comfort, privacy, and comfort zone for you to express your own feelings. We go using humanize conversation to ask your current feelings and according to your feelings to recommond adequate music. Or you can just simply record your feeling through voice message and recall it later.

![](https://github.com/jyl6932/EMobot/blob/master/IntroImage/cut.png)

Project Lik: https://docs.google.com/presentation/d/1cQQksk3V0y7aBJYp5pXlpaaUDUwxtOO3svfX_hI0bAU/edit#slide=id.g8a23483449_0_144

Demo Link: https://www.youtube.com/watch?v=OSAoHcLSiaE&t=6s

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

#### Coordinate system
![](https://github.com/jyl6932/EMobot/blob/master/IntroImage/Work%20Flow.png)

This model is designed to combine all the separate parts altogether. And even the same commonds are inputted different responses will be given according to different current states.

## Project Structure
* **Main Loop**
  * *Based on arcade game engine*
    * *emobot.py* 

* **Animation Part**
  * *Build the character*
    * *robot.py*  (build up the character from ground)
    * *robotPart.py* 
  * *Build a skeletal animation system(SAS)* (By doing that we could join several objects together in a hierarchical relationship. Thus, when you apply a transformation to an object, it will also affect all of its children)
    * *morphTarget.py*
    * *morphTargetCore.py*
    * *morphTargetInterp.py*
  * *Let the character move!*
    * *animation.py*
    * *animationCore.py*
    * *fidgetAnimationController.py*

* **Speach Input/Output Part** (build speach as input commonds and also output voice)
  * *Build speach input* 
    * *speechRecognition.py*
  * *Build speach output* 
    * *audio.py*
    * *speech.py* (make AWS Polly working)
    * *intent.py* (give some feedback based on different states)
    
* **Function Part** (build music and messageBox functions)
  * *Build music part* 
    * *browerServiceJetson.py* (based on Jetson environment)
    * *browerServiceMac.py* (based on Mac environment)
  * *Build messageBox* 
    * *messageBox.py* (recored message and play the message later)
    
* **Control Part** (combined seperate parts all together)
  * *Control center* 
    * *brainStateMachine.py* (give differenct voice output according to differenct input commonds and states)
    
## Running the Project!
### Build your own AWS account first
1. Get your **service key**  from AWS Polly service *AND* Get your **service secret**.
2. Update your key and secret in `speech.py`.
 
### Debugging (Mac, could not use voice input/output function)
1. Update the 6 lines **IS_JETSON = No**. And then the code could be suitable for Mac environmnet.
2. Run `emobot.py` to start the project.

### Application (Jetson)
1. Update the 6 lines **IS_JETSON = Yes**. And then the code could be suitable for Jetson environmnet.
2. Run `emobot.py` to start the project.
3. Give your commonds according to conversation guidline. Mainly `Yes` and `No` to control the emobot. And also when the emobot is playing the video, you can also using `Stop` commond to stop it. Otherwise, it will automatically stop after 50s.


## Reference
Link: https://github.com/msubzero2000/Qrio-public.git
