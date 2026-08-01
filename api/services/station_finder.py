from scipy.spatial import cKDTree
from api.models import FuelStation

class StationFinder():
    _tree = None
    _stations = None

    @classmethod
    def load_tree(cls):
        if(cls._tree is None):
            all_stations = list(FuelStation.objects.all())

            coords = []
            stations = []
            for s in all_stations:
                if s.longitude is None:
                    continue
                coords.append((s.latitude,s.longitude))
                stations.append(s)

            cls._stations = stations
            cls._tree = cKDTree(coords)

        return cls._tree,cls._stations

