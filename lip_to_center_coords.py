from math import sqrt
import face_landmarks as mn
import cv2
import pickle
import Serial_communication as sc





def cam_center(img,width,height,draw=True,color=(0,0,0), thickness = 1):#draws crosshairs on the image
    if draw:
        cv2.line(img, (int(width/2),0),(int(width/2),height),color,thickness)
        cv2.line(img, (0, int(height/2)), (width, int(height/2)), color, thickness)
        return width/2, height/2
    return width/2, height/2


def centolipdist(center, lip, dis = False):
    del_x = -(center[0] - lip[0]) #to make it according to the cartesian system.. forgot to update before.
    del_y = (center[1] - lip[1])
    dist = sqrt((del_x**2) + (del_y**2))
    if dis:
        return dist
    return int(del_x), int(del_y)

def main():
    fps = mn.FPS()
    #=======================
    serial = sc.COMMUNICATION(115200,2,'COM15',1)
    #=======================
    cam = mn.CAMERA(1,100)
    cam.initiate()
    #=======================


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
            #==================================================================================================================================
            cv2.putText(img, gesture_names[predictions[0]], lip_points[0], cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
            #==================================================================================================================================
            mouth_coord = lips_det.getopenmouth_coord(img) #coord of openmouth wrt to the origin

            cv2.circle(img,mouth_coord,3,(0,0,0),-1)
            #==================================================================================================================================
            c_x,c_y = cam_center(img,cam.width,cam.height) #draws crosshairs and returns centerpoint coords of the camera
            l_x,l_y=centolipdist((c_x,c_y),mouth_coord)# return the coords of openmouth from the center cross
            #==================================================================================================================================

            serial.serialOutput(l_x,l_y,0.01)#serial output to arduino via uart
            print(serial.serialInput())
        #==================================================================================================================================

        key = cv2.waitKey(1)
        cv2.putText(img, str(fp), (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
        cv2.imshow("output", img)


        #=====================================to stop the program
        if key & 0xff == ord('q'): break
        #=====================================

    #============================================
    #releaseing the camera and destroying all windows
    print(fps.getavgfr())
    cam.cap.release()
    cv2.destroyAllWindows()
    #============================================

if __name__ == '__main__': main()