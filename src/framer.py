import canny
import cv2
import subprocess

# PHASE0 :: Creating a Working Environment
def env_setup(output_path):
    print("-------------------- Phase0 - Environment Setup --------------------")
    print("[+] Creating Uitlity Directory " + output_path + "/output")
    print("[+] Creating Uitlity Directory " + output_path + "/output/frames")
    print("[+] Creating Uitlity Directory " + output_path + "/output/edge_frames")
    cmd = "cd " + output_path + ";" + "mkdir output" + ";" + "cd output" + ";" + "mkdir frames" + ";" + "mkdir edge_frames"
    subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# PHASE1 & PHASE2 :: Extracting & Detecting
def FrameCapture(input_path, output_path):
    vidObj = cv2.VideoCapture(input_path)
    count = 0
    success = 1
    print("-------------------- Phase1 - Extracting Frames --------------------")
    while success:
        frame_path = output_path + "/output/frames/frame" + str(count) + ".jpg"
        print("[+] Capturing Frame " + frame_path)
        success, image = vidObj.read()
        cv2.imwrite(frame_path, image)
        count += 1

    print("-------------------- Phase2 - Canny Edge Detection --------------------")
    for i in range(count-1):
        edge_frame_path = output_path + "/output/edge_frames/frame" + str(i) + ".jpg"
        frame_path = output_path + "/output/frames/frame" + str(i) + ".jpg"
        print("[+] Edge Detection on " + edge_frame_path)
        edge_image = canny.detect(frame_path)
        cv2.imwrite(edge_frame_path, edge_image)

# PHASE3 :: Assembling Calculated Frames Back to a Video
def FrametoStream(output_path):
    print("-------------------- Phase3 - Assembling the Frames into a Stream --------------------")
    print("[+] Generated Video on " + output_path)
    command = "cd " + output_path + "/output/edge_frames" + ";" + "ffmpeg -framerate 60 -i frame%d.jpg video.mp4;" + "mv video.mp4 " + "../.."
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# PHASE4 :: Cleaning our Working Environment
def env_cleanup(output_path):
    print("-------------------- Phase4 - Environment Cleanup --------------------")
    print("[+] Deleting Uitlity Directory " + output_path + "/output")
    cmd  = "rm -rf " + output_path + "/output"
    subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# PHASE5 :: Preforming our Video Operations
def execute(input_path, output_path):
    env_setup(output_path)
    FrameCapture(input_path, output_path)
    FrametoStream(output_path)
    env_cleanup(output_path)
