from beard import swissknife
import unittest

class TestSwissKnife(unittest.TestCase):

    def test_find_child(self):
        val_to_pos = {}

        child_pos = swissknife.find_child('Ver:Pres', val_to_pos)

        self.assertEqual(child_pos.value, 'Pres')
        self.assertEqual(child_pos.parent, 'Ver')

        child_pos = swissknife.find_child('Some:Separated:Val', val_to_pos)
        self.assertEqual(child_pos.value, 'Val')
        self.assertEqual(child_pos.parent, 'Separated')

    def test_get_leaves(self):

        values = {
            'Root': {
                'Parent 0': {
                    '0': 'Value 0',
                    '1': 'Value 1'
                },
                'Parent 1': {
                    '2': 'Value 2',
                    '3': 'Value 3'
                }
            }
        }

        leaves = swissknife.get_leaves(values)
        self.assertEqual(len(leaves), 4)
        self.assertListEqual(sorted(leaves), ['Value 0', 'Value 1', 'Value 2', 'Value 3'])