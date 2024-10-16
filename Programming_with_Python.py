'''

Module Name: Programming_with_Python
Description: This program reads data from .csv files, inserts it into a database,
                and applies analysis and visualization techniques
                Finally, the correct functionality of the program is ensured through Unit Tests

Author: Clemens Reh
Date: 14.08.2024

Order of execution / pipeline of the program:
    When started, the program first creates a connection to a database.
    Then, the individual datasets are read and stored in the database, for which different classes are used.
    Afterwards, the program selects four ideal functions, maps the individual data points to these functions
    and inserts the results into a database.
    Furthermore, the program displays the data points and functions.
    The mapping of data points to functions is thereby visualized through different colors.
    Finally, unit-tests are applied to ensure the correct functionality of:
        - Saving data in a database and retrieving it as rows
        - Saving data in a database and retrieving it as columns
        - Finding the best matching functions
        - Assigning data points to found best matching functions
        - Saving the assignments of data points to functions in a database



Components:
 - Classes:
    - Data: Class providing functions to store and retrieve data from a database
    - TrainingData(Data): Child class of Data, used for training data
    - IdealFunctions(Data): Child class of Data, used for ideal data
    - TestData(Data): Child class of Data, used for test data
    - TestResults(Base): Class to save test results in a database
    - UnitTestTestResults(Base): Class to save test results of unit-tests in a database
    - AppendedTestDatabaseException(Exception): Custom exception, is raised in the unit-tests if the database contains
        to many values (e.g., if the data from a previous exectution of the program is still included
    - UnitTests(unittest.TestCase): Class containing the unit-tests
 - Important Methods:
    -






'''



import os
import unittest

import bokeh
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, Legend

import sqlalchemy as db


# Set to True to only perform the unit tests
onlyUnitTests = False


# Define the base for SQLAlchemy ORM classes
Base = declarative_base()


class Data():
    '''
    Main class responsible for the object oriented reading of data from a csv file,
    as well as saving and accessing it from a SQL database

    Functions:
        - __init__(filepath, engine, table_name): read data from a csv file and save it in a SQL database
        - getColumns(): get the data column wise
        - getRows(): get the data row wise
        - getDataframe(): get the data as a pandas dataframe
        - get_x_row(): get a specific row from the database
    '''

    # Example of handling exceptions for CSV loading and database operations
    def __init__(self, filepath, engine, table_name):
        '''
        Read data from a csv file and save it in a SQL database
        :param filepath: the path of the csv file
        :param engine: the engine of the database
        :param table_name: the name of the table in the database the data will be saved in
        '''

        try:
            self.engine = engine
            self.table_name = table_name
            self.data = pd.read_csv(filepath)

            self.data.to_sql(table_name, con=engine, index=False, if_exists='replace')
        except FileNotFoundError:
            print("File not found, please check the path and try again.")
        except pd.errors.ParserError:
            print("Error parsing the file, please check the file format.")


    def getColumns(self):
        '''
        Get the Columns of the database
        :return: An array containing the data column wise
        '''

        # Select and print data
        meta_data = db.MetaData()
        connection = self.engine.connect()

        result = []
        try:
            table = db.Table(self.table_name, meta_data, autoload_with=self.engine)
            result = connection.execute(db.select(table))
            result = [list(col) for col in zip(*result)]
        finally:
            connection.close()

        return result

    def getRows(self):
        '''
        Get the Rows of the database
        :return: An array containing the data row wise
        '''

        # Select and print data
        meta_data = db.MetaData()
        connection = self.engine.connect()

        result = []
        try:
            table = db.Table(self.table_name, meta_data, autoload_with=self.engine)
            result = connection.execute(db.select(table))
            result = [list(col) for col in result]
        finally:
            connection.close()

        return result

    def get_dataframe(self):
        '''
        Get the data as a pandas dataframe
        :return: the data as a pandas dataframe
        '''
        meta_data = db.MetaData()
        table = db.Table(self.table_name, meta_data, autoload_with=engine)

        # Use a context manager to ensure that the connection is closed
        with engine.connect() as connection:
            # Select everything from table and load directly into a DataFrame
            query = table.select()
            result = pd.read_sql(query, connection)

        return result

    def get_x_row(self, x):
        '''
        Get a specific row of the database (table)
        :param x: the index of the row to be selected
        :return: the row at position x of the data
        '''

        # Select and print data
        meta_data = db.MetaData()
        connection = self.engine.connect()

        result = []
        try:
            table = db.Table(self.table_name, meta_data, autoload_with=self.engine)
            query = db.select(table).where(table.c.x == x)
            result = connection.execute(query).fetchall()
            result = result[0]
        finally:
            connection.close()

        return result


# Define a class for training data in the database
class TrainingData(Data):
    '''
    Child class of data
    Represents the Training data
    '''
    def __init__(self, filepath, engine):
        super().__init__(filepath, engine, 'training_data')


# Define a class for ideal functions in the database
class IdealFunctions(Data):
    '''
    Child class of data
    Represents the Ideal data
    '''
    def __init__(self, filepath, database):
        super().__init__(filepath, database, 'ideal_functions')


class TestData(Data):
    '''
    Child class of data
    Represents the Test data
    '''
    def __init__(self, filepath, database):
        super().__init__(filepath, database, 'test_data')

# Define a class for test results in the database
class TestResults(Base):
    '''
    Class used for the representation of the results of the assignment of test data to best functions when inserting them into the database
    '''
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True)
    X = Column(Float)  # Adjust types as necessary
    Y = Column(Float)
    Delta_Y = Column(Float)
    No_of_ideal_func = Column(Integer)


class UnitTestTestResults(Base):
    '''
    Class used for the representation of the results of the assignment of test data to best functions when inserting them into the database
    Used for the results of Unit Tests to avoid errors
    '''
    __tablename__ = 'unit_tests_test_results'
    id = Column(Integer, primary_key=True)
    X = Column(Float)  # Adjust types as necessary
    Y = Column(Float)
    Delta_Y = Column(Float)
    No_of_ideal_func = Column(Integer)


# Delete the database-file if exists, to make sure no redundancies from previous runs are included
if (os.path.isfile('database.db')):
    os.remove('database.db')

# Establish connection to a SQLite database and create tables
try:
    engine = create_engine('sqlite:///database.db')
    Base.metadata.create_all(engine)
except Exception as e:
    print(f"Error establishing database connection or creating tables: {e}")

# Create a Session class and instantiate it
Session = sessionmaker(bind=engine)
session = Session()




def find_best_matching_functions(training_data, ideal_functions_data):
    '''
    Match training functions to ideal functions
    :param training_data: the training functions
    :param ideal_functions_data: the ideal functions
    :return: the results of the matching (i.e., the best functions)
    '''

    best_functions = []
    training_data_columns = training_data.getColumns()
    ideal_functions_columns = ideal_functions_data.getColumns()
    for column in training_data_columns[1:]:
        min_error = float('inf')
        best_function_id = None
        y_training = column
        for func_id in range(1, len(ideal_functions_columns)):
            y_ideal = ideal_functions_columns[func_id]
            if len(y_training) == len(y_ideal):
                error = 0
                for i in range (0, len(y_training)):
                    error += (y_training[i] - y_ideal[i]) ** 2
                if error < min_error:
                    min_error = error
                    best_function_id = func_id
        best_functions.append(best_function_id)
    return best_functions


def get_maximum_deviation(training_function, ideal_function):
    '''
    Get the largest deviation between points with the same x value in the training function and the ideal function
    :param training_function: the training function (an array of x and y values)
    :param ideal_function: the ideal function (an array of x and y values)
    :return: the maximum found deviation between points with the same x value in the given functions as a float value
    '''

    max_deviation = -1
    for i in range (0, len(training_function)):
        training_val = training_function[i]
        ideal_val = ideal_function[i]
        deviation = abs(training_val - ideal_val)
        if deviation > max_deviation:
            max_deviation = deviation
    return max_deviation


def assign_test_data (training_data, ideal_data, test_data, best_functions, session, unit_tests, save_mappings=True):
    '''
    Assign the test data points to one of the best functions if the criteria are matched
    :param training_data: the training functions
    :param ideal_data: the ideal functions
    :param test_data: the test data points
    :param best_functions: the found best functions (their ids)
    :param session: the session of the database connection
    :param unit_tests: a boolean value representing whether the functions was called as part of a unit test
    :param save_mappings: a boolean value indicating whether the assignments produced in this function should be saved in the database
    :return: the results of the matching of values
    '''

    deviations = {}
    # Get the maximum deviation of each selected best function to its assigned function#
    for func_id in best_functions:
        min_deviation = float('inf')
        for column in training_data.getColumns()[1:]:
            dev = get_maximum_deviation(column, ideal_data.getColumns()[func_id])
            if dev < min_deviation:
                min_deviation = dev
        deviations[func_id] = min_deviation

    results = []
    for row in test_data.getRows():
        x, y = row[0], row[1]
        best_match = None
        min_deviation = float('inf')
        ideal_x_row = ideal_data.get_x_row(x)
        for func_id in best_functions:
            ideal_val = getattr(ideal_x_row, 'y'+ str(func_id))
            dev = abs(y - ideal_val)
            if dev < min_deviation:
                best_match = func_id
                min_deviation = dev
        if best_match is not None and min_deviation <= deviations.get(best_match) * np.sqrt(2):
            results.append({'X': x, 'Y': y, 'Delta_Y': min_deviation, 'Ideal_Function_No': best_match})

    if (save_mappings):
        save_test_mappings(results, session, unit_tests)

    return results

def save_test_mappings(test_mappings, session, unit_tests):
    '''
    Save the results of assign_test_data in a SQL database
    :param test_mappings: the results of assign_test_data
    :param session: the session of the database
    :param unit_tests: whether or not assign_test_data was called as part of a unit test
    :return: None
    '''

    for mapping in test_mappings:
        # Unpack each tuple into the respective fields of the TestMapping
        if unit_tests:
            record = UnitTestTestResults(X=mapping['X'], Y=mapping['Y'], Delta_Y=mapping['Delta_Y'],
                                 No_of_ideal_func=mapping['Ideal_Function_No'])
        else:
            record = TestResults(X=mapping['X'], Y=mapping['Y'], Delta_Y=mapping['Delta_Y'], No_of_ideal_func=mapping['Ideal_Function_No'])
        session.add(record)

    # Commit the session to write the objects to the database
    session.commit()
        
# Visualization function using Bokeh
def visualize_data(training_data, title, idealData, test_data, best_functions, test_mappings):
    '''
    Visualize the given data points using Bokeh and colorize them depending on their type
    Output: a .html file containing the visualization
    :param training_data: the training data
    :param title: the title of the visualization
    :param idealData: the ideal data
    :param test_data: the test data
    :param best_functions: the found best functions
    :param test_mappings: the mappings of the test data points
    :return: None
    '''

    output_file(f"{title}.html")
    training_source = ColumnDataSource(training_data.get_dataframe())
    p = bokeh.plotting.figure(title=title, x_axis_label='x', y_axis_label='y', width=800)
    ideal_colors = ['green', 'red', 'navy', 'yellow']
    training_legend = []
    for i in range (0, len(training_data.getColumns())-1):
        p.circle('x', 'y' + str(i+1), source=training_source, size=6, color=ideal_colors[i], alpha=0.5)
        training_legend.append(('Training Column y' + str(i + 1), [p.circle(0, 0, source=training_source, size=6, color=ideal_colors[i], alpha=0.5)]))
    ideal_source = ColumnDataSource(idealData.get_dataframe())
    best_colors = ['springgreen', 'pink', 'orange', 'peru']
    ideal_legend = []
    for i in range(0, len(best_functions)):
        p.circle('x', 'y' + str(best_functions[i]), source=ideal_source, size=4, color=best_colors[i], alpha=0.5)
        ideal_legend.append(('Ideal Function ' + str(i), [
            p.circle(0, 0, source=ideal_source, size=4, color=best_colors[i], alpha=0.5)]))

    test_source = ColumnDataSource(test_data.get_dataframe())
    mapped_test_points = []
    mapped_test_points_legend = [('Mapped Test Points', [p.circle(0, 0, size=6, color='purple', alpha=0.5)])]
    for mapping in test_mappings:
        p.circle(mapping['X'], mapping['Y'], size=6, color='purple', alpha=0.5)
        mapped_test_points.append(mapping['X'])

    unmapped_test_data_legend = [('Unmapped Test Data', [p.circle (0, 0, size=6, color='black', alpha=0.5)])]
    for row in test_data.getRows():
        if not mapped_test_points.__contains__(row[0]):
            p.circle (row[0], row[1], size=6, color='black', alpha=0.5)
    legend_list = training_legend + ideal_legend + mapped_test_points_legend + unmapped_test_data_legend
    legend = Legend(items=legend_list)

    p.add_layout(legend, 'right')

    show(p)




# if __name__ == "__main__":
if not onlyUnitTests:
    '''
    The function calls necessary to perform the tasks
    '''
    training_data = TrainingData('Dataset2/train.csv', engine)
    ideal_functions_data = IdealFunctions('Dataset2/ideal.csv', engine)
    test_data = TestData('Dataset2/test.csv', engine)
    training_data.getColumns()
    best_functions = find_best_matching_functions(training_data, ideal_functions_data)
    test_mappings = assign_test_data(training_data, ideal_functions_data, test_data, best_functions, session, False)
    visualize_data(training_data, "Visualization", ideal_functions_data, test_data, best_functions, test_mappings)




class AppendedTestDatabaseException(Exception):
    '''
    Exception used in the Unit Test 'test_assign_test_data' if the amount of test mappings returned by
    the database query is larger than the amount of test points that were tried to be mapped
    '''
    def __init__(self, message, test_data_length, database_length):
        '''
        The initialization of the exception
        :param message: the message of the exception
        :param test_data_length: the amount of test data points that were tried to be mapped
        :param database_length: the amount of test mappings returned by the database query
        '''
        super().__init__(self, message)
        self.message = message
        self.test_data_length = test_data_length
        self.database_length = database_length

    def __str__(self):
        '''
        Converts the information given to the Exception into a final string
        :return: the string representation of the exception
        '''
        return f"{self.message}, (Amount of tested values: {self.test_data_length}, Amount of values in Database: {self.database_length})"



class UnitTests(unittest.TestCase):
    '''
    The Class used for Unit Testing

    Unit Tests:
        - test_save_data(): Tests whether the reading of data from a csv file, as well as saving and reading it into a SQL Database is working properly
        - test_find_best_matching_function(): Tests whether the finding of the best matching functions is working properly
        - test_assign_test_data(): Tests whether the matching of specific data points to the best found functions is working properly
        - test_visualize(): Tests whether the visualization of the results is working properly
    '''


    def test_save_data_rows(self):
        '''
        Unit Test
        Tests whether the reading of data from a csv file, as well as saving and reading it into a SQL Database is working properly

        :return: None
        '''

        print('Test Saving Data')
        data = Data('unit_test-ideal.csv', engine, 'test_data')

        self.assertEqual(data.getRows(), [[1, 1, 2, 3], [2, 4, 5, 6], [3, 7, 8, 9]], 'Rows should be [[1, 1, 2, 3], '
                                                                                     '[2, 4, 5, 6], [3, 7, 8, 9]]')
        self.assertEqual(data.getColumns(), [[1, 2, 3], [1, 4, 7], [2, 5, 8], [3, 6, 9]],
                         'Columns should be [[1, 2, 3], [1, 4, 7], [2, 5, 8], [3, 6, 9]]')


    def test_save_data_cols(self):
        '''
        Unit Test
        Tests whether the reading of data from a csv file, as well as saving and reading it into a SQL Database is working properly

        :return: None
        '''

        print('Test Saving Data')
        data = Data('unit_test-ideal.csv', engine, 'test_data')

        self.assertEqual(data.getColumns(), [[1, 2, 3], [1, 4, 7], [2, 5, 8], [3, 6, 9]],
                         'Columns should be [[1, 2, 3], [1, 4, 7], [2, 5, 8], [3, 6, 9]]')

    def test_find_best_matching_function(self):
        '''
        Unit Test
        Tests whether the finding of the best matching functions is working properly

        :return: None
        '''

        print('Test find_best_matching_function')

        train_data = Data('unit_test-train.csv', engine, 'test_data2')
        ideal_data = Data('unit_test-ideal.csv', engine, 'test_data')

        matches = find_best_matching_functions(train_data, ideal_data)
        self.assertEqual(matches, [1,3], 'Ideal Functions should be 1 and 3')


    def test_assign_test_data(self):
        '''
        Unit Test
        Tests whether the matching of specific data points to the best found functions is working properly

        :return: None
        '''

        print('Test assign_test_data')

        train_data = Data('unit_test-train.csv', engine, 'test_data2')
        ideal_data = Data('unit_test-ideal.csv', engine, 'test_data')
        test_data = Data('unit_test-test.csv', engine, 'test_data3')

        matches = find_best_matching_functions(train_data, ideal_data)

        assigned_tests = assign_test_data(train_data, ideal_data, test_data, matches, session, True, False)

        self.assertEqual(assigned_tests, [{'X': 1, 'Y': 2.4, 'Delta_Y': 0.6000000000000001, 'Ideal_Function_No': 3}, {'X': 3, 'Y': 7.1, 'Delta_Y': 0.09999999999999964, 'Ideal_Function_No': 1}], 'Assignments should be: [1,2.4] -> 3; [3,7.1] -> 1')


    def test_save_assigned_data(self):
        '''
        Unit Test
        Tests whether the matching of specific data points to the best found functions is working properly

        :return: None
        '''

        print('Test assign_test_data')

        train_data = Data('unit_test-train.csv', engine, 'test_data2')
        ideal_data = Data('unit_test-ideal.csv', engine, 'test_data')
        test_data = Data('unit_test-test.csv', engine, 'test_data3')

        matches = find_best_matching_functions(train_data, ideal_data)

        assigned_tests = assign_test_data(train_data, ideal_data, test_data, matches, session, True)

        meta_data = db.MetaData()
        connection = engine.connect()

        query_result = []
        try:
            table = db.Table('unit_tests_test_results', meta_data, autoload_with=engine)
            query_result = connection.execute(db.select(table))
            query_result = [list(col) for col in zip(*query_result)]
        finally:
            connection.close()

        try:
            if (len(query_result[0]) > len(test_data.getRows())):
                print(query_result)
                raise AppendedTestDatabaseException(
                    "The database contains more values than were tested, make sure it is empty before performing tests! (try deleting database.db)",
                    len(test_data.getRows()), len(query_result[0]))
            # Note: the database has to be reset after every run, as the results of previous executions will still be present otherwise
            self.assertEqual(query_result,
                             [[1, 2], [1.0, 3.0], [2.4, 7.1], [0.6000000000000001, 0.09999999999999964], [3, 1]],
                             'Test Results were not saved properly')
        except AppendedTestDatabaseException as e:
            print('\033[91m' + "An exception occurred:", e, '\033[0m')


session.close()
