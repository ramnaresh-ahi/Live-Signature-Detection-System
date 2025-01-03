import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk
import os
import os.path
import pickle


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x500+350+100")
        
        self.detect_button_main_window = util.get_button(self.main_window, 'Detect', 'green', self.detect)
        self.detect_button_main_window.place(x = 700, y = 300)
        
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register new user', 'gray',
                                                                    self.register_new_user, fg = 'black')
        self.register_new_user_button_main_window.place(x = 700, y = 400)
        
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x = 10, y = 0, width = 700, height = 500)
        
        self.add_webcam(self.webcam_label)
        
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
       
        
    def add_webcam(self, label):
        
          if 'cap' not in self.__dict__:
              self.cap = cv2.VideoCapture(0)
              
          self._label =  label
          self.process_webcam()   
           
                
    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame
        
        gray_img = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2GRAY)
        
        self.most_recent_capture_pil = Image.fromarray(gray_img)
        
        imgtk = ImageTk.PhotoImage(image = self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image = imgtk)
        
        self._label.after(20,self.process_webcam)
             
                
    def detect(self):
        result, name = util.recognize(self.most_recent_capture_arr, self.db_dir)

        if result == 'valid' and name:
            util.msg_box('Valid', f"Signature is valid. It's {name}'s signature!")
        else:
            util.msg_box('Invalid', 'Signature is invalid. Please try again or register.')


    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")
        
        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green',
                                                                    self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x = 750, y = 300)
        
        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try Again', 'red',
                                                                    self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x = 750, y = 400)
        
        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x = 10, y = 0, width=700, height=500)
        
        self.add_img_to_label(self.capture_label)
        
        
    def add_img_to_label(self,label):
        imgtk = ImageTk.PhotoImage(image = self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image = imgtk)
        
        self.register_new_user_capture = self.most_recent_capture_arr.copy()
        
        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x = 750, y = 150)
        
        self.entry_text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, Enter \nYour Name:')
        self.entry_text_label_register_new_user.place(x = 750, y = 80)
            
            
    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()
    
    
    def Start(self):
        self.main_window.mainloop()
        
        
    def accept_register_new_user(self):
        orb = cv2.ORB_create()
        name = self.entry_text_register_new_user.get(1.0, "end-1c").strip()

        _, descriptors = orb.detectAndCompute(self.register_new_user_capture, None)

        if descriptors is not None:
            print(f"Saving descriptors for {name}: {descriptors.shape}")  

            with open(os.path.join(self.db_dir, f'{name}.pickle'), 'wb') as file:
                pickle.dump(descriptors, file)
            util.msg_box('Success!', 'User was registered successfully!')
        else:
            util.msg_box('Error', 'No features found in the signature. Please try again.')

        self.register_new_user_window.destroy()


if __name__ == '__main__':
    app = App()
    app.Start()
    
    
   