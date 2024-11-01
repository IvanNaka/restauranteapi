# myapp/test_runner.py
from django.test.runner import DiscoverRunner

class CustomTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        return super().run_tests(test_labels, **kwargs)