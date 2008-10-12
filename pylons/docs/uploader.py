import cPickle
import mimetypes
import os
from os import path

import httplib2
import simplejson

HERE_DIR = path.dirname(path.abspath(__file__))
BUILD_DIR = path.join(HERE_DIR, '_build')

post_uri = 'http://localhost:5000/docs/upload'
image_uri = 'http://localhost:5000/docs/upload_image'



def scan_dir(parent, directory):
    files = []
    for name in os.listdir(directory):
        full_name = path.join(directory, name)
        if name in ['_sources', '_static']:
            continue
        if path.isdir(full_name):
            new_parent = parent + '/' + name
            files.extend(scan_dir(new_parent, full_name))
        else:
            if name.endswith('.fpickle') or name.endswith('.pickle'):
                data = cPickle.load(open(full_name, 'r'))
                files.append(
                    ('/'.join([parent, name]), data)
                )
    return files

def scan_images(directory):
    files = []
    for name in os.listdir(directory):
        if name[-4:] in ['.png', '.jpg', 'gif']:
            files.append(name)
    return files

files = scan_dir('', path.join(BUILD_DIR, 'web'))
http = http = httplib2.Http(timeout=10)

basedata = {}
# Find the metadata about versions and such
for filename, filedoc in files:
    if 'globalcontext.pickle' in filename:
        basedata['version'] = filedoc['version']
        basedata['project'] = filedoc['project']
        basedata['shorttitle'] = filedoc['shorttitle']

headers = {}
headers.setdefault('Accept', 'application/json')
headers.setdefault('User-Agent', 'Doc Uploader')
headers.setdefault('Content-Type', 'application/json')

for filename, filedoc in files:
    if not isinstance(filedoc, dict):
        continue
    filedoc['filename'] = filename
    filedoc.update(basedata)
    content = simplejson.dumps(filedoc, ensure_ascii=False).encode('utf-8')
    
    resp, data = http.request(post_uri, 'POST', body=content, headers=headers)
    status_code = int(resp.status)
    if status_code == 200:
        print "Uploaded %s" % filename
    else:
        print "FAILED: %s" % filename

for filename in scan_images(path.join(BUILD_DIR, 'web', '_images')):
    headers['Content-Type'] = mimetypes.guess_type(filename)
    file_content = open(path.join(BUILD_DIR, 'web', '_images', filename), 'r').read()
    resp, data = http.request(image_uri + '?version=%s&project=%s&name=%s' %
                              (basedata['version'], basedata['project'], filename),
                              body=file_content, headers=headers)
    status_code = int(resp.status)
    if status_code == 200:
        print "Uploaded %s" % filename
    else:
        print "FAILED: %s" % filename
