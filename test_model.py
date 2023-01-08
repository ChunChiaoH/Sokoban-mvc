import unittest
import model

class TestRoom(unittest.TestCase):

    @staticmethod
    def basic_room():
        room = model.Room(5, 3)
        room.set_playground(['+++',
                             'C +',
                             '+G+',
                             '+0+',
                             '+++'])
        return room

    def test_get_dimension(self):
        self.assertEqual((5, 3), self.basic_room().get_dimension(), 'Room dimension incorrect')

    def test_get_cat_start(self):
        self.assertEqual((1, 0), self.basic_room().get_cat_start(), 'Cat initial position incorrect')

    def test_get_glasses(self):
        keys = [key for key in self.basic_room().get_glasses()]
        self.assertEqual([(2, 1)], keys)

    def test_get_tiles(self):
        tiles = self.basic_room().get_tiles()
        self.assertEqual(type(model.Wall()), type(tiles[0][1]), 'Get tiles incorrect, Wall')
        self.assertEqual(type(model.Empty()), type(tiles[1][0]), 'Get tiles incorrect, Empty')
        self.assertEqual(type(model.Dest()), type(tiles[3][1]), 'Get tiles incorrect, Dest')

    def test_get_tile(self):
        self.assertEqual(type(model.Wall()), type(self.basic_room().get_tile(2, 0)), 'Get tile incorrect, Wall')
        self.assertEqual(type(model.Empty()), type(self.basic_room().get_tile(1, 1)), 'Get tile incorrect, Empty')
        self.assertEqual(type(model.Dest()), type(self.basic_room().get_tile(3, 1)), 'Get tile incorrect, Dest')

    def test_move_glass(self):
        room = self.basic_room()
        room.move_glass(room.get_glass(2, 1), (1, 0))
        self.assertIn((3, 1), room.get_glasses())
        self.assertNotIn((2, 1), room.get_glasses())