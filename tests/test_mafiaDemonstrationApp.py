from unittest import TestCase
from mafiademonstration import mafiademonstration
from kivy.uix.screenmanager import ScreenManager


class TestMafiaDemonstrationApp(TestCase):
    def test_build(self):
        test_app = mafiademonstration.MafiaDemonstrationApp()
        assert isinstance(test_app.build(), ScreenManager)

    def test_build_config(self):
        self.fail()

    def test_build_settings(self):
        self.fail()

    def test_on_config_change(self):
        self.fail()

    def test_on_pause(self):
        self.fail()

    def test_on_resume(self):
        self.fail()
