import sys
import types
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = PROJECT_ROOT / "MusicTager"
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from song_metadata.metadata_type import SongSearchInfo


SEARCH_KEYWORD = "Yound and beautiful"


def load_module(module_name, module_path):
    spec = spec_from_file_location(module_name, module_path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


api_package = types.ModuleType("api")
api_package.__path__ = [str(PACKAGE_ROOT / "api")]
sys.modules.setdefault("api", api_package)

api_error = load_module("api.api_error", PACKAGE_ROOT / "api" / "api_error.py")
sys.modules["api.api_error"] = api_error

cloud_api = load_module("cloud_api_under_test", PACKAGE_ROOT / "api" / "cloud_api.py")
kugou_api = load_module("kugou_api_under_test", PACKAGE_ROOT / "api" / "kugou_api.py")

NoneResultError = api_error.NoneResultError
CloudMusicWebApi = cloud_api.CloudMusicWebApi
KugouApi = kugou_api.KugouApi


class MusicApiSearchTest(unittest.TestCase):
    def assert_valid_search_results(self, api_name, results):
        self.assertIsInstance(results, list)
        if not results:
            self.skipTest(f"{api_name} returned no results for {SEARCH_KEYWORD!r}")

        first = results[0]
        self.assertIsInstance(first, SongSearchInfo)
        self.assertTrue(first.songName)
        self.assertTrue(first.singer)
        self.assertRegex(first.duration, r"^\d+:\d{2}$")
        self.assertTrue(first.idOrMd5)

        combined_text = " ".join(
            f"{item.songName} {item.singer}".lower() for item in results
        )
        self.assertIn("beautiful", combined_text)

    def test_cloud_music_search_yound_and_beautiful(self):
        api = CloudMusicWebApi()

        try:
            results = api.search_data(SEARCH_KEYWORD)
        except NoneResultError:
            self.fail(f"CloudMusicWebApi returned no results for {SEARCH_KEYWORD!r}")

        self.assert_valid_search_results("CloudMusicWebApi", results)

    def test_kugou_search_yound_and_beautiful(self):
        api = KugouApi()

        try:
            results = api.search_hash(SEARCH_KEYWORD)
        except NoneResultError:
            self.fail(f"KugouApi returned no results for {SEARCH_KEYWORD!r}")

        self.assert_valid_search_results("KugouApi", results)


if __name__ == "__main__":
    unittest.main()
