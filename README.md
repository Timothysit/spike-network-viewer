# Spike Network Viewer

 [![Launch app online](https://img.shields.io/badge/Launch%20online-app-brightgreen.svg?style=flat)](https://spike-network-viewer.herokuapp.com/spike-network-viewer)
 

This is a (work in progress) dashboard for visualising the network properties of neural activity from spikes. 
Note that currently the spatial structure of the network is assumed to be that of the [MultiChannels 60MEA system (8 x 8 layout)](https://www.multichannelsystems.com/products/meas-60-electrodes)

## Installation Instructions 

### Step 1: Clone the repository

 - option A: (go to a suitable direcotry, such as home), and run `git clone https://github.com/Timothysit/spike-network-viewer` 
 - option B: click on the green `Code` button, then do `Download ZIP`, then unpack the contents

### Step 2: Set up python environment 

1. If you use anaconda, change to the folder containing the repository contents (`cd spike-network-viewer`) and create a new environment using `conda env create --name spike-network-viewer --file=spike-network-viewer.yml`
   - feel free to replace 'spike-network-viewer' with your preferred name of the environment
2. Install the required packages by running: `pip install -r requirements.txt`

   

### Step 3: Run command line argument to launch viewer 

1. Change to the directory containing the cloned repoistory, eg. `cd spike-network-viewer`, then do: 
2. Activate your python environment, eg. `conda activate spike-network-viewer` if you use anaconda as your python package manager 
3. Launch the viewer: `panel serve --show spike-network-viewer.ipynb`




## File format requirements

The current supported file format is limited to: 

 - pickle files: `.pkl` 


An example file can be found in the `example-files` folder. 

### Pickle file structure 

For pickle files, the content should be a dictionary with the following structure: 

 - `metadata`: a dictionary with:
   - `Name`: name of the file (optional)
   - `num_channels`: number of channels in the recording (int)
   - `num_frames`: number of frames in the recording per channel (int)
   - `fs`: sampling rate (float) 
   - `channel_id`: numpy array containing the names of the channels 
 - `df`: pandas dataframe with two columns:
   - `spikeTime`: time of spike (s)
   - `electrode`: electrode id (int or float)


## Modifying the viewer

The viewer is contained in the file `spike-network-viewer.ipynb`, which can be opened using:

 1. jupyter notebook, in which case run: `python -m jupyter notebook` 
 2. jupyter lab, in which case run: `python -m jupyter lab`
 
then open the notebook, which allows you modify the behaviour or add/subtract functionalities to the viewer.


## Contributing 

Feel free to post issues if you have trouble running the app or have feature suggestions!
