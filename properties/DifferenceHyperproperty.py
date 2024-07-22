from spa import GenericThreshold, OutOfDataException
import abc
import operator
import numpy as np
from typing import Any, List, Tuple, Union

_T_NUMBER = Union[int, float]

class DifferenceHyperproperty(GenericThreshold):
    """Comparison model to compare the ratios of two execution properties. Notably, this includes speedup.
    Technically, the data may be pre-processed to take the ratio of all data points and then the property
    :class ThresholdProperty can be used. However, this class is provided as an example of a hyperproperty.
    """

    NUM_SOURCES = 2
    """The expected number of data sources for the property"""

    @staticmethod
    def start_point_estimate(data: List[List[_T_NUMBER]], proportion: float) -> float:
        # First take all the differences of the data points
        ratio_data = [x[0] - x[1] for x in zip(*data)]
        # Find the point estimate
        return np.quantile(ratio_data, 1 - proportion)

    def verify_data(self, data: List[List[_T_NUMBER]]) -> None:
        """Verify that the input data is valid for the property. Raises an exception to provide detailed error info.
        In this case, expecting two lists, each of which contains at least one integer or float.
        :param data: The data to verify.
        :raises TypeError: If the data is not a tuple or list of integers or floats of length at least 1.
        """

        correct_type = isinstance(data, list) or isinstance(data, list)
        correct_length = len(data) == self.NUM_SOURCES
        correct_data_type = all(isinstance(x, tuple) or isinstance(x, list) for x in data)

        correct_sub_length = all(len(x) >= 1 for x in data)
        correct_sub_type = all(isinstance(y, int) or isinstance(y, float) for x in data for y in x)

        if not (correct_type and correct_length and correct_data_type and correct_sub_length and correct_sub_type):
            raise TypeError(
                'Data must be a list or tuple of lists or tuples of integers or floats of length at least 1')

    def extract_value(self, data: List[List[_T_NUMBER]]):
        """Extract the value from the input data. Meant to be used in conjunction with :function check_sample_satisfy:
        For this property, return only the leftmost value in both data lists. Returns the value and the remaining data.
        :param data: The data to extract from.
        :return: The extracted value(s).
        """
        # Check if each data source has at least one value
        has_data = all(len(d) > 0 for d in data)
        if not has_data:
            raise OutOfDataException
        # Extract the leftmost value from each data source
        value = [d[0] for d in data]
        data = [d[1:] for d in data]
        return value, data

    def check_sample_satisfy(self, value):
        """Check if the property is satisfied or not satisfied by the given value. Meant to be used with the
        :function extract_value: method.
        In this case, the property is satisfied if the value comparison against the threshold is True.
        :param value: The value(s) to check.
        :return: True if the property is satisfied, False otherwise.
        """
        if not (isinstance(self.threshold, int) or isinstance(self.threshold, float)):
            raise TypeError('Threshold must be an integer or float')
        # Difference is the first data source minus the second
        difference = value[0] - value[1]
        return self._comparison(difference, self.threshold)
