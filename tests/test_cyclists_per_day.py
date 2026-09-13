#!/usr/bin/env python3

import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from src.cyclists_per_day import cyclists_per_day, main


class TestCyclistsPerDay(unittest.TestCase):

    def setUp(self):
        self.df = cyclists_per_day()

    def test_shape(self):
        self.assertEqual(
            self.df.shape,
            (1547, 20),
            msg="cyclists_per_day() returned a DataFrame of shape %r, "
            "expected (1547, 20). The index should combine (Year, Month) "
            "over the whole dataset, with one column per counting station."
            % (self.df.shape,),
        )

    def test_columns(self):
        cols = [
            'Auroransilta', 'Eteläesplanadi',
            'Huopalahti (asema)', 'Kaisaniemi/Eläintarhanlahti', 'Kaivokatu',
            'Kulosaaren silta et.', 'Kulosaaren silta po. ', 'Kuusisaarentie',
            'Käpylä, Pohjoisbaana', 'Lauttasaaren silta eteläpuoli',
            'Merikannontie', 'Munkkiniemen silta eteläpuoli',
            'Munkkiniemi silta pohjoispuoli', 'Heperian puisto/Ooppera',
            'Pitkäsilta itäpuoli', 'Pitkäsilta länsipuoli',
            'Lauttasaaren silta pohjoispuoli', 'Ratapihantie', 'Viikintie',
            'Baana',
        ]
        self.assertCountEqual(
            self.df.columns,
            cols,
            msg="cyclists_per_day() columns %r do not match the expected "
            "counting-station columns %r." % (list(self.df.columns), cols),
        )

    def test_main_plots_the_result(self):
        with patch(
            "src.cyclists_per_day.cyclists_per_day", wraps=cyclists_per_day
        ) as pcpd, patch.object(
            pd.core.frame.DataFrame, "plot", new=MagicMock(name="plot")
        ) as plot_method, patch(
            "src.cyclists_per_day.plt.plot"
        ) as pplot, patch(
            "src.cyclists_per_day.plt.show"
        ) as pshow:
            main()
            pcpd.assert_called_once_with()
            func_called = pplot.call_count == 1
            method_called = plot_method.call_count == 1
            self.assertTrue(
                func_called or method_called,
                msg="main() must display the data by calling either "
                "plt.plot(...) or the .plot(...) method of a DataFrame.",
            )
            pshow.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
