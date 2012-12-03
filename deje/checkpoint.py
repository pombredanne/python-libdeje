'''
This file is part of python-libdeje.

python-libdeje is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

python-libdeje is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with python-libdeje.  If not, see <http://www.gnu.org/licenses/>.
'''

import quorum

class Checkpoint(object):
    def __init__(self, document, content, version, author = None, signatures = {}):
        '''
        >>> import testing
        >>> cp = testing.checkpoint()
        >>> ident = testing.identity()
        >>> sig = cp.make_signature(ident)
        >>> cp.verify_signature(ident, sig)
        True
        >>> cp.make_signature("some string")
        Traceback (most recent call last):
        ValueError: Identity lookups not available at this time.
        >>> cp.verify_signature("some string", sig)
        Traceback (most recent call last):
        ValueError: Identity lookups not available at this time.
        >>> cp.sign(ident)
        >>> cp.verify_signature(ident, cp.signatures[ident.name])
        True
        >>> cp.sign("anonymous")
        Traceback (most recent call last):
        ValueError: No signature provided, and could not derive from identity 'anonymous'
        '''
        self.document = document
        self.content  = content
        self.version  = int(version)
        self.author   = author
        self.quorum   = quorum.Quorum(
                            self.document, 
                            [self.content, self.version, self.author],
                            signatures = signatures,
                        )
    def enact(self):
        self.document.animus.on_checkpoint_achieve(self.content, self.author)

    def test(self):
        return self.document.animus.checkpoint_test(self.content, self.author)

    def hash(self):
        '''
        >>> import testing
        >>> testing.checkpoint().hash()
        '960341d14e3531a50770bd6529a422d2b4997ae9'
        '''
        return self.quorum.hash
