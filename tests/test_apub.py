import unittest


class TestApub(unittest.TestCase):
    def test_all(self):
        """Test that __all__ contains only names that are actually exported.
        """
        import apub

        missing = list(set(name for name in apub.__all__
                           if getattr(apub, name, None) is None))

        self.assertFalse(
            missing,
            msg="__all__ contains unresolved names: {0}"
                .format(", ".join(missing), ))
