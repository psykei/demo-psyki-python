from pathlib import Path

PATH = Path(__file__).parents[0]
UCI_URL: str = "https://archive.ics.uci.edu/ml/machine-learning-databases/"


class CensusIncome(object):
    name: str = 'census-income'
    knowledge_file_name: str = 'census-income.pl'
    data_url: str = UCI_URL + "adult/adult.data"
    data_test_url: str = UCI_URL + "adult/adult.test"
    features: list[str] = ["Age", "WorkClass", "Fnlwgt", "Education", "EducationNumeric", "MaritalStatus",
                           "Occupation", "Relationship", "Ethnicity", "Sex", "CapitalGain", "CapitalLoss",
                           "HoursPerWeek", "NativeCountry"]
    target: list[str] = ["income"]
    class_mapping: dict[str, int] = {'0.0': 0, '1.0': 1}
    integer_features: list[str] = ["Age", "CapitalGain", "CapitalLoss", "HoursPerWeek"]
    ordinal_features: list[str] = ["EducationNumeric"]
    binary_features: list[str] = ["Sex"]
    nominal_features: list[str] = ["WorkClass", "MaritalStatus", "Occupation", "Relationship", "Ethnicity", "NativeCountry"]
    droppable_features: list[str] = ["Fnlwgt", "Education"]
