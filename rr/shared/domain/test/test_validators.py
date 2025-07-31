import unittest
import pytest
from rest_framework.serializers import Serializer
from src.shared.domain.validators import DRFValidator, ValidatorRules
from src.shared.domain.exceptions import ValidationException
from unittest import mock


class TestValidatorRules(unittest.TestCase):

    def test_values_method(self):
        validator = ValidatorRules.validate("abc", "field")
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, "abc")
        self.assertEqual(validator.key, "field")

    def test_required_rule(self):
        invalid_values = [
            {'value': None, 'key': 'field1'},
            {'value': '', 'key': 'field2'},
        ]
        for i in invalid_values:
            with self.assertRaises(ValidationException) as assert_error:
                self.assertIsInstance(
                    ValidatorRules.validate(i['value'], i['key']).required(),
                    ValidatorRules
                )
            self.assertEqual(
                f'The field {i["key"]} is required', assert_error.exception.args[0])
        # válido
        valid_values = ["abc", 123, False]
        for v in valid_values:
            self.assertIsInstance(ValidatorRules.validate(
                v, "field").required(), ValidatorRules)

    def test_string_rule(self):
        invalid_values = [123, 1.2, True, []]
        for v in invalid_values:
            with self.assertRaises(ValidationException) as assert_error:
                self.assertIsInstance(
                    ValidatorRules.validate(v, "field1").string(),
                    ValidatorRules
                )
            self.assertEqual("The field field1 must be a string",
                             assert_error.exception.args[0])
        # válido
        self.assertIsInstance(ValidatorRules.validate(
            "abc", "field").string(), ValidatorRules)

    def test_number_rule(self):
        invalid_values = ["abc", True, []]
        for v in invalid_values:
            with self.assertRaises(ValidationException) as assert_error:
                self.assertIsInstance(
                    ValidatorRules.validate(v, "field1").number(),
                    ValidatorRules
                )
            self.assertEqual("The field field1 must be a number",
                             assert_error.exception.args[0])
        # válido
        for v in [123, 1.2]:
            self.assertIsInstance(ValidatorRules.validate(
                v, "field").number(), ValidatorRules)

    def test_boolean_rule(self):
        invalid_values = [1, 0, "true", None, []]
        for v in invalid_values:
            with self.assertRaises(ValidationException) as assert_error:
                self.assertIsInstance(
                    ValidatorRules.validate(v, "field3").boolean(),
                    ValidatorRules
                )
            self.assertEqual("The field field3 must be a boolean",
                             assert_error.exception.args[0])
        # válido
        for v in [True, False]:
            self.assertIsInstance(ValidatorRules.validate(
                v, "field").boolean(), ValidatorRules)

    def test_max_length_rule(self):
        invalid = {"value": "abcdef", "max": 5}
        with self.assertRaises(ValidationException) as assert_error:
            self.assertIsInstance(
                ValidatorRules.validate(
                    invalid["value"], "field4").max_length(invalid["max"]),
                ValidatorRules
            )
        self.assertEqual(
            "The field field4 must be less than 5 characters", assert_error.exception.args[0])
        # válido
        for v in ["abc", "abcde"]:
            self.assertIsInstance(ValidatorRules.validate(
                v, "field").max_length(5), ValidatorRules)

    def test_min_length_rule(self):
        invalid = {"value": "abc", "min": 5}
        with self.assertRaises(ValidationException) as assert_error:
            self.assertIsInstance(
                ValidatorRules.validate(
                    invalid["value"], "field5").min_length(invalid["min"]),
                ValidatorRules
            )
        self.assertEqual(
            "The field field5 must be at least 5 characters", assert_error.exception.args[0])
        # válido
        for v in ["abcde", "abcdef"]:
            self.assertIsInstance(ValidatorRules.validate(
                v, "field").min_length(5), ValidatorRules)


class TestDRFValidator(unittest.TestCase):

    @mock.patch.object(Serializer, 'is_valid', return_value=True)
    @mock.patch.object(
        Serializer,
        'validated_data',
        return_value={'field': ['some error']},
        new_callable=mock.PropertyMock
    )
    def test_if_validated_data_is_set(self, mock_is_valid: mock.MagicMock, mock_validated_data: mock.PropertyMock):

        validator = DRFValidator()

        is_valid = validator.validate(Serializer())
        self.assertTrue(is_valid)
        self.assertEqual(validator.validated_data, {'field': ['some error']})
        mock_is_valid.assert_called()
      


    @mock.patch.object(Serializer, 'is_valid', return_value=False)
    @mock.patch.object(
        Serializer,
        'errors',
        return_value={'field': ['some error']},
        new_callable=mock.PropertyMock
    )
    def test_if_errors_is_set(self, mock_is_valid: mock.MagicMock, mock_errors: mock.PropertyMock):

        validator = DRFValidator()

        is_valid = validator.validate(Serializer())
        self.assertFalse(is_valid)
        self.assertEqual(validator.errors, {'field': ['some error']})
        mock_is_valid.assert_called()
      
