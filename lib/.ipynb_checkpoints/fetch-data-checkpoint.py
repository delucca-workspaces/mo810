import os
import opendatasets as od

from pathlib import Path


def main():
    dataset_id = 'groffo/ads16-dataset'
    output_dir = f'{Path(__file__).resolve().parent.parent.absolute()}/data'
    has_data = os.path.isdir(output_dir) and os.listdir(output_dir)
    
    if not has_data:
        od.download('https://www.kaggle.com/datasets/groffo/ads16-dataset', data_dir=output_dir)
        print('🚀 Finished downloading dataset')
    else:
        print('Data already downloaded, skipping...')

if __name__ == '__main__':
    main()