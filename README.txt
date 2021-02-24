DESCRIPTION
This package contains the final report, poster in DOC folder, and a web application under CODE/Map-Visualization. The application achieves visualization for the accident information across the U.S. and prediction for the accident handling time based on time, location, weather and road conditions. 
The rpart regression tree model script is also included under CODE/Model with the final modeling dataset in this package. (The script will generate two outcome files: 1. the best tree model rules and 2. prediction vs actual values). Please follow the instructions inside each script to run and test data manipulation and data modeling if interested in.
To test the web application, please follow the instruction below to set up the environment and install Flask. Any combination of user inputs is acceptable for the web tool, but to get different prediction results, here are some examples provided:
Date: 3/1/2020, Temperature: 30, Junction: Yes, Zip code: 29009
Date: 5/1/2020, Temperature: 50, Junction: No, Zip code: 21014
Date: 2/5/2020, Temperature: 90, Junction: Yes, Zip code: 94303

INSTALLATION
I. Prerequisite.
 Python 3. Please download and install it from: https://www.python.org/downloads/

II. Setup the environment and install Flask.
Create a virtual environment.
Create a 'venv' folder within the 'Map-Visualization' folder:
	$ cd Map-Visualization
	$ python3 -m venv venv

	On Windows:
	> cd Map-Visualization
	> py -3 -m venv venv 
	OR:
    	> python -m venv venv

Activate the environment.
	$ . venv/bin/activate

	On Windows:
	> venv\Scripts\activate

Install Flask.
	$ pip install Flask

	On Windows:
	> pip install Flask

EXECUTION
Run the application using the following commands under the root folder 'Map-Visualization':
	$ export FLASK_APP=mapdata.py
	$ flask run
	
	On Windows:
	> set FLASK_APP=mapdata.py
	> flask run
	
Wait several seconds until following information shown up:
 	* Running on http://127.0.0.1:5000/
 
Now the application is running on the localhost, and please head over to http://127.0.0.1:5000/ and check the application UI (Please use FireFox or Chrome for the best performance. It may run into issues if Safari or IE is used).
