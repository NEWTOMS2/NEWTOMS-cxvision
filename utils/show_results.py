import cv2 
import json
import os 
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX
text_color = (255, 255, 255) # White
text_color_bbox = (3, 252, 127)
text_color_dwell =  (0, 128, 255) #Orange
bbox_default_color = (255, 0, 0) # Dark blue
label_color=(255, 0, 0)
dwell_color = (3, 252, 127) # Green
service_color = (252, 227, 3) # Light blue

def show_service_and_dwell_areas(image, coor, color, bbox_thickness):
    upper_left, upper_right, lower_right, lower_left = coor
    cv2.line(image, lower_left, lower_right, color, bbox_thickness)
    cv2.line(image, upper_left, upper_right, color, bbox_thickness)
    cv2.line(image, lower_left, upper_left, color, bbox_thickness)
    cv2.line(image, lower_right, upper_right, color, bbox_thickness)

def print_resume(frame, people_labels, fonts_info):
    cv2.rectangle(frame, people_labels["background_box_p1"], people_labels["background_box_p2"], (0,0,0), -1, cv2.LINE_AA)  # filled
    cv2.putText(frame, people_labels["time_label"],(int(0), int(people_labels['height'])) , font, fonts_info["font_scale_label"], text_color, fonts_info["font_thickness"], cv2.LINE_AA)    
    cv2.putText(frame, people_labels["total_detected_people_label"], (people_labels["label_coords"][0][0], people_labels["label_coords"][0][1] + people_labels["h_background"]), font, fonts_info["font_scale_label"], text_color, fonts_info["font_thickness"], cv2.LINE_AA) 
    
    if people_labels["zones"]:
        cv2.putText(frame, 'DWELL: {}'.format(str(people_labels["num_people_dwell"])), people_labels["label_coords"][1], font,  fonts_info["font_scale_label"], text_color, fonts_info["font_thickness"], cv2.LINE_AA)
        cv2.putText(frame, 'SERVICE: {}'.format(str(people_labels["num_people_service"])), people_labels["label_coords"][2], font,  fonts_info["font_scale_label"], text_color, fonts_info["font_thickness"], cv2.LINE_AA)  
    
def set_box_label(frame, box_label, fonts_info):
    cv2.rectangle(frame, box_label["p1"], box_label['p2'], bbox_default_color, thickness=fonts_info['bbox_thickness'], lineType=cv2.LINE_AA)

    if box_label["label_id"]:        
        w, h = cv2.getTextSize(box_label['label_id'], 0, fonts_info['font_scale_label'], thickness=fonts_info['font_thickness'])[0]  # text width, height
        outside = box_label["p1"][1] - h - 3 >= 0  # label fits outside box
        p2 = box_label["p1"][0] + w, box_label["p1"][1] + h + 3
        cv2.rectangle(frame, box_label["p1"], p2, bbox_default_color, -1, cv2.LINE_AA)  # filled
        cv2.putText(frame, box_label["label_id"], (box_label["p1"][0], box_label["p1"][1] + h + 2), 0, fonts_info['font_scale_label'], text_color, thickness=fonts_info['font_thickness'], lineType=cv2.LINE_AA)
        
    if box_label["label_seconds"]:       
        w, h = cv2.getTextSize(box_label.get("label_seconds"), 0, fonts_info['font_scale_label'], thickness=fonts_info['font_thickness'])[0]  # text width, height
        outside = box_label['p3'][1] - h - 3 >= 0  # label fits outside box
        p4 = box_label['p3'][0] + w, box_label['p3'][1] - h - 3 if outside else box_label['p3'][1] + h + 3
        cv2.rectangle(frame, box_label['p3'], p4, label_color, -1, cv2.LINE_AA)  # filled
        cv2.putText(frame, box_label.get("label_seconds"), (box_label['p3'][0], box_label['p3'][1] - 2 if outside else box_label['p3'][1] + h + 2), 0, fonts_info['font_scale_label'], text_color, thickness=fonts_info['font_thickness'], lineType=cv2.LINE_AA)

def apply_blurring(image, box,  blocks=25):
    """Apply blurring"""
    y0 =  box['y0']
    y1 =  box['y1']
    x0 =  box['y0']
    x1 =  box['y1']

    print(box)
    to_blur = image[y0:y1, x0:x1]
            
    (h, w) = to_blur.shape[:2]
    x_steps = np.linspace(0, w, blocks + 1, dtype="int")
    y_steps = np.linspace(0, h, blocks + 1, dtype="int")
    
    for i in range(1, len(y_steps)):
        for j in range(1, len(x_steps)):
            start_x = x_steps[j - 1]
            start_y = y_steps[i - 1]
            end_x = x_steps[j]
            end_y = y_steps[i]
            roi = to_blur[start_y:end_y, start_x:end_x]
            (B, G, R) = [int(x) for x in cv2.mean(roi)[:3]]
            cv2.rectangle(to_blur, (start_x, start_y), (end_x, end_y),
                (B, G, R), -1)

    image[y0:y1, x0:x1] = to_blur

def generate_video(video_path, video_predictions_path):
    # Opening JSON file
    with open(video_predictions_path, 'r') as openfile:
        video_predictions = json.load(openfile)

    # Read raw video
    if not os.path.isfile(video_path):
        raise FileExistsError

    cap = cv2.VideoCapture(video_path)    
    v_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    v_height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    #Create output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_video = cv2.VideoWriter("example-2.mp4", fourcc, int(round(cap.get(cv2.CAP_PROP_FPS))), (v_width, v_height))

    for frame in video_predictions['tracking']:
        ret, video_frame = cap.read() 
        frame_aux = video_frame
        fonts_info = {
            "font_scale_label": video_predictions['font_scale_label'],
            "font_thickness": video_predictions['font_thickness'],
            "bbox_thickness": video_predictions['bbox_thickness'],
        }

        if not video_predictions['areas']['unique_area']:
            show_service_and_dwell_areas(frame_aux, video_predictions['areas']['service_area_coord'], service_color, fonts_info['bbox_thickness'])
            show_service_and_dwell_areas(frame_aux, video_predictions['areas']['dwell_area_coord'], dwell_color, fonts_info['bbox_thickness'])

        print('Blurring people (if necessary)')
        for box_to_blur in frame['boxes_to_blur']:
            apply_blurring(video_frame, box_to_blur)

        print('Drawing bounding boxes')
        for box in frame['boxes']:
            set_box_label(frame_aux, box, fonts_info)

        print('Drawing tracking resume')
        print_resume(frame_aux, frame['people_couting'], fonts_info)
        
        out_video.write(frame_aux) 

