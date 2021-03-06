import numpy as np
import pandas as pd

class Stack():
    def __init__(self, name, data, sigma=None, mu=None):
        self.name = name
        self.data = data
        self.sigma = sigma
        self.mu = mu

    def get_idx(self):
        pass


def read_data(filenames, mode):
    """
    The main function to read all the back calculated files

    Parameters
    ----------
    filenames: dict
        This parameter is a dictionary of properties with their relative path to the data file.

    mode: str
        This parameter must be one of the following:
            - 'exp': experimental data
            - 'trades': back calculated data for TRADES pool
            - 'trades_uf': back calculated data for TRADES pool only including unfolded structures
            - 'mixed': back calculated data for MIXED pool
            - 'ensemble': back calculated data for ENSEMBLE pool

    Returns
    -------
    dict: A dictionary of properties with their pandas data frame

    """
    if mode == 'exp':
        pre = pd.read_csv(filenames['pre'])
        pre.drop(21, axis=0, inplace=True)  # high-error outlier
        # print(pre.head(25))

        saxs = pd.read_csv(filenames['saxs'])
        saxs.error = saxs.error * 0.1

        return {
            # property name: Stack(name, exp data, sigma, mu)
            'rh'  : Stack('rh', 20.3, 0.3, None),
            'rdc' : Stack('rdc', pd.read_csv(filenames['rdc']), None, None),
            'pre' : Stack('pre', pre, None, None),
            'noe' : Stack('noe', pd.read_csv(filenames['noe']), None, None),
            'jc'  : Stack('jc', pd.read_csv(filenames['jc']), None, None),
            'fret': Stack('fret', 0.55, 0.02, None),
            'cs'  : Stack('cs', pd.read_csv(filenames['cs']), None, None),
            'saxs': Stack('saxs', saxs, None, None)
        }

    elif mode in  ['mixed', 'ensemble']:
        pre_data = pd.read_csv(filenames['pre'], header=None, delim_whitespace=True, index_col=0)   # shape: None, 68
        pre_data.index = range(pre_data.shape[0]) # just wanted to keep the indices 0-indexed
        pre_data.drop(22, axis=1, inplace=True)  # remove index 21, column 22 (due to high upper bound error: outlier)
        # print(pre_data.describe().iloc[:,18:25], pre_data.columns)

        noe_data = pd.read_csv(filenames['noe'], header=None, delim_whitespace=True, index_col=0)   # shape: None, 93
        noe_data.index = range(noe_data.shape[0]) # just wanted to keep the indices 0-indexed

        jc_data = pd.read_csv(filenames['jc'], header=None, delim_whitespace=True, index_col=0)   # shape: None, 47
        jc_data.index = range(noe_data.shape[0]) # just wanted to keep the indices 0-indexed

        fret_data = pd.read_csv(filenames['fret'], header=None, delim_whitespace=True, index_col=0)   # shape: None, 1
        fret_data.index = range(noe_data.shape[0]) # just wanted to keep the indices 0-indexed
        # fret_data = (1.0 / (1.0 + (1.05862 * fret_data / 44.0) ** 6.0))
        if mode == 'mixed':
            fret_data.iloc[1700:] = (1.0 / (1.0 + (1.05862 * fret_data.iloc[1700:] / 44.0) ** 6.0))

        saxs_data = pd.read_csv(filenames['saxs'], header=None, delim_whitespace=True, index_col=0)   # shape: None, 37
        saxs_data.index = range(noe_data.shape[0]) # just wanted to keep the indices 0-indexed

        return {
            # property name: Stack(name, back calc data, sigma, mu)
            'rh': Stack('rh', pd.read_csv(filenames['rh'], header=None),  # shape: None, 1
                        0.812, None),
            'rdc': Stack('rdc',
                         pd.read_csv(filenames['rdc'], header=None, delim_whitespace=True, index_col=0), # shape: None, 28
                         0.88, None),
            'pre': Stack('pre', pre_data, 0.0001, None),
            'noe': Stack('noe', noe_data, 0.0001, None),
            'jc': Stack('jc', jc_data,
                        {'A': np.sqrt(0.14), 'B': np.sqrt(0.03), 'C':np.sqrt(0.08)},
                        {'A': 6.51, 'B': -1.76, 'C': 1.6}),
            'fret': Stack('fret', fret_data, 0.0074, None),
            'cs': Stack('cs', pd.read_csv(filenames['cs'], header=None, delim_whitespace=True, index_col=0),  #shape: None, 262
                        # {'C': 0.533, 'CA': 0.4412, 'CB': 0.5163, 'H': 0.1711, 'HA': 0.1231},
                        {'C': 1.21, 'CA': 1.16, 'CB': 1.43, 'H': 0.52, 'HA': 0.29},  # LH-Test from Li et al
                        None),
            'saxs': Stack('saxs', saxs_data, 0.00055, None)
        }

    elif mode == 'trades_uf':
        pre_data = pd.read_csv(filenames['pre'], header=None, delim_whitespace=True, index_col=0)   # shape: None, 68
        pre_data.index = range(pre_data.shape[0]) # just wanted to keep the indices 0-indexed
        pre_data.drop(22, axis=1, inplace=True)  # remove index 21, column 22 (due to high upper bound error: outlier)
        # print(pre_data.describe().iloc[:,18:25], pre_data.columns)

        noe_data = pd.read_csv(filenames['noe'], header=None, delim_whitespace=True, index_col=0)   # shape: None, 93
        noe_data.index = range(noe_data.shape[0]) # just wanted to keep the indices 0-indexed

        jc_data = pd.read_csv(filenames['jc'], header=None, delim_whitespace=True, index_col=0)   # shape: None, 47
        jc_data.index = range(noe_data.shape[0]) # just wanted to keep the indices 0-indexed

        fret_data = pd.read_csv(filenames['fret'], header=None, delim_whitespace=True, index_col=0)   # shape: None, 1
        fret_data.index = range(noe_data.shape[0]) # just wanted to keep the indices 0-indexed
        fret_data = (1.0 / (1.0 + (1.05862 * fret_data / 44.0) ** 6.0))

        saxs_data = pd.read_csv(filenames['saxs'], header=None, delim_whitespace=True, index_col=0)   # shape: None, 37
        saxs_data.index = range(noe_data.shape[0]) # just wanted to keep the indices 0-indexed

        return {
            # property name: Stack(name, back calc data, sigma, mu)
            'rh': Stack('rh', pd.read_csv(filenames['rh'], header=None).iloc[100:, :],  # shape: None, 1
                        0.812, None),
            'rdc': Stack('rdc',
                         pd.read_csv(filenames['rdc'], header=None, delim_whitespace=True, index_col=0).iloc[100:, :], # shape: None, 28
                         0.88, None),
            'pre': Stack('pre', pre_data.iloc[100:, :], 0.0001, None),
            'noe': Stack('noe', noe_data.iloc[100:, :], 0.0001, None),
            'jc': Stack('jc', jc_data.iloc[100:, :],
                        {'A': np.sqrt(0.14), 'B': np.sqrt(0.03), 'C':np.sqrt(0.08)},
                        {'A': 6.51, 'B': -1.76, 'C': 1.6}),
            'fret': Stack('fret', fret_data.iloc[100:, :], 0.0074, None),
            'cs': Stack('cs', pd.read_csv(filenames['cs'], header=None, delim_whitespace=True, index_col=0).iloc[100:, :],  #shape: None, 262
                        # {'C': 0.533, 'CA': 0.4412, 'CB': 0.5163, 'H': 0.1711, 'HA': 0.1231},
                        {'C': 1.21, 'CA': 1.16, 'CB': 1.43, 'H': 0.52, 'HA': 0.29},   # LH-Test from Li et al
                        None),
            'saxs': Stack('saxs', saxs_data.iloc[100:, :], 0.00055, None)
        }