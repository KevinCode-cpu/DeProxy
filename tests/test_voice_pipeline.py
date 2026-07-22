import importlib
import sys
import unittest


class VoicePipelineImportTest(unittest.TestCase):
    def test_voice_pipeline_imports_without_reassemblyzer(self) -> None:
        sys.modules.pop("src.pipelines.voice_pipeline", None)
        sys.modules.pop("resemblyzer", None)

        module = importlib.import_module("src.pipelines.voice_pipeline")

        self.assertTrue(hasattr(module, "get_voice_embedding"))
        self.assertTrue(hasattr(module, "voice_features_available"))


if __name__ == "__main__":
    unittest.main()
