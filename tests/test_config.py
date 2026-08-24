import unittest
from dcactivity.core.config import Config


class TestConfig(unittest.TestCase):
    def test_config_defaults(self):
        cfg = Config()
        self.assertEqual(cfg.get("update_interval"), 2)
        self.assertFalse(cfg.get("privacy_mode"))
        self.assertEqual(cfg.get("idle_timeout"), 180)
        self.assertIn("clear", cfg.get("ignored_commands"))


if __name__ == "__main__":
    unittest.main()
