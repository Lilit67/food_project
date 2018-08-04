import logging
import argparse

from varieties.bread import Bread
from management.chain_manager import ChainManager, RecipeTree

def parse_options():
    parser = argparse.ArgumentParser(description='Calculate recipe')
    parser.add_argument('-w', "--workbook",  metavar='filepath', type=str,
                        help='file path')
    parser.add_argument('--sheet',  metavar='sheet', type=str,
                        help='sheet name')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    return args

def set_logger():
    logname = '/tmp/assistant/logs/bread.log'

    logging.basicConfig(filename=logname, filemode='w')
    logger = logging.getLogger()
    fh = logging.FileHandler(logname)
    logger.addHandler(fh)
    return logger


def main():
    try:
        args = parse_options()
        logger = set_logger()

        logger.debug('Starting...')
        bread = Bread(args)

        exit(0)
        changed = bread.change_hydration(90, bread.recipe)
        changed = bread.change_hydration(50, changed)
        print(changed)
        bread.to_xl(changed)
        json_obj = bread.df_to_json(changed)
        #print(json_obj)
    except Exception as e:
        #print(e)
        import traceback
        traceback.print_exc()
        exit(-1)




if __name__ == '__main__':
    main()