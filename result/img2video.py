import cv2
import os
 
#图片路径
im_dir = "."
#输出视频路径
video_dir = 'Final_video.mp4'
fps = 2
#图片数 
num = 34
#图片尺寸
img_size = (256,256)
 
 
# fourcc = cv2.cv.CV_FOURCC('M','J','P','G')#opencv2.4
# fourcc = cv2.VideoWriter_fourcc('I','4','2','0') 
 
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')        # 设置输出视频为mp4格式
videoWriter = cv2.VideoWriter(video_dir, fourcc, fps, img_size)
 
 
 
for i in range(num):
    name = f"My Maze_result_{i}.png"
    im_name = os.path.join(im_dir, name)
    print(im_name)
    frame = cv2.imread(im_name,1)
    videoWriter.write(frame)
 
videoWriter.release()
print('finish')