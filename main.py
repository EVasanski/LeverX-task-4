import argparse
import json
import sys
from configparser import ConfigParser
from getpass import getpass
from os.path import exists

from connector import MyDatabase
from queries import *
from writefile import WriteJSON, WriteXML


def parse_args():
    """ Returns arguments passed to the command line """
    parser = argparse.ArgumentParser(description='List of students living in each room.')
    parser.add_argument('students', type=str, help='Path to the students file')
    parser.add_argument('rooms', type=str, help='Path to the rooms file')
    parser.add_argument('format', type=str, help='Output format (XML or JSON)', choices=['XML', 'JSON'])
    parser.add_argument('--config', type=str, help='Path to the config file', default=False)
    args = parser.parse_args()
    return args


def input_settings():
    settings = {
        'host': input('Host: '),
        'user': input('User: '),
        'password': getpass('Password: '),
        'database': input('Database name: ')
    }
    return settings


def read_db_config(filename='config.ini', section='mysql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
    return db


def is_file_exists(path):
    """ Checking for file existence """
    if exists(path):
        return True
    else:
        print(f'Error: the file "{path}" cannot be found.')
        sys.exit()


def reed_files(stud_file, room_file):
    """ Returns the contents of the input files """
    if is_file_exists(stud_file):
        with open(stud_file, 'r') as file:
            students = json.load(file)
    if is_file_exists(room_file):
        with open(room_file, 'r') as file:
            rooms = json.load(file)
    return students, rooms


def serialize_list_of_dicts_to_str(students, rooms):
    students_values = str([tuple(student.values()) for student in students])[1:-1]
    rooms_values = str([tuple(room.values()) for room in rooms])[1:-1]
    return students_values, rooms_values


def insert_into_tables(database, rooms, students):
    database.execute(create_table_students_query)
    database.execute(create_table_rooms_query)
    database.execute(insert_into_students_query(students))
    database.execute(insert_into_rooms_query(rooms))
    database.execute(create_index_query)


def main():
    args = parse_args()
    students, rooms = reed_files(args.students, args.rooms)
    students_values, rooms_values = serialize_list_of_dicts_to_str(students=students, rooms=rooms)
    if not args.config:
        settings = input_settings()
    else:
        settings = read_db_config()

    db_host = settings.get('host')
    db_user = settings.get('user')
    db_password = settings.get('password')
    db_name = settings.get('database')

    queries = {
        'result_query1': select_count_of_students_by_room_query,
        'result_query2': select_min_avg_age_by_room_query,
        'result_query3': select_max_age_difference_by_room_query,
        'result_query4': select_rooms_by_with_different_sexes_query
    }

    with MyDatabase(db_host=db_host, db_user=db_user, db_password=db_password, db_name=db_name) as database:
        insert_into_tables(database, students=students_values, rooms=rooms_values)

        for query in queries:
            data = database.query_to_dict(queries[query])
            if args.format == 'JSON':
                WriteJSON(file_name=query).write(data)
            elif args.format == 'XML':
                WriteXML(file_name=query).write(data)


if __name__ == "__main__":
    main()
