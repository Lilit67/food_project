""" USDA FOOD DATABASE INTERFACE """

import json
import requests
import logging
import os
from optparse import OptionParser

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(funcName)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



db_url = 'http://api.nal.usda.gov/ndb/'
nutrients_url  = db_url + 'nutrients/'
list_url       = db_url + 'list/'
search_url     = db_url + 'search/'
report_url     = db_url + 'reports/'

demo_key       = 'DEMO_KEY'

class Nutrient(object):
    """
    use information and api from
    usda food database 
    https://ndb.nal.usda.gov/ndb/doc/apilist/API-NUTRIENT-REPORT.md
    USES DEMO KEY

    """

    def __init__(self):
        self.logdir = 'saved_searches'
        if not os.path.isdir(self.logdir):
            os.mkdir(self.logdir)


    def foodList(self, start=0, end=50):
        '''
        NOT USED
        just for test
        '''    
        url = list_url
        
        payload = {
        'format': 'json', 
        'lt': 'f',
        'sort': 'n',
        'api_key': demo_key,
        'start': start,
        'end': end,
        'total': end - start 
        }

        r = requests.get(url, payload)
        if r.ok:
           l = json.loads(r.text)
           print(l.viewkeys())
           return l

    def cheddarInfo(self):

        '''
        USE FOR TEST

        '''
        r = requests.get('http://api.nal.usda.gov/ndb/nutrients/?format=json&api_key=DEMO_KEY&nutrients=205&nutrients=204&nutrients=208&nutrients=269&ndbno=01009')
        self.record('saved_cheddar.json') 

    
    def head(self, url):
        r = requests.head(url)
        if r.ok:
            return r.text       



    def getFrom(self, url, payload = None):

        r = requests.get(url, timeout = 0.1) 
        result = None
        try:
            if r.ok:           
                result = r.json()
              
        except Exception as data:
            
            logger.error(data)             
        finally:
            return result    



    def nutrientInfo(self, ndbcode):
        '''
        Browser: http://api.nal.usda.gov/ndb/nutrients/?format=json&api_key=DEMO_KEY&nutrients=205&nutrients=204&nutrients=208&nutrients=269
        CURL: curl -H "Content-Type:application/json" -d '{"nutrients":["204","205","208","269"],"max":25,"offset":0}' DEMO_KEY@api.nal.usda.gov/ndb/nutrients
        
        For food groups Dairy and Egg Products (id = 0100) and Poultry Products (id=0500):
        Browser: http://api.nal.usda.gov/ndb/nutrients/?format=json&api_key=DEMO_KEY&nutrients=205&nutrients=204&nutrients=208&nutrients=269&fg=0100&fg=0500
        CURL: curl -H "Content-Type:application/json" -d '{"nutrients":["204","205","208","269"],"fg":["0100","0500"],"max":25,"offset":0}' DEMO_KEY@api.nal.usda.gov/ndb/nutrients

        For chedder cheese (ndbno 01009) only:
        Browser: http://api.nal.usda.gov/ndb/nutrients/?format=json&api_key=DEMO_KEY&nutrients=205&nutrients=204&nutrients=208&nutrients=269&ndbno=01009
        CURL: curl -H "Content-Type:application/json" -d '{"nutrients":["204","205","208","269"],"ndbno":"01009","max":25,"offset":0}' DEMO_KEY@api.nal.usda.gov/ndb/nutrients

        '''

        r = requests.get('http://api.nal.usda.gov/ndb/nutrients/?format=json&api_key=DEMO_KEY&nutrients=205&nutrients=204&nutrients=208&nutrients=269&fg=0100&fg=0500') 
        if r.ok: 
            logger.debug(r.text)           
            return r.json()

    
    def food_nutrient(self, ndbcode):
        ''' nutrients for code '''
        payload = {
        'format': 'json',
        'api_key': demo_key,
        'ndbno': ndbcode,
        'nutrients': 205,
        'nutrients': 204,
        'nutrients': 208,
        'nutrients': 269  }
        r = requests.get(nutrients_url,  payload)
        if r.ok:
            logger.debug(r.json())
            with open('saved_searches/nutrientInfo2.json', 'w') as f:

                json.dump(result.json(), f, indent = 4)
            return r.json()

               
    def food_report(self, ndbno):
        ''' nutrients for code '''
        payload = {
        'format': 'json',
        'api_key': demo_key,
        'ndbno': ndbno,
        'type': 'b'
        }
 
        r = requests.get('http://api.nal.usda.gov/ndb/reports/?ndbno=01009&type=b&format=json&api_key=DEMO_KEY')
        #r = requests.get(report_url, payload)
        print(dir(r))
        if r.ok:
            logger.debug(r.json())
            with open('saved_searches/food_report.json', 'w') as f:

                json.dump(r.json(), f, indent = 4)
            return r.json()
        else:
            logger.debug(r.reason) 
            #pass   


    def lists(self, list_type='f'):
        '''
        handy to get list of
        database items
        '''
        if list_type not in ['f','g','n','ns','nr']:
            logging.error("lt entry of the payload can " + \
                " be one of ['f','g','n','ns','nr'] ")
            return None
        result = []
        url = list_url
        
        payload = {
        'format': 'json', 
        'lt': list_type,
        'sort': 'n',
        'api_key': demo_key
        
        } 
        r = requests.get(list_url, payload)
        if r.ok:
            j_obj = r.json()
            items = j_obj[u'list'][u'item']
            for i in items:      	
                if i[u'id'] not in result:
                    result.append(i[u'name'])
        logger.debug(result)

        with open(list_type + '_query.json', 'w') as f:
            json.dump(result, f, indent=4)             
        return result





    def searchFor(self, keyword, fg=None, mx=None, ds="SR"):
        '''
        Examble:
        http://api.nal.usda.gov/ndb/search/
        ?format=json&q=butter&sort=n&max=25
        &offset=0&api_key=DEMO_KEY 
        '''
        payload = {
        'format': 'json',
        'q': keyword,
        'sort': 'r',
        "fg": fg,
        'offset': 0,
        "DS": ds,
        'api_key': 'DEMO_KEY'

        }
        result = {}
        r = requests.get(search_url, payload)

        logger.debug(r.headers)
        if r.ok:
            f = os.path.abspath('saved_searches/serch_for_'+keyword+'.json')
            result = r.json()
        else:

            logging.error('Could not find ' + keyword)
            logging.error('Error is: ' + str(r.reason))
        return result


    def searchForFlour(self, keyword, fg="Cereal Grains and Pasta", mx=None, ds="SR"):
        '''
        Examble:
        http://api.nal.usda.gov/ndb/search/
        ?format=json&q=butter&sort=n&max=25
        &offset=0&api_key=DEMO_KEY
        '''

        payload = {
        'format': 'json',
        'q': keyword,
        'sort': 'r',
        "fg": fg,
        'offset': 0,
        'api_key': 'DEMO_KEY',
        "DS": "SR"

        }
        result = {}
        r = requests.get(search_url, payload)
        #test = open('debug.out', 'r')
        #r = json.load(test)
        #print r
        #json.dump(r.json(), 'debug.out', indent = 4)
        logger.debug(r.headers)
        if r.ok:

            f = os.path.abspath('saved_searches/serch_for_' + str(keyword) + '.json')
            #self.serialize(f, r)
            result = r.json()
            #print(json.dumps(result, indent=4))
        else:

            logging.error('Could not find ' + keyword)
            logging.error('Error is: ' + str(r.reason))
        return result

    def searchSpecific(self, keyword, fg="Cereal Grains and Pasta", mx=None, ds="SR"):
        '''
        Example:
        http://api.nal.usda.gov/ndb/search/
        ?format=json&q=butter&sort=n&max=25
        &offset=0&api_key=DEMO_KEY
        '''

        payload = {
        'format': 'json',
        'q': keyword,
        'sort': 'r',
        "fg": fg,
        'offset': 0,
        'api_key': 'DEMO_KEY',
        "DS": "SR"

        }
        result = {}
        r = requests.get(search_url, payload)
        #test = open('debug.out', 'r')
        #r = json.load(test)
        #print r
        #json.dump(r.json(), 'debug.out', indent = 4)
        logger.debug(r.headers)
        if r.ok:

            f = os.path.abspath('saved_searches/serch_for_'+keyword+'.json')
            #self.serialize(f, r)
            result = r.json()
            #print(json.dumps(result, indent=4))
        else:

            logging.error('Could not find ' + keyword)
            logging.error('Error is: ' + str(r.reason))
        return result

    
    def serialize(self, filename, query_result):
        '''
        '''
        with open(filename) as f:
            #json.dump(jsonobj, f, indent=4)
            json.dump(query_result.json(), f, indent = 4)

    def pretty_print(self, jobj):
        pass		


    def productNDM(self, j_obj):
        '''
        treat this as a 
        dictionary
        '''
        if not j_obj:
            return None
        items = j_obj[u'list'][u'item']
        for i in items:
            logger.debug(i) #i[u'ndbno'], i[u'name'], i[u'group']
        return items



    def fromNdbNo(self, ndbno):
        '''
        treat this as a 
        dictionary
        '''

        payload = {

        'format': 'json',
        'api_key': 'DEMO_KEY',
        'nutrients': ['205','204','208','269'],
        'ndbno': ['01008', '01009']
 
        }

        result = requests.get(nutrients_url, payload)
        logging.debug(result)
        if result.ok:
            with open('saved_searches/fromNDBNO.json', 'w') as f:

                json.dump(result.json(), f, indent = 4)
        return result


    def rawDB(self, jsonobj, name):
        '''
        the USDA db has raw produce 
        named mostly like: Apple, raw
        but this is
        not a rule, so some
        guesswork is involved in this method
        '''
        name = name.capitalize()
        key = name + ', raw'
        result = self.searchFor(key)
        logging.debug(result) 
        return result   	

    def raw(self, jsonobj, name):
        '''
        the USDA db has raw produce 
        named mostly like: Apple, raw
        but this is 
        not a rule, so some
        guesswork is involved in this method 
        '''
        name = name.capitalize()
        key = name + ', raw'
        result = self.searchFor(key)
         
        logging.debug(result) 
        return result  


def main():

    parser = OptionParser()

    parser.add_option('--find', 
        dest = 'find', 
        type = 'string', 
        help = "search for key in database"
        )
    parser.add_option('--list', 
        dest = 'list', 
        type = 'choice', 
        choices = ['g','f','n', 'ns', 'nr'],
        help = "list items of category"
        #default='f'
        )
    parser.add_option('--debug', '-g', 
        dest = 'debug', 
        action = "store_true",
        default = False,
        help = "print debug info") 
    parser.add_option('--info', 
        dest = 'info', 
        type = 'string',  
        help = "show nutritional info ")         
    (opts, args) = parser.parse_args()

    f = Nutrient()

    if opts.debug:
 
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
    if opts.find:
        product = f.searchFor(opts.find)

        j = f.productNDM(product)

    if opts.list:
        category = f.lists(opts.list)
    
    if opts.info:
        result = f.searchFor(opts.info)
        ndms = f.getNDMNO(result)
        nutritions = f.fromNdbNo(ndms)
    #f.food_report('01009')




if __name__ == '__main__':
    main()





