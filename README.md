# TEMPORAL-EMOTION-DETECTION

INTRUCTIONS FOR RUNNING:

1. To be able to run the models on your machine, first download a copy of the repository to your machine using the 'Download ZIP' feature provided by Github. Unzip the file to start using.

2. For your convenience all the dependencies have been installed into the virtual environment. Install pip on your machine by using 'pip install virtualenv' if it is not installed already. Activate the virtual environment using 'source bin/activate' in the root directory.

4. For running the static classifier cd into the 'StaticDetection' folder.
  - Download Fer2013 dataset and the Face Landmarks models from https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data and http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2 since they could not be added to the github repository because of their size. 
  - Unzip the downloaded files and add them to the 'StaticDetection' directory.
  - To extract facial features use: python convert_fer2013_to_images_and_landmarks.py
  - To train the model use: python train.py --train=yes
  - To test the model use: python train.py --evaluate=yes
  - To find optimised hyperparameters use: python optimize_parameters.py --max_evals=15
  - The above found hyperparameters have to be changed in the 'parameters.py' file. Run the training and testing commands again to see improved accuracy.
  - Inorder to cross-validate you have to add the 700 dataset points from IIM database to the csv file. For that move the downloaded 'fer.csv' into the 'TEST_DB' directory. 
  - Next, download the 700 images from https://drive.google.com/file/d/1mMZUSqf_STR_FSPdPLFlQYH_YJj8bYgX/view?usp=sharing into the 'TEST_DB' directory.
  - Cd into the 'TEST_DB' directory. To add the 700 new points, run: python gen_db.py
  - Now replace 'fer.csv' back into 'StaticDetection' folder.
  - Now to finally obtain the cross-validation accuracy repeat the steps to extract facial features, train the model, test the model, find the optimised hyperparameters and use them. 
 
5. For understanding and running the dynamic classifier cd into the 'TemporalDetection' folder
