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


def centerToLipCoords(center, lip):
    del_x = -(center[0] - lip[0]) #to make it according to the cartesian system.. forgot to update before.
    del_y = (center[1] - lip[1])
    return int(del_x), int(del_y)

def errorToSteps(x_error, y_error):
    x_veiwing_angle = 81.14 #viewing angles of camera
    y_veiwing_angle = 45.61
    degreesperpixel_x = x_veiwing_angle / 640 #resolution of camera
    degreesperpixel_y = y_veiwing_angle / 480
    degreeperstep = 360 / 800 #quater microstepping..(200*4)

    x_step = int((x_error * degreesperpixel_x) / degreeperstep)
    y_step = int((y_error * degreesperpixel_y) / degreeperstep)
    return x_step, y_step

#=====================================================================================
#defined outside since they need to remember.
x_prevError =0#error one frame ago
y_prevError =0
x_integral  =0
y_integral  =0
x_errorFiltered =0
y_errorFiltered =0
def PID(x_error, y_error,kp,kd,ki,fps):
    global x_prevError
    global y_prevError
    global x_integral
    global y_integral
    global x_errorFiltered
    global y_errorFiltered

    #==============================================
    #only take integral when the error small but if error is too small then ignore.
    if(abs(x_error)<50 and abs(x_error)>=10):
        x_integral += x_error
    elif(abs(x_error) <10):
        x_integral =0
    if(abs(y_error)<50 and abs(y_error)>=10):
        y_integral += y_error
    elif(abs(y_error) <10):
        y_integral =0
    #====================================================
    #for derivative term the time between 2 frames.
    dt = max(fps.elapsed,0.005)
    #exponenetial moving average for smoothening.
    a = 0.05
    x_errorFiltered = x_errorFiltered*a + x_error*(1-a)
    y_errorFiltered = y_errorFiltered*a + y_error*(1-a)
    x_derivative = float(x_error - x_prevError)/dt
    y_derivative = float(y_error - y_prevError)/dt
    #====================================================
    x_prevError = x_error
    y_prevError = y_error

    x_output = x_error*kp + x_derivative*kd + x_integral*ki  #PID output
    y_output = y_error*kp + y_derivative*kd + y_integral*ki

    return x_output,y_output


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
        works, img = cam.startcam(rotate=False)
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
            x_error,y_error = centerToLipCoords((c_x,c_y),mouth_coord)# return the coords of openmouth from the center cross
            x_corrected_error,y_corrected_error = PID(x_error,y_error,0.5,0.015,0,fps)
            x_step,y_step = errorToSteps(x_corrected_error,y_corrected_error)
            print(x_step,y_step,"   ",x_error,y_error)
            #==================================================================================================================================

            serial.serialOutput(x_step,y_step,predictions[0],0.01)#serial output to arduino via uart
            #print(serial.serialInput())
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



