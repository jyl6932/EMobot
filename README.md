# EMobot

With the development of modern society, people are facing serious mental problems such as depression, happiness, and lack of family connection. Expressing their real feeling is an important way to balance mental health. However, people are afraid to express their own feelings with other people. They usually need some comfort area to take off the fake masks such as a home. Therefore, there is a necessary need for people to create a comfort zone at home to express their real emotional feelings.

Our EMobot is your personal emotional health carer. It will create comfort, privacy, and comfort zone for you to express your own feelings. We go using humanize conversation to ask your current feelings and according to your feelings to recommond adequate music. Or you can just simply record your feeling through voice message and recall it later.

![](https://github.com/jyl6932/EMobot/blob/master/IntroImage/cut.png)

Project Lik: https://docs.google.com/presentation/d/1cQQksk3V0y7aBJYp5pXlpaaUDUwxtOO3svfX_hI0bAU/edit#slide=id.g8a23483449_0_144

Demo Link: https://www.youtube.com/watch?v=OSAoHcLSiaE&t=6s

## Pre-requirement
### Hardware
* **Jetson Nano**
![](https://github.com/jyl6932/EMobot/blob/master/IntroImage/jetson%20nano.jpg)
* **Television**（or you can just use the screen monitor and add a speaker to Jetson to output the voice)
* **HDMI cable**（or any other cable which could transform both image and voice signals)
* **Microphone**

### Software(Library)
Arcade, boto3, selenium, Chromium driver
* **Arcade**
  * *Arcade is an easy-to-learn Python library for creating 2D video games. By using this framework, we could build the visualization part.*
* **boto3**
  * *Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python, which allows Python developers to write software that makes use of services like Amazon S3 and Amazon EC2. Here, we gonna use Amazon Polly which turned the text into lifelike speech using deep learning.*
* **selenium**
  * *Selenium is a portable framework for testing web applications. We will use it to do the auto search and click the web browser. By doing that, to finish the music part.*
* **Chromium driver**
  * *WebDriver is an open source tool for automated testing of webapps across many browsers.*

#### SETUP
```
pip install arcade
pip install boto3
pip install selenium
sudo apt-get install chromium-chromedriver
```

## System Flow
### Animation part
Using arcade to build visualization part. It supports a game animation loop and is able to render/display a sprite(PNG image with transparency) with rotation and scaling.



![](https://github.com/jyl6932/EMobot/blob/master/IntroImage/character.gif)



### Voice input/output
Previously I am using pyttsc3 as voice output. It sounds like an alien. Therefore, I decided to use Amazon Polly as the output voice. The voice quality is 100 times better and there is no noticeable delay.

### Function part
* **Music**

Recommend different music lists according to different users' emotions. I decided to play music through the Youtube platform.
Therefore, the search and click function is needed. The best way to do this is by using an automation test suite, which can control a web browser to perform a search on YouTube and play the video from the search result.

* **MessageBox**

Recorded voice message and play it later

### Coordinate system
![](https://github.com/jyl6932/EMobot/blob/master/IntroImage/Work%20Flow.png)

This model is designed to combine all the separate parts altogether. And even the same commands are inputted different responses will be given according to different current states.

## Project Structure
* **Main Loop**
  * *Based on arcade game engine*
    * *emobot.py* 

* **Animation Part**
  * *Build the character*
    * *robot.py*  (build up the character from the ground)
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
    * *speechRecognition.py* (speech to text implementation part)
  * *Build speach output* 
    * *audio.py*
    * *speech.py* (make AWS Polly working, text to speech implementation part I)
    * *intent.py* (give some feedback based on different states, text to speech implementation part II)
    
* **Function Part** (build music and messageBox functions)
  * *Build music part* 
    * *browerServiceJetson.py* (based on Jetson environment) (automatically search and click the web browser according to different keywords)
    * *browerServiceMac.py* (based on Mac environment)
  * *Build messageBox* 
    * *messageBox.py* (recored message and play the message later)
    
* **Control Part** (combined separate parts altogether)
  * *Control center* 
    * *brainStateMachine.py* (give different voice outputs and feedbacks according to different input commands and states)

* **Others** (some useful tools or images)
  * *poppy folder* 
    * *This folder included all the PNG files which are needed to build the character. Include: head, body, left arm, right arm...* 
  * *utilities folder* 
    * *Some basic tools which were used in previous parts. For example: `stopwatch.py` is a tool to time the duration between each state since the state changed. By doing that we can calculate how long the user absent.* 
    
## Running the Project!
### Build your own AWS account first
1. Get your **service key**  from AWS Polly service *AND* Get your **service secret**.
2. Update your key and secret in `speech.py`.
 
### Debugging (Mac, could not use voice input/output function)
1. Update the 6th lines **IS_JETSON = No** in `congfig.py`. And then the code could be suitable for Mac environment.
2. Run `emobot.py` to start the project.

![](https://github.com/jyl6932/EMobot/blob/master/IntroImage/Details.png)

### Application (Jetson)
1. Update the 6th lines **IS_JETSON = Yes** in `congfig.py`. And then the code could be suitable for the Jetson environment.
2. Run `emobot.py` to start the project.
3. Say `Hello` to EMobot and then the robot will be wake up.
4. After wake up, EMobot will greet the user first and then ask users' current emotion. By saying a keyword, the user could express his current emotion to EMobot.(Happy/Angry/Blue(sad))
5. Then, EMobot will ask the user which function he wants to use like `MessageBox` and `Music`. EMobot will wait until the user gives some feedback. Otherwise, he will wait for 5s and ask it again.
6. If the user chooses `MessageBox`, EMobot will ask again whether the user wants to use record a new message or play the previous one. If the user chooses `Record`, he will have 15s to record his current feelings. If user choose `Play`, EMobot will choose a random message from previously recorded messages.
7. If the user chooses `Music`, EMobot will play the music which is relative to the user's current feelings (like happy/angry/sad). EMobot will automatically search and click the video for the user. And it will kindly help users click the full-screen button and also nicely escape the advertises. The user could by saying `Stop` to stop the video otherwise it will automatically stop after the 50s.
(In `browerServiceJetson.py` and `browerServiceMac.py` parts decide the keywords the system search and play. For exmaple: when the user is happy, EMobot will search `happymv2020`.)
8. For all the above functions, after one function finished, the user could decide to move to the other function area or keep in the loop.
9. For each switch part, the user could say `No` to quit the system. Then, EMobot will become an idle state and wait to be activated again.
10. After EMobot is activated, if there is no input for more than the 20s in any state, EMobot will automatically become an idle state. User could say hello to re-activate it again.


## Reference
Thanks to `msubzero2000`, I could build the skeletal animation system from the ground.

Link: https://github.com/msubzero2000/Qrio-public.git
