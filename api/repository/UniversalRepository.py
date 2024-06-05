import copy
from typing import Tuple, TypeVar, Generic, List

from api.repository.DBConnector import get_connection


def generate_input_parameters(dictionary: dict) -> Tuple[str, str]:
    if not dictionary:
        return "()", "()"

    placeholders_string = "(" + ", ".join(["?" for _ in dictionary]) + ")"
    keys_string = "(" + ", ".join(dictionary.keys()) + ")"

    return placeholders_string, keys_string


def create_tuple(input_dict: dict, fuzzy: bool = False) -> Tuple:
    if fuzzy:
        return tuple(f'%{value}%' for value in input_dict.values())
    else:
        return tuple(input_dict.values())


def create_condition_string(data: dict, joiner: str = 'AND', fuzzy: bool = False) -> str:
    if len(data) == 0:
        return "1=1"
    conditions = []
    for key, value in data.items():
        if fuzzy:
            condition = f'{key} LIKE (?)'
        else:
            condition = f'{key} = (?)'
        conditions.append(condition)

    condition_string = f" {joiner} ".join(conditions)
    return f'({condition_string})'


def create_dict(obj: object) -> dict:
    return copy.copy(vars(obj))


def dict_diff(dict1: dict, dict2: dict) -> dict:
    return {key: dict2[key] for key in dict1 if dict1[key] != dict2[key]}


def is_alive() -> bool:
    query = f"SELECT 1"
    cursor = get_connection().cursor()
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result == 1


T = TypeVar('T')


class UniversalRepositoryHelper(Generic[T]):

    def __init__(self, cls: T, table_name: str, primary_keys: List[str]):
        self.TABLE_NAME = table_name
        self.CLASS = cls
        self.PRIMARY_KEYS = primary_keys

    def call_sql_query(self, query: str, values: List[str], map_to_object: bool = False) -> 'List[T] | List[dict]':
        query = f"{query}"
        cursor = get_connection().cursor()
        cursor.execute(query, values)
        results = cursor.fetchall()
        if results:
            column_names = [description[0] for description in cursor.description]
            result_list = [dict(zip(column_names, row)) for row in results]
            if map_to_object:
                return [self.__convert_to_instance(data) for data in result_list]
            else:
                return result_list
        else:
            return []

    def get_record_count(self) -> int:
        query = f"SELECT COUNT(1) FROM {self.TABLE_NAME}"
        cursor = get_connection().cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]

    def get_all_records(self, limit: int = 20, offset: int = 0) -> List[T]:
        return self.get_objects_union(dict(), limit, offset)

    def __get_objects_conditional(self, condition_string: str, keys: dict, limit: int = 20,
                                  offset: int = 0, fuzzy: bool = False) -> List[T]:
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE {condition_string} LIMIT (?) OFFSET (?)"

        cursor = get_connection().cursor()
        cursor.execute(query, create_tuple(keys, fuzzy) + tuple([limit, offset]))

        results = cursor.fetchall()

        if results:
            column_names = [description[0] for description in cursor.description]
            result_list = [dict(zip(column_names, row)) for row in results]
            return [self.__convert_to_instance(data) for data in result_list]
        else:
            return []

    def get_objects_fuzzy(self, keys: dict, limit: int = 20, offset: int = 0) -> List[T]:
        condition_string = create_condition_string(keys, 'AND', True)
        return self.__get_objects_conditional(condition_string, keys, limit, offset, True)

    def get_objects_intersection(self, keys: dict, limit: int = 20, offset: int = 0) -> List[T]:
        condition_string = create_condition_string(keys, 'AND', False)
        return self.__get_objects_conditional(condition_string, keys, limit, offset)

    def get_objects_union(self, keys: dict, limit: int = 20, offset: int = 0) -> List[T]:
        condition_string = create_condition_string(keys, 'OR', False)
        return self.__get_objects_conditional(condition_string, keys, limit, offset)

    def does_record_exist(self, keys: dict) -> bool:
        condition_string = create_condition_string(keys)
        query = f"SELECT COUNT(*) FROM {self.TABLE_NAME} WHERE {condition_string}"
        cursor = get_connection().cursor()
        cursor.execute(query, create_tuple(keys))
        result = cursor.fetchall()
        return result[0] >= 1

    def create_object(self, obj: T):
        dictionary = create_dict(obj)
        placeholders_string, keys_string = generate_input_parameters(dictionary)
        query = f"INSERT INTO {self.TABLE_NAME} {keys_string} VALUES {placeholders_string}"
        cursor = get_connection().cursor()
        cursor.execute(query, create_tuple(dictionary))
        get_connection().commit()

    def __update_keys(self, keys: dict, update_data: dict):
        set_clause = ", ".join([f"{column} = ?" for column, value in update_data.items()])
        condition_string = create_condition_string(keys)
        query = f"UPDATE {self.TABLE_NAME} SET {set_clause} WHERE {condition_string}"
        values_tuple = tuple(update_data.values()) + tuple(keys.values())
        cursor = get_connection().cursor()
        cursor.execute(query, values_tuple)
        get_connection().commit()

    def insert_update_object(self, mutated: T):
        mutated_dictionary = create_dict(mutated)
        mutated_primary_keys = \
            {attr: mutated_dictionary[attr] for attr in self.PRIMARY_KEYS if attr in mutated_dictionary}
        original = self.get_objects_intersection(mutated_primary_keys)
        if not original:
            self.create_object(mutated)
        else:
            original_dictionary = create_dict(original[0])
            diff = dict_diff(original_dictionary, mutated_dictionary)
            self.__update_keys(mutated_primary_keys, diff)

    def delete_object(self, obj: T):
        primary_key_values = (getattr(obj, primary_key) for primary_key in self.PRIMARY_KEYS)
        primary_key_dict = {key: value for (key, value) in zip(self.PRIMARY_KEYS, primary_key_values)}
        self.__delete_entry(primary_key_dict)

    def __delete_entry(self, keys: dict):
        condition_string = create_condition_string(keys)
        query = f"DELETE FROM {self.TABLE_NAME} WHERE {condition_string}"
        cursor = get_connection().cursor()
        cursor.execute(query, create_tuple(keys))
        get_connection().commit()

    def __convert_to_instance(self, data: dict) -> T:
        return self.CLASS(**data)
