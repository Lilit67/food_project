
# dry is flours only
flours = ['wheat flour', 'AP flour', 'bread flour', 'rye flour',
          'rye', 'wheat',
          'oat flour', 'oats', 'flour',
          'all purpose flour, white',
          'white flour', 'whole wheat flour',
          'white wheat flour', 'high gluten', 'bakers flour',
          'high extraction flour',
          'white wheat flour (bread flour)',
          'white wheat flour(bread flour) (100 %)',
          'Bread flour', '50/50 blend flour', 'All purpose flour',
          'All-purpose flour', 'whole rye flour', 'white bread flour',
          'pizza flour Caputo red', '00 tipo', 'high extraction',
          'kamut', 'eikhorn', 'barley',
          'brown rice flour', 'white whole what flour',
          'King Arthur (14%)', 'Arrowhead Mills Wholemeal Wheat', 'Arrowhead Mills Wholemeal Spelt',
          ]

# rest of dry ingredients
condiments = ['salt', 'sugar', 'kosher salt',
        'sea salt', 'turbinado sugar',
        'brown sugar', 'coconut sugar',
        'date sugar']

# waters
wet = ['water', 'egg', 'butter', 'milk', 'yoghurt',
       'purified water', 'eggs', 'egg whites',
       'cold water', 'scaled milk', 'kefir', 'warm milk',
       'honey']

waters = ['water', 'milk']

non_usda = ['water', 'starter', 'salt']

starter = ['starter', 'white starter',
           'whole wheat starter',
           'gf starter', 'levain',
           'poolish', 'leaven', 'starter 100%',
           'starter 50/50',
           '50-50 starter']

# oils, should also go as wet
butter = ['butter', 'european butter',
          'butter packet', 'oil',
          'melted butter', 'salted butter',
          'vegetable oil', 'olive oil',
          'clarified butter', 'ghee']

fat = butter

milk = ['cold milk', 'milk', 'buttermilk', 'yoghurt']

wheat = ['wheat', 'whole wheat', 'white wheat', 'white bread flour']

# for searching in usda db
usda_group_item_map = {'Cereal Grains and Pasta': flours,
                       'Dairy and Egg Products': butter,
                        'Fats and Oils': butter

                      }

yeast = ['yeast']

salt = ['salt', 'sea salt', 'himalayan pink salt', 'kosher salt', 'fine salt']