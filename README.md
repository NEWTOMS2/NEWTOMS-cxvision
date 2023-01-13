# CxVision - AWS Marketplace Model Package

CxVision offers a computer vision solution for tracking people and generate metrics that can be subsequently analyzed to improve the user experience.

This solution allows you to:

* Detect people in videos.
* Count people within a defined zone.
* Measure the spent time in each zone.
* Apply blurring on each person to maintain their privacy.


## Contents

1. [What does the solution do?](#What-does-the-solution-do?)
2. [How does the solution work?](#How-does-the-solution-work?)
    - [Processing independent videos](#1.-Processing-independent-videos)
    - [Processing stream videos](#2.-Processing-stream-videos)
        - [Continuous video upload to Amazon S3 Bucket](#Continuous-video-upload-to-Amazon-S3)
3. [Recommendations](#Recommendations)
        
## What does the solution do?

The solution allows you to define two zones in each video, a waiting zone (Dwell) and a service zone. This allows you to measure how long a person takes in queue (waiting zone) and how long it takes while being served (service zone). 

![Cxvision gif](./imgs/cxvision.gif)

> It's not necessary to define the zones. In this case, the solution will measure the time of all the people in the video.

## How does the solution work?

You can deploy the CxVision Model Package from AWS Marketplace and then configure some services needed to run the solution.
The solution could be consumed in two different ways: In real-time or through a batch transform job.

> CxVision also allows you to process streaming related videos in near real-time by executing a trigger for each new video fragment. [See CxVision - Streaming videos][./StreamingVideos.ipynb]

## Recommendations

1. If the video resolution is greater than 1280 x 720, the solution will resize the video for better processing. However, it could take some time, so we recommend using a resolution lower than 1280 x 720.

2. For better performance, the video fragments for the streaming videos processing should have a duration less or equal than 60 seconds.
