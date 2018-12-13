import logging
import argparse
import json

from executables.bread import Bread
from management.chain_manager import ChainManager, RecipeTree

logger = logging.getLogger()

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

    #logging.basicConfig(filename=logname, filemode='w')
    # Display progress logs on stdout
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    fh = logging.FileHandler(logname)
    logger.addHandler(fh)
    print(logger)
    return logger


def main():
    try:
        args = parse_options()
        logger = set_logger()

        logger.debug('Starting...')
        bread = Bread(args)


        changed = bread.change_hydration(90, bread.original)
        logger.info('Changed hydration to 90 {}'.format(changed))
        changed1 = bread.change_hydration(50, changed)
        logger.info('Changed hydration to 50 {}'.format(changed1))
        json_obj = bread.df_to_json(changed1)

        #print(json_obj[0])
        #print(json.dumps(json_obj, indent=4))
        output_file = '/tmp/assistant/logs/recipe.json'#os.path.join(output_dir, bread.)
        with open(output_file, 'w') as f:
            json.dump(json_obj, f, indent=4)
        scaled = bread.scale_recipe(changed1, 3)
        logger.info('Scaled {} times {}'.format(scaled, 3))
        bread.save_xl()
        bread.df_to_csv('./output/recipe.csv')
    except Exception as e:

        import traceback
        traceback.print_exc()
        exit(-1)




if __name__ == '__main__':
    main()