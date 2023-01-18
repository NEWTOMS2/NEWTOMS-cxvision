# CxVision - AWS Marketplace Model Package

**CxVision** offers a computer vision solution focused on improving **user experience** by **tracking people and generating metrics** that **business intelligence applications** can subsequently analyze. 

**CxVision** helps you to:

- **Improve** service quality
- **Optimize** business operations
- **Elevate** customer experience
- **Make** data-driven decisions
- **Convert** clients into fans

![Cxvision gif](./imgs/cxvision-metrics.gif)

## Contents

1. [What does the solution do?](#What-does-the-solution-do?)
2. [How does the solution work?](#How-does-the-solution-work?)
3. [Recommendations](#Recommendations)

## What does the solution do?

This solution allows you to:

* Detect people in videos.
* Count people within a defined zone.
* Measure the time spent in each zone.
* Apply blurring on each person to maintain their privacy.
* Generate data for business intelligence apps.


Furthermore, the solution allows you to define two zones in each video, a waiting zone (Dwell) and a service zone. It will enable you to measure how long a person takes in a queue (waiting zone) and how long it takes while being served (service zone). 

As a result, you'll get metrics that allow you to build business intelligence dashboards to answer questions in near real-time, such as:

- How many people are there in the area?
- What are the average and maximum waiting times per area?
- How many people are being cared for in the area?

![Cxvision gif](./imgs/cxvision.gif)

## How does the solution work?

You can deploy the CxVision Model Package from AWS Marketplace and configure some services needed to run the solution.

The solution is flexible to be consumed in different ways:

1. Real-time: A single video is processed, and its metrics are generated.  [See CxVision Notebook](./CxVision.ipynb)
2. Batch process: A group of videos is processed. [See CxVision Notebook](./CxVision.ipynb)
3. Streaming Videos: In this mode, you can process streaming-related videos in near real-time by executing a trigger for each new video fragment. [See CxVision - Streaming Videos](./StreamingVideos.ipynb)

## Recommendations

1. If the video resolution is greater than 1280 x 720, the solution will resize the video for better processing.
2. For better performance, the video fragments for streaming video processing should have a duration of 180 frames. E.g. 1 video of 6 seconds at 30fps, 1 video of 180 seconds at 1fps.
