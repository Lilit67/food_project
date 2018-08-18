
import os
import sys
import json
import math
import logging
from nutrient.foodinfo import Nutrient
from nutrient.ingredients import usda_group_item_map, non_usda


class UsdaReader:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.nu = Nutrient()
        self.cache_root = '/tmp/assistant/cache'
        if not os.path.isdir(self.cache_root):
            os.makedirs(self.cache_root)


    def get_usda_code(self, usda_item):
        """
        Get the USDA code
        First get the
        exact product, then get the
        code
        :param name:
        :return:
        """
        code = None
        group = usda_group_item_map
        product_list = self.nu.searchFor(usda_item).get('list')
        items = []
        if product_list:
            items = product_list.get('item')


        self._logger.info('*****')
        self._logger.info('Found {} records for name '
              '"{}"'.format(len(items), usda_item))
        self._logger.info('*****')
        if len(items) >= 3:
            self._logger.info(items[:3])
        if items:
            product = items[0]
            name = items[0]['name']
            if name:
                return product.get("ndbno")

        return None

    def get_usda_group(self, item_name):
        for key, val in usda_group_item_map.items():
            if item_name in val:
                return key

    def load_cache(self, cache_path):
        self._logger.info('Loading from cache {}'.format(cache_path))
        with open(cache_path, 'r') as fp:
            info = json.load(fp)
            return info

    def pretty_print(self, item):
        print(json.dumps(item, indent=4))


    def adjusted_item_name(self, item_name):
        item_name = item_name.replace('/', '-')
        item_name = item_name.replace(' ', '_')
        return item_name

    def cache_path(self, item_name):
        item_name = self.adjusted_item_name(item_name)
        return os.path.join(self.cache_root, str(item_name) + '.json')

    def get_product_info(self, item_name):
        """
        :param usda_item:
        :return:

        # curl -H "Content-Type: appliction/json" -d '{"q":"butter","max":"25","offset":"0"}' DEMO_KEY@api.nal.usda.gov/ndb/search
        # curl -H "Content-Type: application/json" -d '{"q":"milk","ax":"25","offset":"0", "fg": "Dairy and Egg Products"}' DEMO_KEY@api.nal.usda.gov/ndb/search

        Get the USDA db code
        :param name:
        :return:
        """

        if not isinstance(item_name, str): #math.isnan(float(item_name)):
            print('Item name should be a non empty string')
            return None
        item_group = self.get_usda_group(item_name)
        cache_path = self.cache_path(item_name)
        if os.path.isfile(cache_path):
            product_list = self.load_cache(cache_path)
        else:
            product_list = self.nu.searchForFlour(item_name, fg=item_group, ds="SR")
            cache_path = self.cache_path(item_name)

            with open(cache_path, 'w') as fp:
                json.dump(product_list, fp, indent=4)

        product_list = product_list.get('list', [])
        closest = self.closest_match(product_list, item_name)
        return closest

    def closest_match(self, product_list, item_name):
        """
        TODO: intelligently find the closest match
        :param product_list:
        :return:
        """
        items = []
        if product_list:
            items = product_list.get('item')
        self._logger.info('*****')
        self._logger.info('Found {} records for name '
              '"{}"'.format(len(items), item_name))
        self._logger.info('*****')
        #if len(items) >= 3:
        #    print(items[:3])
        if items:
            product = items[0]
            name = product['name']
            if name:
                return product
        return None

