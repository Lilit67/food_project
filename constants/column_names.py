class ColumnNames:
    # column names
    weight = 'amount'
    ingredient = 'ingredient'
    code = 'USDA #'
    usda_name = 'USDA NAME'
    BP = 'BP'
    unit = 'unit'
    ingredient_type = 'type 1'
    step_no = 'stepNo'
    step_description = 'step description'
    step_name = 'step name'
    temperature = 'temperature'
    brand = 'brand'
    manufacturer = 'manufacturer'
    time_in_minutes = 'time in minutes'

    @staticmethod
    def get_ordered():
        return [ColumnNames.ingredient, ColumnNames.weight, ColumnNames.unit,
                ColumnNames.step_no, ColumnNames.step_name,
                ColumnNames.step_description,
                ColumnNames.time_in_minutes, ColumnNames.brand,
                ColumnNames.manufacturer, ColumnNames.temperature,
                ColumnNames.time_in_minutes
                ]

    @staticmethod
    def column_names():
        return ColumnNames.get_ordered()