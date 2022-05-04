# TEMPORAL-EMOTION-DETECTION

Following are comments on the directory structure and instructions on how to run the models for the files relevant to my course project for CGS702 at IIT Kanpur. Feel free to reach out to me at somyaloh@iitk.ac.in for any queries on the project. 

The RelevantPapers folder consists of the most important papers that have been crucial to the shaping of this project.

SomyaLohani_CGS702.pdf is the project report for this project.


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
  - cd into the 'TEST_DB' directory. To add the 700 new points, run: python gen_db.py
  - Now replace 'fer.csv' back into 'StaticDetection' folder.
  - Now to finally obtain the cross-validation accuracy repeat the steps to extract facial features, train the model, test the model, find the optimised hyperparameters and use them. 
 
5. For understanding and running the dynamic classifier cd into the 'TemporalDetection' folder
  - For Maximum Confidence implementation:
    - cd into 'MaximumConfidence' folder to implement the Maximum confidence algorithm.
    - The algorithm is integrated into the maxc_python_socket.py file.
    - Open the terminal of your UNIX system and cd to the current directory and run: python maxc_python_socket.py
    - Click on the file 'maxc_ generator.html' to open it in your browser 
    - The result of maximum confidencethe will now be displayed on the html webpage as well as on the terminal
    - Click on the stop button the webpage to stop the stream/ close your terminal.
  - For HMM implementation:
    - cd into 'HMM' folder to implement the HMM algorithm for detecting head nods.
    - The 'data(i).txt' files are the files which were generated for exploratory data analysis.
    - The 'plots' directory contains the important plots which were generated during the exploratory data analysis.
    - The 'trainnods' directory contains the dictionary data that corresponds to succesful nods.
    - The 'failednods' directory contains the dictionary data that corresponds to no nods.
    - The 'testnods' directory contains the curated test dataset. 
    - Install jupyter on your system. 
    - Open the terminal of your UNIX system and cd to the current directory and run: jupyter notebook
    - This opens a new page on your browser where you can view the .ipynb notebooks. The 'EDA.ipynb' file consists of the exploratory data analysis; the 'DB_GENERATION.ipynb' file consists of the process for database generation in terms of the creation of training and testing dataset; the 'FINAL_DETECTION.ipynb' file consists of the process for model development, model training and model testing.
    - The model is then integrated into the hmm_python_socket.py file.
    - Open the terminal of your UNIX system and cd to the current directory and run: python hmm_python_socket.py
    - Click on the file 'hmm_generator.html' to open it in your browser 
    - The result of the HMM model indicating whether a nod has occured or not and in between what time frames will now be displayed on the html webpage as well as on the terminal. 
    - Click on the stop button the webpage to stop the stream/ close your terminal.
