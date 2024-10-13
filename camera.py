import asyncio
import cv2
from picamera2 import Picamera2, Preview
from ultralytics import YOLO
import time
import utils
import httpx
actions_url = 'http://miharpi:8000/bark'
async def call_dog(sound_file: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{actions_url}/{sound_file}')
        
async def main():
    # Initialize the Picamera2
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (720, 720)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    #picam2.start_preview(Preview.DRM)
    picam2.start()
    
    # Load the YOLOv8 model
    model = YOLO("yolov8n_ncnn_model")
    counter = 0
    object_counter = 0
    while True:
        # Capture frame-by-frame
        frame = picam2.capture_array()
        frame = frame[::-1,::-1]
        # Run YOLOv8 inference on the frame
        results = model(frame)

        for result in results[0]:
            index = int(result.boxes.cls.tolist()[0])  # Print detection boxes
            object_type = utils.img_classes[index]
            print(f'{object_type}')
            print('\n-----------------------\n')
            # Visualize the results on the frame
            annotated_frame = result.plot()
            if object_type=='bird':
                await call_dog('mixkit-giant-dog-aggressive-growl-59.wav')
            if object_type=='person':
                await call_dog('mixkit-dog-barking-twice-1.wav')
            
            # Display the resulting frame
            #cv2.imshow("Camera", annotated_frame)
            cv2.imwrite(f'photos/Camera_object_{object_counter}.png', annotated_frame)
        
            # Break the loop if 'q' is pressed
            time.sleep(2)
            object_counter +=1
        counter+=1
        if cv2.waitKey(1) == ord("q") or counter==4:
            break
    
    # Release resources and close windows
    cv2.destroyAllWindows()
    picam2.close()


if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())