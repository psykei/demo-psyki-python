import re
from pathlib import Path
from typing import Callable, Iterable
import pandas as pd
from psyki.logic import Formula, Theory
from psyki.logic.prolog import TuProlog
from knowledge import UCI_URL, PATH as KNOWLEDGE_PATH
from abc import ABCMeta

PATH = Path(__file__).parents[0]


class Dataset(ABCMeta):
    name: str = "Dataset name"
    data_file_name: str = None
    data_test_file_name: str = None
    knowledge_filename: str = None
    data_url: str = None
    data_url_test: str = None
    class_mapping: dict[str, int] = {}
    features: list[str] = []
    target: list[str] = []
    preprocess: bool = False
    need_download: bool = True

    @classmethod
    @property
    def is_downloaded(mcs) -> bool:
        return (PATH / mcs.data_file_name).is_file()

    @classmethod
    @property
    def is_test_downloaded(mcs) -> bool:
        return (PATH / mcs.data_test_file_name).is_file() if mcs.data_test_file_name is not None else False

    @classmethod
    def download(mcs) -> None:

        def update_columns_names(df: pd.DataFrame) -> None:
            if len(df.columns) == len(mcs.features) + len(mcs.target):
                df.columns = mcs.features + mcs.target

        if mcs.need_download and not mcs.is_downloaded:
            d: pd.DataFrame = pd.read_csv(
                mcs.data_url, sep=r",\s*", header=None, encoding="utf8"
            )
            update_columns_names(d)
            d.to_csv(PATH / mcs.data_file_name, index=False)
        if mcs.data_url_test is not None and not mcs.is_test_downloaded:
            d: pd.DataFrame = pd.read_csv(
                mcs.data_url_test, sep=r",\s*", header=None, encoding="utf8"
            )
            update_columns_names(d)
            d.to_csv(PATH / mcs.data_test_file_name, index=False)

    @classmethod
    def get_knowledge(mcs) -> list[Formula]:
        return TuProlog.from_file(str(KNOWLEDGE_PATH / mcs.knowledge_filename))

    @classmethod
    def get_theory(mcs) -> Theory:
        return Theory(mcs.get_knowledge(), mcs.get_train(), mcs.class_mapping)

    @classmethod
    def get_train(mcs, preprocess: bool = False) -> pd.DataFrame:
        if not mcs.is_downloaded:
            mcs.download()
        if mcs.preprocess and preprocess:
            return mcs.get_processed_dataset(mcs.data_file_name)
        else:
            return pd.read_csv(PATH / mcs.data_file_name)

    @classmethod
    def get_test(mcs, preprocess: bool = False) -> pd.DataFrame:
        if mcs.data_test_file_name is None:
            return pd.DataFrame()
        else:
            if not mcs.is_test_downloaded:
                mcs.download()
            if mcs.preprocess and preprocess:
                return mcs.get_processed_dataset(mcs.data_test_file_name)
            else:
                return pd.read_csv(PATH / mcs.data_file_name)

    @staticmethod
    def get_processed_dataset(data: str or pd.DataFrame) -> pd.DataFrame:
        pass


class CensusIncome(Dataset):
    name: str = "census-income"
    knowledge_file_name: str = "census-income.pl"
    data_file_name: str = "census-income.csv"
    data_test_file_name: str = "census-income-test.csv"
    data_url: str = UCI_URL + "adult/adult.data"
    data_test_url: str = UCI_URL + "adult/adult.test"
    features: list[str] = [
        "Age",
        "WorkClass",
        "Fnlwgt",
        "Education",
        "EducationNumeric",
        "MaritalStatus",
        "Occupation",
        "Relationship",
        "Ethnicity",
        "Sex",
        "CapitalGain",
        "CapitalLoss",
        "HoursPerWeek",
        "NativeCountry",
    ]
    target: list[str] = ["income"]
    class_mapping: dict[str, int] = {"0.0": 0, "1.0": 1}
    integer_features: list[str] = ["Age", "CapitalGain", "CapitalLoss", "HoursPerWeek"]
    ordinal_features: list[str] = ["EducationNumeric"]
    binary_features: list[str] = ["Sex"]
    nominal_features: list[str] = [
        "WorkClass",
        "MaritalStatus",
        "Occupation",
        "Relationship",
        "Ethnicity",
        "NativeCountry",
    ]
    droppable_features: list[str] = ["Fnlwgt", "Education"]

    @staticmethod
    def get_processed_dataset(data: str or pd.DataFrame) -> pd.DataFrame:
        if isinstance(data, str):
            data = pd.read_csv(PATH / data)
        new_data = data.copy()
        new_data.drop(CensusIncome.droppable_features, axis=1, inplace=True)
        new_data.Sex = new_data.Sex.apply(lambda x: 0 if x.replace(" ", "") in ('Male', "Male.") else 1)
        target = new_data.income.apply(lambda x: 0 if x.replace(" ", "") in ('<=50K', "<=50K.") else 1)
        new_data.drop(CensusIncome.target, axis=1, inplace=True)
        new_data.drop(CensusIncome.nominal_features, axis=1, inplace=True)
        one_hot = pd.get_dummies(data[CensusIncome.nominal_features].apply(lambda x: x.str.upper()),
                                 columns=CensusIncome.nominal_features)
        callback: Callable = lambda pat: pat.group(1) + "_" + pat.group(2).lower()
        one_hot.columns = [re.sub(r"([A-Z][a-zA-Z]*)[_][ ](.*)", callback, f) for f in one_hot.columns]
        # Special characters removed
        one_hot.columns = [f.replace('?', 'unknown') for f in one_hot.columns]
        one_hot.columns = [f.replace('-', '_') for f in one_hot.columns]
        one_hot.columns = [f.replace('&', '_') for f in one_hot.columns]
        one_hot.columns = [f.replace('NativeCountry_outlying_us(guam_usvi_etc)', 'NativeCountry_outlying_us') for f in
                           one_hot.columns]
        new_data = pd.concat([new_data, one_hot, target], axis=1)
        return new_data


class SpliceJunction(Dataset):
    name: str = "splice-junction"
    knowledge_file_name: str = "splice-junction.pl"
    data_file_name: str = "splice-junction.csv"
    data_url: str = UCI_URL + "molecular-biology/splice-junction-gene-sequences/splice.data"
    features = {
        "X" + ("_" if j < 0 else "") + str(abs(j)) + f: k + i * 4
        for i, j in enumerate(list(range(-30, 0)) + list(range(1, 31)))
        for k, f in enumerate(["a", "c", "g", "t"])
    }
    features_values: list[str] = ['a', 'c', 'g', 't']
    target: list[str] = ["class"]
    class_mapping: dict[str, int] = {'EI': 0, 'IE': 1, 'N': 2}
    preprocess = True

    @staticmethod
    def get_processed_dataset(data: str or pd.DataFrame) -> pd.DataFrame:
        def _data_to_int(d: pd.DataFrame, mapping: dict[str:int]) -> pd.DataFrame:
            return d.applymap(lambda x: mapping[x] if x in mapping.keys() else x)

        def _get_values(mapping: dict[str: set[str]]) -> Iterable[str]:
            result = set()
            for values_set in mapping.values():
                for value in values_set:
                    result.add(value)
            return result

        def _get_binary_data(
                d: pd.DataFrame, mapping: dict[str: set[str]]
        ) -> pd.DataFrame:
            sub_features = sorted(_get_values(mapping))
            results = []
            for _, row in d.iterrows():
                row_result = []
                for value in row:
                    positive_features = mapping[value]
                    for feature in sub_features:
                        row_result.append(1 if feature in positive_features else 0)
                results.append(row_result)
            return pd.DataFrame(results, dtype=int)

        aggregate_mapping = {
            "a": ("a",),
            "c": ("c",),
            "g": ("g",),
            "t": ("t",),
            "d": ("a", "g", "t"),
            "m": ("a", "c"),
            "n": ("a", "c", "g", "t"),
            "r": ("a", "g"),
            "s": ("c", "g"),
            "y": ("c", "t"),
        }
        x = []
        if isinstance(data, pd.DataFrame):
            for row in data.iterrows():
                label, features = row[1][0], row[1][2]
                features = list(f for f in features.lower())
                features.append(label.lower())
                x.append(features)
        else:
            with open(str(PATH / data), encoding="utf8") as f:
                for row in f:
                    row = re.sub("\n", "", row)
                    label, _, features = row.split(",")
                    features = list(f for f in features.lower())
                    features.append(label.lower())
                    x.append(features)
        data = pd.DataFrame(x)
        y = _data_to_int(data.iloc[:, -1:], SpliceJunction.class_mapping)
        x = _get_binary_data(data.iloc[:, :-1], aggregate_mapping)
        y.columns = [x.shape[1]]
        x.columns = SpliceJunction.features
        return x.join(y)
