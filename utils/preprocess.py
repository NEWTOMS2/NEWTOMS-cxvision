import cv2

def preprocess_video(video, base_output_path="videos"):
    cap = cv2.VideoCapture(video)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))           
    fps = int(round(cap.get(cv2.CAP_PROP_FPS)))
    frame_count =  int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps_interval = fps # If this value is equal to fps, the final video output will be at 1fps. 
    video_duration = int(frame_count / fps_interval)
    fixed_rescale = (1280,720)

    print('Video fps: {}'.format(fps))
    print('Original video Width: {} - Video Height: {}'.format(frame_width, frame_height))
                        
    if (frame_width > fixed_rescale[0]) and (frame_height > fixed_rescale[1]):
        rescale_value = (frame_width / fixed_rescale[0]) if frame_width >= frame_height else (frame_height / fixed_rescale[1])
        print('Resize Scale: {}'.format(rescale_value))
        frame_width = int(frame_width / rescale_value)
        frame_height = int(frame_height / rescale_value)    
        
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_video_path = base_output_path + "/preprocess_" + video.split('/')[1]
    out = cv2.VideoWriter(out_video_path,fourcc,int(fps/fps_interval),(frame_width,frame_height))    
    frame_index = 0
    video_seconds = 0

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            break

        if frame_index % fps_interval == 0:
            print('{}/{}'.format(video_seconds, video_duration))
            video_seconds += 1
            frame_resized = cv2.resize(frame, (frame_width, frame_height),fx=0,fy=0, interpolation=cv2.INTER_CUBIC)
            out.write(frame_resized)
            
        frame_index += 1