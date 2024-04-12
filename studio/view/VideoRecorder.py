import cv2
import time


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

    def demarage(self, lien, filename):
        self.device_index = lien
        self.video_filename = "enregistrement/" + filename
        try:
            
            self.video_cap = cv2.VideoCapture(self.device_index)
        except Exception as e:
            print(f"demarage=====>>>> {e}")
            self.video_cap = None
        # return self.video_cap

    def record_demarage(self, frames_to_record):
        if frames_to_record:
            self.frame_counts = 1
            self.start_time = time.time()
            height, width, layers = frames_to_record[0].shape
            size = (width, height)
            print(self.video_filename)
            self.out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, size)

    def stop_record(self, frames_to_record):
        # Enregistrer la liste d'images en vidéo
        print(" demare stop")
        if frames_to_record and self.out is not None:
            for i in range(len(frames_to_record)):
                self.out.write(frames_to_record[i])
                self.frame_counts += 1
            self.out.release()
            print("stop")
            return []

    def update_record(self, frames_to_record):
        if frames_to_record and self.out is not None:
            for i in range(len(frames_to_record)):
                self.out.write(frames_to_record[i])
                self.frame_counts += 1
            print("update")
            return []

    def stop(self):

        if self.open:
            self.open = False
            self.video_out.release()

        else:
            pass
    
    def stop_video(self):
        self.video_cap = None
