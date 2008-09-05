.. _unicode:

=====================
Understanding Unicode 
===================== 

If you've ever come across text in a foreign language that contains lots of ``????`` characters or have written some Python code and received a message such as ``UnicodeDecodeError: 'ascii' codec can't decode byte 0xff in position 6: ordinal not in range(128)`` then you have run into a problem with character sets, encodings, Unicode and the like. 

The truth is that many developers are put off by Unicode because most of the time it is possible to muddle through rather than take the time to learn the basics. To make the problem worse if you have a system that manages to fudge the issues and just about work and then start trying to do things properly with
Unicode it often highlights problems in other parts of your code. 

The good news is that Python has great Unicode support, so the rest of 
this article will show you how to correctly use Unicode in Pylons to avoid 
unwanted ``?`` characters and ``UnicodeDecodeErrors``. 

What is Unicode? 
---------------- 

When computers were first being used the characters that were most important 
were unaccented English letters. Each of these letters could be represented by 
a number between 32 and 127 and thus was born ASCII, a character set where 
space was 32, the letter "A" was 65 and everything could be stored in 7 bits. 

Most computers in those days were using 8-bit bytes so people quickly realized 
that they could use the codes 128-255 for their own purposes. Different people 
used the codes 128-255 to represent different characters and before long these 
different sets of characters were also standardized into *code pages*. This 
meant that if you needed some non-ASCII characters in a document you could also
specify a codepage which would define which extra characters were available. 
For example Israel DOS used a code page called 862, while Greek users used 737.
This just about worked for Western languages provided you didn't want to write 
an Israeli document with Greek characters but it didn't work at all for Asian 
languages where there are many more characters than can be represented in 8 
bits. 

Unicode is a character set that solves these problems by uniquely defining 
*every* character that is used anywhere in the world. Rather than defining a 
character as a particular combination of bits in the way ASCII does, each 
character is assigned a *code point*. For example the word ``hello`` is made 
from code points ``U+0048 U+0065 U+006C U+006C U+006F``. The full list of code 
points can be found at http://www.unicode.org/charts/. 

There are lots of different ways of encoding Unicode code points into bits but 
the most popular encoding is UTF-8. Using UTF-8, every code point from 0-127 is
stored in a single byte. Only code points 128 and above are stored using 2, 3, 
in fact, up to 6 bytes. This has the useful side effect that English text looks
exactly the same in UTF-8 as it did in ASCII, because for every 
ASCII character with hexadecimal value 0xXY, the corresponding Unicode 
code point is U+00XY. This backwards compatibility is why if you are developing
an application that is only used by English speakers you can often get away 
without handling characters properly and still expect things to work most of 
the time. Of course, if you use a different encoding such as UTF-16 this 
doesn't apply since none of the code points are encoded to 8 bits. 

The important things to note from the discussion so far are that: 

* Unicode can represent pretty much any character in any writing system in widespread use today 
* Unicode uses code points to represent characters and the way these map to bits in memory depends on the encoding 
* The most popular encoding is UTF-8 which has several convenient properties
    1. It can handle any Unicode code point 
    2. A Unicode string is turned into a string of bytes containing no embedded  zero bytes. This avoids byte-ordering issues, and means UTF-8 strings can be  processed by C functions such as strcpy() and sent through protocols that can't handle zero bytes 
    3. A string of ASCII text is also valid UTF-8 text 
    4. UTF-8 is fairly compact; the majority of code points are turned into two  bytes, and values less than 128 occupy only a single byte. 
    5. If bytes are corrupted or lost, it's possible to determine the start of  the next UTF-8-encoded code point and resynchronize. 

.. note:: Since Unicode 3.1, some extensions have even been defined so that the defined range is now U+000000 to U+10FFFF (21 bits), and formally, the character set is defined as 31-bits to allow for future expansion. It is a myth that there are 65,536 Unicode code points and that every Unicode letter can really be squeezed into two bytes. It is also incorrect to think that UTF-8 can represent less characters than UTF-16. UTF-8 simply uses a variable number of bytes for a character, sometimes just one byte (8 bits). 

Unicode in Python 
----------------- 

In Python Unicode strings are expressed as instances of the built-in 
``unicode`` type. Under the hood, Python represents Unicode strings as either 
16 or 32 bit integers, depending on how the Python interpreter was compiled. 

The ``unicode()`` constructor has the signature ``unicode(string[, encoding, 
errors])``. All of its arguments should be 8-bit strings. The first argument is
converted to Unicode using the specified encoding; if you leave off the 
encoding argument, the ASCII encoding is used for the conversion, so characters
greater than 127 will be treated as errors: 

.. code-block:: pycon 

    >>> unicode('hello') 
    u'hello' 
    >>> s = unicode('hello') 
    >>> type(s) 
    <type 'unicode'> 
    >>> unicode('hello' + chr(255)) 
    Traceback (most recent call last): 
    File "<stdin>", line 1, in ? 
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xff in position 6: 
    ordinal not in range(128) 

The ``errors`` argument specifies what to do if the string can't be decoded to 
ascii. Legal values for this argument are ``'strict'`` (raise a 
``UnicodeDecodeError`` exception), ``'replace'`` (replace the character that 
can't be decoded with another one), or ``'ignore'`` (just leave the character 
out of the Unicode result). 

.. code-block:: pycon 

    >>> unicode('\x80abc', errors='strict') 
    Traceback (most recent call last): 
    File "<stdin>", line 1, in ? 
    UnicodeDecodeError: 'ascii' codec can't decode byte 0x80 in position 0: 
    ordinal not in range(128) 
    >>> unicode('\x80abc', errors='replace') 
    u'\ufffdabc' 
    >>> unicode('\x80abc', errors='ignore') 
    u'abc' 

It is important to understand the difference between *encoding* and *decoding*.
Unicode strings are considered to be the Unicode code points but any 
representation of the Unicode string has to be encoded to something else, for 
example UTF-8 or ASCII. So when you are converting an ASCII or UTF-8 string to 
Unicode you are *decoding* it and when you are converting from Unicode to UTF-8
or ASCII you are *encoding* it. This is why the error in the example above says
that the ASCII codec cannot decode the byte ``0x80`` from ASCII to Unicode 
because it is not in the range(128) or 0-127. In fact ``0x80`` is hex for 128 
which the first number outside the ASCII range. However if we tell Python that 
the character ``0x80`` is encoded with the ``'latin-1'``, ``'iso_8859_1'`` or 
``'8859'`` character sets (which incidentally are different names for the same 
thing) we get the result we expected: 

.. code-block:: pycon 

    >>> unicode('\x80', encoding='latin-1') 
    u'\x80' 

.. note:: 

    The character encodings Python supports are listed at http://docs.python.org/lib/standard-encodings.html 

Unicode objects in Python have most of the same methods that normal Python 
strings provide. Python will try to use the ``'ascii'`` codec to convert 
strings to Unicode if you do an operation on both types: 

.. code-block:: pycon 

    >>> a = 'hello' 
    >>> b = unicode(' world!') 
    >>> print a + b 
    u'hello world!' 

You can encode a Unicode string using a particular encoding like this: 

.. code-block:: pycon 

    >>> u'Hello World!'.encode('utf-8') 
    'Hello World!' 

Unicode Literals in Python Source Code 
-------------------------------------- 

In Python source code, Unicode literals are written as strings prefixed with 
the 'u' or 'U' character: 

.. code-block:: pycon 

    >>> u'abcdefghijk' 
    >>> U'lmnopqrstuv' 

You can also use ``"``, ``"""``` or ``'''`` versions too. For example: 

.. code-block:: pycon 

    >>> u"""This 
    ... is a really long 
    ... Unicode string""" 

Specific code points can be written using the ``\u`` escape sequence, which is 
followed by four hex digits giving the code point. If you use ``\U`` instead 
you specify 8 hex digits instead of 4. Unicode literals can also use the same 
escape sequences as 8-bit strings, including ``\x``, but ``\x`` only takes two 
hex digits so it can't express all the available code points. You can add 
characters to Unicode strings using the ``unichr()`` built-in function and find
out what the ordinal is with ``ord()``. 

Here is an example demonstrating the different alternatives: 

.. code-block:: pycon 

    >>> s = u"\x66\u0072\u0061\U0000006e" + unichr(231) + u"ais" 
    >>> # ^^^^ two-digit hex escape 
    >>> # ^^^^^^ four-digit Unicode escape 
    >>> # ^^^^^^^^^^ eight-digit Unicode escape 
    >>> for c in s: print ord(c), 
    ... 
    97 102 114 97 110 231 97 105 115 
    >>> print s 
    français 

Using escape sequences for code points greater than 127 is fine in small doses 
but Python 2.4 and above support writing Unicode literals in any encoding as 
long as you declare the encoding being used by including a special comment as 
either the first or second line of the source file: 

.. code-block:: python 

    #!/usr/bin/env python 
    # -*- coding: latin-1 -*- 
    u = u'abcdé' 
    print ord(u[-1]) 

If you don't include such a comment, the default encoding used will be ASCII. 
Versions of Python before 2.4 were Euro-centric and assumed Latin-1 as a 
default encoding for string literals; in Python 2.4, characters greater than 
127 still work but result in a warning. For example, the following program has 
no encoding declaration: 

.. code-block:: python 

    #!/usr/bin/env python 
    u = u'abcdé' 
    print ord(u[-1]) 

When you run it with Python 2.4, it will output the following warning: 

.. code-block:: pycon 

    sys:1: DeprecationWarning: Non-ASCII character '\xe9' in file testas.py on line 2, but
     no encoding declared; see http://www.python.org/peps/pep-0263.html for details 

and then the following output: 

.. code-block:: pycon 

    233 

For real world use it is recommended that you use the UTF-8 encoding for your 
file but you must be sure that your text editor actually saves the file as 
UTF-8 otherwise the Python interpreter will try to parse UTF-8 characters but 
they will actually be stored as something else. 

.. note :: 

    Windows users who use the `SciTE <http://www.scintilla.org/SciTE.html>`_ editor can specify the encoding of their file from the menu using the  ``File->Encoding``. 

.. note :: 

    If you are working with Unicode in detail you might also be interested in the ``unicodedata`` module which can be used to find out Unicode properties  such as a character's name, category, numeric value and the like. 


Input and Output 
---------------- 

We now know how to use Unicode in Python source code but input and output can 
also be different using Unicode. Of course, some libraries natively support 
Unicode and if these libraries return Unicode objects you will not have to do 
anything special to support them. XML parsers and SQL databases frequently 
support Unicode for example. 

If you remember from the discussion earlier, Unicode data consists of code 
points. In order to send Unicode data via a socket or write it to a file you 
usually need to encode it to a series of bytes and then decode the data back to
Unicode when reading it. You can of course perform the encoding manually 
reading a byte at the time but since encodings such as UTF-8 can have variable 
numbers of bytes per character it is usually much easier to use Python's 
built-in support in the form of the ``codecs`` module. 

The codecs module includes a version of the ``open()`` function that 
returns a file-like object that assumes the file's contents are in a specified 
encoding and accepts Unicode parameters for methods such as ``.read()`` and 
``.write()``. 

The function's parameters are open(filename, mode='rb', encoding=None, 
errors='strict', buffering=1). ``mode`` can be 'r', 'w', or 'a', just like the 
corresponding parameter to the regular built-in ``open()`` function. You can 
add a ``+`` character to update the file. ``buffering`` is similar to the 
standard function's parameter. ``encoding`` is a string giving the encoding to 
use, if not specified or specified as ``None``, a regular Python file object 
that accepts 8-bit strings is returned. Otherwise, a wrapper object is 
returned, and data written to or read from the wrapper object will be converted
as needed. ``errors`` specifies the action for encoding errors and can be one 
of the usual values of ``'strict'``, ``'ignore'``, or ``'replace'`` which we 
saw right at the begining of this document when we were encoding strings in 
Python source files. 

Here is an example of how to read Unicode from a UTF-8 encoded file: 

.. code-block:: python 

    import codecs 
    f = codecs.open('unicode.txt', encoding='utf-8') 
    for line in f: 
        print repr(line) 

It's also possible to open files in update mode, allowing both reading and writing: 

.. code-block:: python 

    f = codecs.open('unicode.txt', encoding='utf-8', mode='w+') 
    f.write(u"\x66\u0072\u0061\U0000006e" + unichr(231) + u"ais") 
    f.seek(0) 
    print repr(f.readline()[:1]) 
    f.close() 

Notice that we used the ``repr()`` function to display the Unicode data. This 
is very useful because if you tried to print the Unicode data directly, Python 
would need to encode it before it could be sent the console and depending on 
which characters were present and the character set used by the console, an 
error might be raised. This is avoided if you use ``repr()``. 

The Unicode character ``U+FEFF`` is used as a byte-order mark or BOM, and is often written as the first character of a file in order to assist with auto-detection of the file's byte ordering. Some encodings, such as UTF-16, expect a BOM to be present at the start of a file, but with others such as UTF-8 it isn't necessary. 

When such an encoding is used, the BOM will be automatically written as the 
first character and will be silently dropped when the file is read. There are 
variants of these encodings, such as 'utf-16-le' and 'utf-16-be' for 
little-endian and big-endian encodings, that specify one particular byte 
ordering and don't skip the BOM. 

.. note :: 

    Some editors including SciTE will put a byte order mark (BOM) in the text 
    file when saved as UTF-8, which is strange because UTF-8 doesn't need BOMs. 

Unicode Filenames 
----------------- 

Most modern operating systems support the use of Unicode filenames. The 
filenames are transparently converted to the underlying filesystem encoding. 
The type of encoding depends on the operating system. 

On Windows 9x, the encoding is ``mbcs``. 

On Mac OS X, the encoding is ``utf-8``. 

On Unix, the encoding is the user's preference according to the 
result of nl_langinfo(CODESET), or None if the nl_langinfo(CODESET) failed. 

On Windows NT+, file names are Unicode natively, so no conversion is performed.
getfilesystemencoding still returns ``mbcs``, as this is the encoding that 
applications should use when they explicitly want to convert Unicode strings to
byte strings that are equivalent when used as file names. 

``mbcs`` is a special encoding for Windows that effectively means "use 
whichever encoding is appropriate". In Python 2.3 and above you can find out 
the system encoding with ``sys.getfilesystemencoding()``. 

Most file and directory functions and methods support Unicode. For example: 

.. code-block:: python 

    filename = u"\x66\u0072\u0061\U0000006e" + unichr(231) + u"ais" 
    f = open(filename, 'w') 
    f.write('Some data\n') 
    f.close() 

Other functions such as ``os.listdir()`` will return Unicode if you pass a 
Unicode argument and will try to return strings if you pass an ordinary 8 bit 
string. For example running this example as ``test.py``: 

.. code-block:: python 

    filename = u"Sample " + unichar(5000) 
    f = open(filename, 'w') 
    f.close() 

    import os 
    print os.listdir('.') 
    print os.listdir(u'.') 

will produce the following output: 

.. code-block:: python 

    ['Sample?', 'test.py'] 
    [u'Sample\u1388', u'test.py'] 

Applying this to Web Programming 
================================ 

So far we've seen how to use encoding in source files and seen how to decode 
text to Unicode and encode it back to text. We've also seen that Unicode 
objects can be manipulated in similar ways to strings and we've seen how to 
perform input and output operations on files. Next we are going to look at how 
best to use Unicode in a web app. 

The main rule is this: 

**Your application should use Unicode for all strings internally, decoding any 
input to Unicode as soon as it enters the application and encoding the Unicode 
to UTF-8 or another encoding only on output.** 

If you fail to do this you will find that ``UnicodeDecodeError`` s will start 
popping up in unexpected places when Unicode strings are used with normal 8-bit
strings because Python's default encoding is ASCII and it will try to decode 
the text to ASCII and fail. It is always better to do any encoding or decoding 
at the edges of your application otherwise you will end up patching lots of 
different parts of your application unnecessarily as and when errors pop up. 

Unless you have a very good reason not to it is wise to use UTF-8 as the 
default encoding since it is so widely supported. 

The second rule is: 

**Always test your application with characters above 127 and above 255 wherever
possible.** 

If you fail to do this you might think your application is working fine, but as
soon as your users do put in non-ASCII characters you will have problems. 
Using arabic is always a good test and www.google.ae is a good source of sample
text. 

The third rule is: 

**Always do any checking of a string for illegal characters once it's in the 
form that will be used or stored, otherwise the illegal characters might be 
disguised.** 

For example, let's say you have a content management system that takes a 
Unicode filename, and you want to disallow paths with a '/' character. You 
might write this code: 

.. code-block:: python 

    def read_file(filename, encoding): 
        if '/' in filename: 
            raise ValueError("'/' not allowed in filenames") 
        unicode_name = filename.decode(encoding) 
        f = open(unicode_name, 'r') 
        # ... return contents of file ... 

This is INCORRECT. If an attacker could specify the 'base64' encoding, they 
could pass ``L2V0Yy9wYXNzd2Q=`` which is the base-64 encoded form of the string
``'/etc/passwd'`` which is a file you clearly don't want an attacker to get 
hold of. The above code looks for ``/`` characters in the encoded form and 
misses the dangerous character in the resulting decoded form. 

Those are the three basic rules so now we will look at some of the places you 
might want to perform Unicode decoding in a Pylons application. 

Request Parameters 
------------------ 

Pylons automatically coerces incoming form parameters (``request.POST``, ``GET`` (quote GET) and ``params``) into unicode objects (as of Pylons 0.9.6). 

The request object contains a ``charset`` (encoding) attribute defining what the parameters should be decoded to (via value.decode(charset, errors)), and the decoding ``errors`` handler. 

The unicode conversion of parameters can be disabled when ``charset`` is set to
None. 

.. code-block:: python 

    def index(self): 
        #request.charset = 'utf-8' # utf-8 is the default charset 
        #request.errors = 'replace' # replace is the default error handler 
        # a MultiDict-like object of string names and unicode values 
        decoded_get = request.GET 

        # The raw data is always still available when charset is None 
        request.charset = None 
        raw_get = request.GET 
        raw_params = request.params 

Pylons can also be configured to not coerece parameters to unicode objects by 
default. This is done by setting the following in the Pylons config object (at 
the bottom of your project's ``config/environment.py``): 

.. code-block:: python 

    # Don't coerce parameters to unicode 
    config['pylons.request_options']['charset'] = None 
    # You can also change the default error handler 
    #config['pylons.request_options']['errors'] = 'strict' 

When the ``request`` object is instructed to always automatically decode to 
unicode via the ``request_settings`` dictionary, the dictionary's ``charset`` 
value acts as a fallback charset. If a ``charset`` was sent by the browser (via
the ``Content-Type`` header), the browser's value will take precedent: this 
takes place when the ``request`` object is constructed. 

``FieldStorage`` (file upload) objects will be handled specially for unicode 
parameters: what's provided is a copy of the original ``FieldStorage`` object 
with a unicode version of its ``filename`` attribute. 

See :ref:`file_uploads` for more information on working with file uploads/``FieldStorage`` objects. 

.. note:: 

    Only parameter values (not their associated names) are decoded to unicode 
    by default. Since parameter names commonly map directly to Python variable 
    names (which are restricted to the ASCII character set), it's usually 
    preferable to handle them as strings. For example, passing form parameters 
    to a function as keyword arguments (e.g. \*\*request.params.mixed()) 
    doesn't work with unicode keys. 

    To make ``WSGIRequest`` decode parameter names anyway, enable the 
    ``decode_param_names`` option on either the WSGIRequest object or the 
    ``request_settings`` dictionary. ``FieldStorage's`` ``name`` attributes are 
    also decoded to unicode when this option is enabled. 

Templating 
---------- 

Pylons uses Mako as its default templating language. Mako handles all content 
as unicode internally. It only deals in raw strings upon the final rendering of
the template (the Mako ``render()`` function, used by the Pylons ``render()`` 
function/Buffet plugin). The encoding of the rendered string can be configured;
Pylons sets the default value to UTF-8. To change this value, edit your 
project's ``config/environment.py`` file and add the following option: 

.. code-block:: python 

    # Customize templating options via this variable 
    tmpl_options = config['buffet.template_options'] 

    tmpl_options['mako.output_encoding'] = 'utf-8' 

replacing ``utf-8`` with the encoding you wish to use. 

More information can be found at `Mako's Unicode Chapter  <http://www.makotemplates.org/docs/unicode.html>`_. 

Output Encoding 
--------------- 

Web pages should be generated with a specific encoding, most likely UTF-8. At 
the very least, that means you should specify the following in the ``<head>`` 
section: 

.. code-block:: html 

    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 

The charset should also be specified in the ``Content-Type`` header (which 
Pylons automatically does for you): 

.. code-block:: python 

    response.headers['Content-type'] = 'text/html; charset=utf-8' 

Pylons has a notion of ``response_options``, complimenting the 
``request_options`` mentioned in the `Request Parameters`_ section above. The 
default request charset can be changed by setting the following in the Pylons 
config object (at the bottom of your project's ``config/environment.py``): 

.. code-block:: python 

    config['pylons.response_options']['charset'] = 'utf-8' 

replacing ``utf-8`` with the charset you wish to use. 

If you specify that your output is UTF-8, generally the web browser will 
give you UTF-8. If you want the browser to submit data using a different 
character set, you can set the encoding by adding the ``accept-encoding`` 
tag to your form. Here is an example: 

.. code-block:: html 

    <form accept-encoding="US-ASCII" ...> 

However, be forewarned that if the user tries to give you non-ASCII 
text, then: 

* Firefox will translate the non-ASCII text into HTML entities. 

* IE will ignore your suggested encoding and give you UTF-8 anyway. 

The lesson to be learned is that if you output UTF-8, you had better be 
prepared to accept UTF-8 by decoding the data in ``request.params`` as 
described in the section above entitled `Request Parameters`_'. 

Another technique which is sometimes used to determine the character set is to 
use an algorithm to analyse the input and guess the encoding based on 
probabilities. 

For instance, if you get a file, and you don't know what encoding it is encoded
in, you can often rename the file with a .txt extension and then try to open it
in Firefox. Then you can use the "View->Character Encoding" menu to try to 
auto-detect the encoding. 

Databases 
--------- 

Your database driver should automatically convert from Unicode objects to a 
particular charset when writing and back again when reading. Again it is normal
to use UTF-8 which is well supported. 

You should check your database's documentation for information on how it handles Unicode. 

For example MySQL's Unicode documentation is here http://dev.mysql.com/doc/refman/5.0/en/charset-unicode.html 

Also note that you need to consider both the encoding of the database and the encoding used by the database driver. 

If you're using MySQL together with SQLAlchemy, see the following, as 
there are some bugs in MySQLdb that you'll need to work around: 

http://www.mail-archive.com/sqlalchemy@googlegroups.com/msg00366.html 

Summary 
======= 

Hopefully you now understand the history of Unicode, how to use it in Python  and where to apply Unicode encoding and decoding in a Pylons application. You  should also be able to use Unicode in your web app remembering the basic rule to use UTF-8 to talk to the world, do the encode and decode at the edge of your  application. 

Further Reading 
=============== 

This information is based partly on the following articles which can be 
consulted for further information.: 

http://www.joelonsoftware.com/articles/Unicode.html 

http://www.amk.ca/python/howto/unicode 

Please feel free to report any mistakes to the Pylons mailing list or to the 
author. Any corrections or clarifications would be gratefully received. 
