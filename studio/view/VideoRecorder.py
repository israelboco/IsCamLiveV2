import cv2
import time
import os

from kivymd.utils import asynckivy


class VideoRecorder:

    # Video class based on openCV
    def __init__(self, lien=None, filename=None, format=None, video_writer=None):
        self.out = None
        self.video_cap = None
        self.open = True
        self.device_index = 0  # 'https://192.168.43.77:8080/video'
        self.fps = 6  # fps should be the minimum constant rate at which the camera can
        self.fourcc = "MJPG"  # capture images (with no decrease in speed over time; testing is required)
        self.frameSize = (720, 480)
        if format:
            self.frameSize = format  # video formats and sizes also depend on and vary according to the camera used
        self.video_filename = "../../enregistrement/temp_video.avi"
        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
        if video_writer:
            self.video_writer = video_writer
        # self.video_writer = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.video_out = None # cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
        self.frame_counts = 1
        self.start_time = time.time()
    
    async def start(self):
        await asynckivy.sleep(0)
        self.video_cap = cv2.VideoCapture(self.device_index)

    async def demarage(self, lien=None, filename=None, cam=None):
        self.device_index = lien
        user_home = os.path.expanduser('~')
        downloads_folder = os.path.join(user_home, 'Downloads')
        self.video_filename = "CamLive/enregistrement/" + filename
        self.video_filename = os.path.join(downloads_folder, self.video_filename)
        await asynckivy.sleep(0)
        try:
            # process = MyProcess(target_function=self.start, args=())
            # # self.listProces.append(process)
            # process.run()
            if not cam:
                await self.start()
            else:
                 self.video_cap = cam
        except Exception as e:
            print(f"demarage=====>>>> {e}")
            self.video_cap = None
        # return self.video_cap

    async def record_demarage(self, frames_to_record):
        await asynckivy.sleep(0)
        if frames_to_record:
            self.frame_counts = 1
            self.start_time = time.time()
            height, width, layers = frames_to_record[0].shape
            size = (width, height)
            print(self.video_filename)
            self.out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, size)

    async def stop_record(self, frames_to_record):
        # Enregistrer la liste d'images en vidéo
        print("demare stop")
        if frames_to_record and self.out is not None:
            for i in range(len(frames_to_record)):
                await asynckivy.sleep(0)
                self.out.write(frames_to_record[i])
                self.frame_counts += 1
            self.out.release()
            print("stop")
            return []

    async def update_record(self, frames_to_record):
        if frames_to_record and self.out is not None:
            for i in range(len(frames_to_record)):
                await asynckivy.sleep(0)
                self.out.write(frames_to_record[i])
                self.frame_counts += 1
            print("update")
            return []

    def stop(self):
        try:
            if self.open:
                self.open = False
                self.video_cap.release()
                self.video_cap = None
        except Exception as e:
            self.video_cap = None
            print(e)
    
    def stop_video(self):
        self.video_cap = None
