# -*- coding: utf-8 -*-
"""
juliet.py - Juliet Test Suite <https://samate.nist.gov/SRD/testsuite.php>

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import os
import re
import zipfile
from .utils import download_file
from .constants import DOWNLOAD_URL, JULIET_CATEGORY
from .models import Dataset
from covec.utils.processor import sysevr


class Juliet(Dataset):
    """Juliet Test Suite <https://samate.nist.gov/SRD/testsuite.php>

    Args:
        root <str>: Directory of dataset, will automately create Juliet_Test_Suite directory in it.
        download <bool, optional>: If true, download dataset from internet, default false.
        proxy <str>: The proxy for download.
            eg. 'http://user:pass@host:port/'
                'socks5://user:pass@host:port'

    """

    def __init__(self, datapath, download=False, proxy=None):
        datapath = os.path.expanduser(datapath)
        # Make sure directory path end with '/'
        if datapath[-1] != '/':
            datapath += '/'
        self._datapath = datapath + "Juliet_Test_Suite/"
        if not os.path.exists(self._datapath):
            os.makedirs(self._datapath)
        if download:
            self.download(proxy)

    def download(self, proxy):
        """Download Juliet Test Suiet from NIST website

        Directory Tree:
           <datapath>/Juliet_Test_Suite
                └── Raw
                    ├── C
                    └── Juliet_Test_Suite_v1.3_for_C_Cpp.zip

        Args:
            proxy <str>: proxy used for download.
                eg. 'http://user:pass@host:port/'
                    'socks5://user:pass@host:port'

        """
        url = DOWNLOAD_URL['juliet']
        raw_path = self._datapath + 'Raw/'
        print(f'Download from {url}')
        if not os.path.exists(raw_path):
            os.makedirs(raw_path)
        download_file(url, raw_path, proxy)
        print('Download success, Start extracting.')
        # Extract download zip file
        with zipfile.ZipFile(os.path.join(raw_path, os.listdir(raw_path)[0])) as z:
            z.extractall(raw_path)

    def process(self, methods=None, category=None):
        """Process dataset and create dataset

        Directory Tree:
            <datapath>/Juliet_Test_Suite
            TODO: w

        Args:
            method <None, list>: The process methods used on dataset
                - None, default: use all methods
                - 'sysevr': source from arXiv:1807.06756
            category <None, list>: The parts of Juliet Test Suite used on dataset
                - None, default: use all categoary
                - 'AE': Arithmetic Expression
                - 'AF': API Function Call
                - 'AU': Array Usage
                - 'PU': Pointer Usage

        """
        files = self._selected(category)
        if not methods:
            methods = ['sysevr', ]
        if 'sysevr' in methods:
            sysevr(files, 'sc')

    def _selected(self, category):
        """Selected file by category

        Args:
            category <None, list>: The parts of Juliet Test Suite used on dataset
            - None, default: use all categoary
            - 'AE': Arithmetic Expression
            - 'AF': API Function Call
            - 'AU': Array Usage
            - 'PU': Pointer Usage
        
        Return:
            file_list <list>: file path list selected by category
            
        """
        juliet_source_path = self._datapath + 'Raw/C/testcases/'
        # the range of selected CWE
        area = []
        if category:
            for i in category:
                area.extend(JULIET_CATEGORY[i])
            area = set(area)
        else:
            for v in JULIET_CATEGORY.values():
                area.extend(v)
            area = set(area)
        file_list = []
        # Extract file path from raw directory
        for root, _, _, in os.walk(juliet_source_path):
            # The file must in CWE directory and selected by area
            if str(re.search(r'CWE\d{2,3}', root).group()) in area:
                for r, _, files in os.walk(root):
                    for file in files:
                        if re.match(r'^CWE\d{3}.*.[c|cpp]$', file):
                            path = os.path.join(r, file)
                            file_list.append(path)
        return file_list