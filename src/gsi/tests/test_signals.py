from django.test import TestCase

from ..models import Tile, Area

class GsiSignalsTests(TestCase):
    def setUp(self):
        tile_1 = Tile.objects.get_or_create(name='tile_1')
        tile_2 = Tile.objects.get_or_create(name='tile_2')
        tile_3 = Tile.objects.get_or_create(name='tile_3')
        area_1 = Area.objects.get_or_create(name='area_1')
        area_1[0].tiles = tile_1
        area_1[0].tiles = tile_2
        area_1[0].tiles = tile_3

    def test_added_update_area_for_each_tile(self):
        '''test signal added_update_area_for_each_tile'''

        self.assertEqual(3, Tile.objects.all().count())
        self.assertEqual(4, Area.objects.all().count())

        tile, created = Tile.objects.get_or_create(name='test1')
        self.assertEqual(4, Tile.objects.all().count())
        self.assertEqual(5, Area.objects.all().count())

        self.assertEqual(tile.name, Area.objects.get(name='test1').name)

        area = Area.objects.get(name='test1')
        self.assertEqual(tile, area.tiles.get())

    def test_remove_empty_area_by_removing_tile(self):
        '''test signal remove_empty_area_by_removing_tile'''

        self.assertEqual(3, Tile.objects.all().count())
        self.assertEqual(4, Area.objects.all().count())

        tile1, created1 = Tile.objects.get_or_create(name='test1')
        tile2, created2 = Tile.objects.get_or_create(name='test2')
        self.assertEqual(5, Tile.objects.all().count())
        self.assertEqual(6, Area.objects.all().count())
        self.assertEqual(tile1.name, Area.objects.get(name='test1').name)
        self.assertEqual(tile2.name, Area.objects.get(name='test2').name)

        tile1.delete()
        self.assertEqual(4, Tile.objects.all().count())
        self.assertEqual(5, Area.objects.all().count())
        self.assertEqual(tile2.name, Area.objects.get(name='test2').name)

        tile2.delete()
        self.assertEqual(3, Tile.objects.all().count())
        self.assertEqual(4, Area.objects.all().count())

