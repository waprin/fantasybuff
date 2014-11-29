__author__ = 'bill'

import unittest
import logging

logger = logging.getLogger(__name__)
from teams.utils.league_files import choose_league_directory


class UtilsTest(unittest.TestCase):
    def test_choose_league_directory(self):
        logger.info('test_choose_directory(): begin() ... ')
        league1 = 'league_000_2012_12'
        league2 = 'league_001_2012_11'

        listings = ['something', '..', '.', league1, league2]
        d = choose_league_directory(listings)
        self.assertEquals(d, league2)

        d = choose_league_directory([])
        self.assertEqual(d, None)

        l1 = 'league_000_2012_12_24_00_57_16'
        # l2 = 'league_001_2012_12_24_00_57_16'
        l3 = 'league_000_2012_12_24_00_58_05'
        l4 = 'league_001_2012_12_24_00_58_05'
        l5 = 'league_000_2012_12_24_00_58_53'
        #l6 = 'league_001_2012_12_24_00_58_53'
        listings = [l1, l3, l4, l5]
        d = choose_league_directory(listings)
        self.assertEquals(d, l4)
