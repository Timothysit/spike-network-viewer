# Spike Network Viewer

 [![Launch app online](https://img.shields.io/badge/Launch%20online-app-brightgreen.svg?style=flat)](https://spike-network-viewer.herokuapp.com/spike-network-viewer)
 

This is a (work in progress) dashboard for visualising the network properties of neural activity from spikes. 
Note that currently the spatial structure of the network is assumed to be that of the [MultiChannels 60MEA system (8 x 8 layout)](https://www.multichannelsystems.com/products/meas-60-electrodes)


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


## Contributing 

Feel free to post issues if you have trouble running the app or have feature suggestions!
