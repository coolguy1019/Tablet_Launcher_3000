import cv2
import mediapipe as mp
import time
import numpy as np
import csv

class FPS:
    def __init__(self):
        self.i = 0
        self.sumfr =0
        self.start = time.time()
    def get(self):
        curt = time.time()
        elapsed = curt - self.start
        self.start =  curt
        self.fr = int(1/elapsed) if elapsed > 0 else 0
        self.sumfr += self.fr
        self.i += 1
        return self.fr
    def getavgfr(self):
        avgfr = self.sumfr/self.i
        return avgfr


class CAMERA:
    def __init__(self,cam_no, brightness, width = 640, height = 480):
        self.cam_no = cam_no
        self.width = width
        self.height = height
        self.brightness = brightness
    def initiate(self):
        self.cap = cv2.VideoCapture(self.cam_no)
        self.cap.set(3, self.width)
        self.cap.set(4, self.height)
        self.cap.set(10, self.brightness)
    def startcam(self, invert = True):
        works, img = self.cap.read()
        if invert:
            img = cv2.flip(img,1)
            return works, img
        return works, img


class FACEDET:
    def __init__(self, max_faces = 1, det_con = 0.5, trac_con = 0.5, redefine = True):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False,
        max_num_faces= max_faces,
        refine_landmarks=redefine,
        min_detection_confidence=det_con,
        min_tracking_confidence=trac_con)

    def getpoints(self, img, lips = True, draw = False):

        #==========================================changing format to fit mediapipe
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)
        #==========================================

        if results.multi_face_landmarks:

            for self.face_landmarks in results.multi_face_landmarks:  # for each and every face in the image

                face_coord_list = []

                #===========================================================================================
                if draw:
                    self.mp_drawing.draw_landmarks(
                        img,
                        self.face_landmarks,
                        self.mp_face_mesh.FACEMESH_LIPS,
                        None,
                        self.mp_drawing_styles.get_default_face_mesh_tesselation_style()
                    )
                #===========================================================================================
                if lips:
                    lip_list_lmk = set()
                    lip_list_coord = []
                    for connection in self.mp_face_mesh.FACEMESH_LIPS:
                        lip_list_lmk.add(connection[0])
                        lip_list_lmk.add(connection[1])
                    for idx in lip_list_lmk:  # iterating over all points around the lips
                        lm = self.face_landmarks.landmark[idx]
                        x, y = int(lm.x * 640), int(lm.y * 480)
                        lip_list_coord.append((x, y))
                    return np.array(lip_list_coord)
                #===========================================================================================

                for idx in range(468):  # iterating over all points of the face
                    lm = self.face_landmarks.landmark[idx]
                    x, y = int(lm.x * 640), int(lm.y * 480)
                    face_coord_list.append((x, y))
                return np.array(face_coord_list)

    def getopenmouth_coord(self, img):
        list =[]

        for idx in (13,14,61,291):
            lm = self.face_landmarks.landmark[idx]
            x, y = int(lm.x * 640), int(lm.y * 480)
            list.append((x,y))
        #=======================================================to get the middle point in the mouth
        avg_x = int(sum(p[0] for p in list) / len(list))
        avg_y = int(sum(p[1] for p in list) / len(list))
        center_point = (avg_x, avg_y)

        return center_point


def normalise(array):
    #====================================================
    #making one point as origin by subtracting it from all
    #and then dividing by the largest value to get normalised features ready for training
    if array is not None:
        array = array - array[0]
        max_val = np.max(np.abs(array))

        if max_val != 0:
            array = array/max_val
        return 1,array.flatten()
    print("array is empty i.e is None")




def save_sample(id, features, clear = False):
    if clear:#to clear the dataset when needed
        with open("openmouth_dataset.csv", 'w') as f:
            pass
    else:
        with open("openmouth_dataset.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([id, *features])
            print(f"feature {id} saved")






def main():
    fps = FPS()
    #=========================================
    cam = CAMERA(1, 100)
    cam.initiate()
    #=========================================
    facedet = FACEDET(2)
    #===============================================================================

    #===============================================================================

    while True:
        fp = fps.get()
        #===========================================
        works, img = cam.startcam()
        if not works: break
        #========================================================================================================
        lip_points = facedet.getpoints(img,True, True)
        ret = 0
        if lip_points is not None:
            ret, lip_points_norm = normalise(lip_points)
            #print(lip_points_norm)
            for points in lip_points:
                cv2.circle(img, points, 1, (0,0,0), -1)
        #========================================================================================================

        #========================================================================================================
        #to save features in the dataset...
        key = cv2.waitKey(1)
        for i in range(10):
            if key == ord(str(i)) and ret == 1:
                save_sample(i, lip_points_norm)
        if key == ord('e'):
            save_sample(1, lip_points_norm, clear=True)
            print("all values erased...")
        if key & 0xff == ord('q') or key==ord('Q'): break
        #========================================================================================================






        #========================================================================================================
        #display the final output
        cv2.putText(img, str(fp), (20,40), cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        cv2.imshow("showtime", img)
        #========================================================================================================

    #releave the camera and destroy all windows
    print(fps.getavgfr())
    cam.cap.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':main()