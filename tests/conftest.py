import sys
import os
import shutil
import pkg_resources

here = os.path.dirname(__file__)
base = os.path.dirname(here)
sys.path.append(here)
sys.path.insert(0, base)

here = os.path.dirname(__file__)

pkg_resources.working_set.add_entry(base)

if not os.environ.get('PASTE_TESTING'):
    output_dir = os.path.join(here, 'test_webapps', 'output')
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

