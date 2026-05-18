from math import sqrt
import main as mn
import cv2
import pickle



def cam_center(img,draw=True,color=(0,0,0), thickness = 1):
    width = 640
    height = 480
    if draw:
        cv2.line(img, (int(width/2),0),(int(width/2),height),color,thickness)
        cv2.line(img, (0, int(height/2)), (width, int(height/2)), color, thickness)
        return width/2, height/2
    return width/2, height/2


def centolipdist(center, lip, dis = False):
    del_x = abs(center[0] - lip[0])
    del_y = abs(center[1] - lip[1])
    dist = sqrt((del_x**2) + (del_y**2))
    if dis:
        return dist
    return del_x, del_y

def main():
    fps = mn.FPS()
    cam = mn.CAMERA(1,100)
    cam.initiate()
    model = pickle.load(open("openmouth_model.pkl","rb"))
    gesture_names = {
        0: "closed",
        1: "open"
    }

    lips_det = mn.FACEDET()

    while True:
        fp = fps.get()
        works, img = cam.startcam()
        if not works: break

        lip_points = lips_det.getpoints(img,True,True)


        if lip_points is not None:
            ret, lip_points_norm = mn.normalise(lip_points)
            predictions = model.predict(lip_points_norm.reshape(1,-1)) #need to reshape to 2d array because its a 1d array the output
            cv2.putText(img, gesture_names[predictions[0]], lip_points[0], cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
            avg_coord = lips_det.getopenmouth_coord(img)
            cv2.circle(img,avg_coord,3,(0,0,0),-1)

            c_x,c_y = cam_center(img)

            print(centolipdist((c_x,c_y),avg_coord))

        key = cv2.waitKey(1)

        cv2.putText(img, str(fp), (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)

        cv2.imshow("output", img)

        if key & 0xff == ord('q'): break

    #============================================
    #releaseing the camera and destroying all windows
    print(fps.getavgfr())
    cam.cap.release()
    cv2.destroyAllWindows()
    #============================================

if __name__ == '__main__': main()