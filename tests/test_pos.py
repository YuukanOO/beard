import base_test
import unittest
import pos

class TestPosModule(base_test.RequireTokens):

    def test_find_child(self):
        val_to_pos = {}

        child_pos = pos._find_child('Ver:Pres', val_to_pos)

        self.assertEqual(child_pos.value, 'Pres')
        self.assertEqual(child_pos.parent, 'Ver')

        child_pos = pos._find_child('Some:Separated:Val', val_to_pos)
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

        leaves = pos._get_leaves(values)
        self.assertEqual(len(leaves), 4)
        self.assertListEqual(sorted(leaves), ['Value 0', 'Value 1', 'Value 2', 'Value 3'])

    def test_create_from_tokens(self):

        data = pos.create_from_tokens(self.tokens_01)

        w = data.get('words', {})
        p = data.get('parts_of_speech', {})

        self.assertTrue(w)
        self.assertTrue(p)

        self.assertEqual(len(w), 14)
        self.assertEqual(len(p), 7) # Don't forget the None Pos (start of paragraph)
