# Smart-Attendance-using-Face-Recognition
Face Recognition using Open CV
#This a group project developed by V.Bhavana,M.Keerthana,Y.Bhavya Sri,Y.Sravani
Steps:
Initially,you will be having an empty StudentDetails.csv file. After each person's registration will be updated.
1.)Run the file finallog.py.
2.)You'll come across a GUI interface with a set of buttons and attributes.Follow the below procedure now.
3.)Give your details like ID,Name as mentioned in the interface.
4.)Click on Take Images now so that webcam will be opened and will take a snap of 60 images all at a time.These images will be stored in TrainingImages folder(dataset).The more the input samples,the higher the accuracy will be.
5.)After this step you will be notified "Images saved" and these details will be uploaded in StudentDetails file,which we refer to as registration file.This is the crucial phase.Make sure that only you occupy the frame while storing your images in the dataset.
6.)The next step is to train these images. For that purpose ,click on train images button.After training all the images in TrainingImage folder,a message stating "Images Trained" will be displayed on the status bar.
7.)After this step,a Trainner.yml file will be created in the TrainingImageLabel folder.
8.)Now,click on Detect Images button.
9.)Now,webcam will be active and recognizes you comparing your face with those in the TrainingImages folder.It will display your name as well as your ID.
10.)Now,in the Attendance folder,a new file with that particular day's date will be created with your particulars, ID,Name,Date,Time,Present status.
11.)This file will be automatically mailed to concerned officials thus reducing manual work.
-This can track a group of people all at a time,create a csv file and mail it to the required.
