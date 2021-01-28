import numpy as np
import pandas as pd
import pickle as pkl
import matplotlib.pyplot as plt
from collections import defaultdict
import mat73
import os
import glob
# from tqdm import tqdm
import argparse
import logging
logging.basicConfig(filename='file-conversion.log', filemode='a',
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

# debugging
import pdb


def str2bool(v):
    """
    Helper function to deal with user input that may be boolean / somewhat boolean.
    :param v:
    :return:
    """
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(description='Perform alignment and decoding of either behaviour of stimulus '
                                             'from firing rate of neurons.')


parser.add_argument('--mat-folder',
                    metavar='mat_folder',
                    type=str, default=None,
                    help='Folder with mat files you want to convert to dataframes'
                         'for the spike viewer')


def mat_to_dict(data_dict, culture_file_name=None, culture_name=None, div=None):

    electrode_names = data_dict['channels']
    # TODO: need to convert this array to float
    # fs = data_dict['spikeDetectionResult']['params']['fs']
    fs = 25000
    recording_duration = data_dict['spikeDetectionResult']['params']['duration']
    spike_times = data_dict['spikeTimes']

    spike_dict = spike_times_to_spike_dict(spike_times=spike_times, electrode_names=electrode_names,
                                           recording_duration=recording_duration, culture_file_name=culture_file_name,
                                           culture_name=culture_name, div=div, fs=fs)

    return spike_dict


def spike_times_to_spike_dict(spike_times, electrode_names, culture_file_name, culture_name, div,
                              recording_duration, fs=25000, spike_detection_method='mea'):
    """
    spike_times : list of dictionary
        each item of the list correspond to an electrode
        within each item, the key of the dictionary gives the spike detection method
    """

    electrode_df_list = list()
    for n_electrode, electrode_name in enumerate(electrode_names):
        electrode_spike_time = spike_times[n_electrode][spike_detection_method] / fs

        if type(electrode_spike_time) is not np.ndarray:
            electrode_spike_time = np.array([electrode_spike_time])

        if electrode_spike_time.ndim != 1:
            electrode_spike_time = electrode_spike_time.flatten()
        # pdb.set_trace()
        try:
            electrode_df = pd.DataFrame.from_dict({'spikeTime': electrode_spike_time,
                                                   'electrode': np.repeat(electrode_name, len(electrode_spike_time))})
        except:
            pdb.set_trace()

        electrode_df_list.append(electrode_df)

    df = pd.concat(electrode_df_list)
    spike_dict = defaultdict(dict)
    spike_dict['df'] = df
    spike_dict['metadata']['Name'] = culture_file_name
    spike_dict['metadata']['fs'] = fs
    spike_dict['metadata']['num_channels'] = electrode_names.size
    spike_dict['metadata']['num_frames'] = recording_duration * fs
    spike_dict['metadata']['channel_id'] = electrode_names
    spike_dict['culture_name'] = culture_name
    spike_dict['DIV'] = div

    return spike_dict


def spike_matrix_to_spike_dict(spike_matrix, electrode_names, culture_file_name, culture_name, div,
                               fs=25000):

    electrode_df_list = list()
    for n_electrode, electrode_name in enumerate(electrode_names):
        electrode_spike_vec = spike_matrix[:, n_electrode]
        electrode_spike_time = np.where(electrode_spike_vec)[0] / fs
        electrode_df = pd.DataFrame.from_dict({'spikeTime': electrode_spike_time,
                                               'electrode': np.repeat(electrode_name, len(electrode_spike_time))})
        electrode_df_list.append(electrode_df)

    df = pd.concat(electrode_df_list)
    spike_dict = defaultdict(dict)
    spike_dict['df'] = df
    spike_dict['metadata']['Name'] = culture_file_name
    spike_dict['metadata']['fs'] = 25000.0
    spike_dict['metadata']['num_channels'] = electrode_names.size
    spike_dict['metadata']['num_frames'] = np.shape(spike_matrix)[0]
    spike_dict['metadata']['channel_id'] = electrode_names
    spike_dict['culture_name'] = culture_name
    spike_dict['DIV'] = div

    return spike_dict


def main():

    # Read user options
    args = parser.parse_args()
    mat_folder = args.mat_folder

    mat_files_to_convert = glob.glob(os.path.join(mat_folder, '*.mat'))

    save_folder = os.path.join(mat_folder, 'converted-files')
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    for mat_file_path in mat_files_to_convert:

        culture_file_name = os.path.basename(mat_file_path)
        culture_file_name_without_ext = os.path.splitext(culture_file_name)[0]
        culture_name = culture_file_name.split('DIV')[0][:-1]
        div = culture_file_name.split('DIV')[1][0:2]

        data_dict = mat73.loadmat(mat_file_path)
        spike_dict = mat_to_dict(data_dict, culture_file_name=culture_file_name, culture_name=culture_name,
                                 div=div)

        culture_dict = {culture_name: spike_dict,
                        'place_holder': spike_dict}

        save_name = culture_file_name_without_ext + '.pkl'
        with open(os.path.join(save_folder, save_name), 'wb') as handle:
            pkl.dump(culture_dict, handle)


if __name__ == '__main__':
    main()
