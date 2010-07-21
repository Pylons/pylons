import unittest

class Test_resolve_dotted(unittest.TestCase):
    def test_it(self):
        from pylons.util import resolve_dotted
        result = resolve_dotted('pylons.util:resolve_dotted')
        self.failUnless(result is resolve_dotted)
        
