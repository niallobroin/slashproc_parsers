#!/usr/bin/env python
import sys
import unittest
from sp_parser.basic_sp_parser import BasicSPParser
from sp_parser.basic_sp_parser import MSG

class DummyParser(BasicSPParser):
    """Mockup parser for testing purposes.

    Overrides base class methods so that they return predefined
    dictionaries to emulate correctly performed parsing.

    """

    @staticmethod
    def get_vars():
        return {'var1': {'name': 'The first variable', 'unit': 'kB'},
                'var2': {'name': 'The second variable', 'unit': 'MB'},
                'var3': {'name': 'The third variable', 'unit': ''}}

    @staticmethod
    def get_groups():
        return {'group1': {'name': 'The first group', 'parents': ['root'],
                           'desc': 'Group for test case'},
                'subgroup1': {'name': 'The first subgroup', 'parents': ['group1'],
                              'desc': 'The first subgroup for test case'},
                'subgroup2': {'name': 'The second subgroup', 'parents': ['group1'],
                              'desc': 'The second Subgroup for test case'}}

    @staticmethod
    def get_data():
        return {'group1': {'subgroup1': {'var1': 'val1',
                                         'var2': 'val2'},
                           'subgroup2': {'var3': 'val3'}}}


class ListStream:
    """Helper class for output redirection into list.

    Class instances are file-like objects that can be assigned
    to output stream to store it into list container.

    """

    def __init__(self):
        self.output = []

    def __iter__(self):
        for s in self.output:
            yield s

    def write(self, s):
        self.output.append(s)

    def clear(self):
        self.output = []


class TestBasicParser(unittest.TestCase):

    def setUp(self):
        self.parser = BasicSPParser()

    def test_get_groups(self):
        self.assertRaises(NotImplementedError, self.parser.get_data)

    def test_get_vars(self):
        self.assertRaises(NotImplementedError, self.parser.get_vars)

    def test_get_data(self):
        self.assertRaises(NotImplementedError, self.parser.get_data)

    def test_get_class(self):
        expected_class_name = "BasicSPParser".lower()
        self.assertEqual(self.parser.get_class(), expected_class_name, "Unexpected class name")


class TestAllValidationsPassed(unittest.TestCase):
    """
    Tests validation success of correctly structured parsing result
    """

    def setUp(self):
        self.concrete_parser = DummyParser()

    def test_validate_groups_success(self):
        self.assertTrue(self.concrete_parser.validate_groups(),
                        "Valid groups parsing result failed validation")

    def test_validate_vars_success(self):
        self.assertTrue(self.concrete_parser.validate_vars(),
                        "Valid vars parsing result failed validation")

    def test_validate_data_success(self):
        self.assertTrue(self.concrete_parser.validate_data(),
                        "Valid data parsing result failed validation")

    def test_validate_parser(self):
        self.assertTrue(self.concrete_parser.validate_parser(),
                        "Valid parser failed validation")


class TestGroupsValidationFailed(unittest.TestCase):
    """
    Tests validation failure of incorrectly structured groups dictionary
    """

    class MalformedGroupsParser(DummyParser):
        """Mockup parser for testing purposes.

        Inherits basic mockup `DummyParser` and changes it's behaviour
        to return incorrectly structured groups parsing result

        """

        @staticmethod
        def get_groups():
            return {'group1': {'name': 'The first group', 'parents': ['root'],
                               'desc': 'Group for test case'},
                    'subgroup1': {'name': 'The first subgroup', 'parents': ['not_exists']},
                    'subgroup2': {'parents': ['group1'], 'desc': 'Subgroup for test case'}
                    }

    def setUp(self):
        self.output = ListStream()
        sys.stdout = self.output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_validate_groups_failed(self):
        parser = self.MalformedGroupsParser()
        result = parser.validate_groups(debug=True)

        errors = [err for err in self.output if err.strip()][1:]

        expected_messages = {
                             MSG.debug(7, 'subgroup1'),
                             MSG.debug(11, 'subgroup2'),
                             MSG.err(9, 'not_exists'),
                             MSG.debug(11, 'group1'),
                             MSG.debug(11, 'subgroup1'),
                             MSG.err(16)}
        for err in errors:
            self.assertTrue(err in expected_messages, err)

        self.assertFalse(result, "Groups validation supposed to fail but succeeded")

        self.output.clear()


class TestVarsValidationFailed(unittest.TestCase):
    """
    Tests validation failure of incorrectly structured variables dictionary
    """

    class MalformedVarsParser(DummyParser):
        """Mockup parser for testing purposes.

        Inherits basic mockup `DummyParser` and changes it's behaviour
        to return incorrectly structured variables parsing result
        """

        @staticmethod
        def get_vars():
            return {'bad var key': {'label': 'The badly named var', 'unit': '',
                                    'desc': 'Variable has incorrect key'},
                    'has_no_name': {'unit': 'kB',
                                    'desc': 'Variable has no name key'},
                    'has_no_unit': {'label': 'Var without unit',
                                    'desc': 'Variable has no unit key'},
                    'has_no_description': {'name': 'Var without description',
                                           'unit': 'MB'}}

    def setUp(self):
        self.output = ListStream()
        sys.stdout = self.output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_validate_vars_failed(self):
        parser = self.MalformedVarsParser()
        result = parser.validate_vars(debug=True)

        errors = [err for err in self.output if err.strip()][1:]

        expected_messages = {MSG.err(10, 'bad var key'),
                             MSG.debug(8, 'has_no_description'),
                             MSG.debug(9, 'has_no_name'),
                             MSG.debug(10, 'has_no_unit'),
                             MSG.debug(9, 'has_no_description')}


        for err in errors:
            self.assertTrue(err in expected_messages, err)

        self.assertFalse(result, "Variables validation supposed to fail, but succeeded")

        self.output.clear()


class TestDataValidationFailed(unittest.TestCase):
    """
    Tests validation failure of incorrectly structured data dictionary
    """

    class MalformedDataParser(DummyParser):
        """Mockup parser for testing purposes.

        Inherits basic mockup `DummyParser` and changes it's behaviour
        to return incorrectly structured data parsing result. Returns
        incorrect groups and vars dictionaries to make data validation failed
        """

        @staticmethod
        def get_groups():
            return {'group1': '', 'group2': '', 'group3': ''}

        @staticmethod
        def get_vars():
            return {'var1': '', 'var2': '', 'var3': '', 'var4': ''}

        @staticmethod
        def get_data():
            return {'group1': {'group2': {'var1': 'val1',
                                          'var2': 'val2'},
                               'group3': {'not_found_var': 'val3'}},
                    'not_found_group': {'var3': 'var3'},
                    'bad key': {'var4': 'val4'}}

    def setUp(self):
        self.output = ListStream()
        sys.stdout = self.output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_validate_data(self):
        parser = self.MalformedDataParser()
        result = parser.validate_data(debug=True)

        errors = [err for err in self.output if err.strip()][1:]
        errors = [err for err in errors if "Recur" not in err and not err.startswith("Found")]

        expected_errors = {MSG.err(2, 'not_found_group'),
                           MSG.err(3, 'not_found_var'),
                           MSG.err(1),
                           MSG.err(2, 'bad key'),
                           MSG.err(16)}

        for err in errors:
            self.assertTrue(err in expected_errors, err)

        self.assertFalse(result, "Data validation supposed to fail, but succeeded")

        self.output.clear()


if __name__ == "__main__":
    unittest.main()
