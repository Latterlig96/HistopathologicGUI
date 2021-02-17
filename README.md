# histopathologic-cancer-detection

This repository focus on [Kaggle competition in histopathologic cancer detection](https://www.kaggle.com/c/histopathologic-cancer-detection).

## Data

[Setup the data sructure](data/README.md)

## Environment
Best practice is to create a [virtual environment](https://docs.python.org/3/tutorial/venv.html)  
To create python env:
 
    python3 -m venv cancer-env
    source cancer-env/bin/activate
This will open a shell in virtual env


## Dependencies
 Make sure you are running python 3.7  
 Install all deps by:
	
	 pip3 install -r requirements.txt

  If you encounter problem with installing Tensorflow 2.1, upgrade pip:
  
     pip3 install -U pip
  	 

## Jupyter
  To use notebook with enviroment:
  
    ipython3 kernel  install --user --name=cancer

  Next launch jupyter:

    jupter-notebook
  
  Kernel -> Change kernel -> cancer 

## Contributing
Please work on separate branches for each feature (eg. data visualization, data reprocessing, model, GPU optimized model), this will allow us to work on more stuff at once.
