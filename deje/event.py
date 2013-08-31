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

from deje import quorum

class Event(object):
    def __init__(self, document, content, version = None, author = None, signatures = {}):
        self.document = document
        self.content  = content
        self.version  = int(version or self.document.version)
        self.author   = author
        self.enacted  = False
        self.quorum   = quorum.Quorum(
                            self,
                            signatures = signatures,
                        )
    def enact(self):
        if self.enacted:
            return
        self.enacted = True
        self.document._blockchain.append(self)
        self.document.interpreter.on_event_achieve(self.content, self.author)
        if self.owner:
            self.quorum.transmit_complete()

    def update(self):
        if self.quorum.done:
            self.enact()

    def transmit(self):
        self.owner.lock_action(self.document, {
            'type': 'deje-event',
            'version': self.version,
            'event': self.content,
            'author': self.authorname,
        })
        self.quorum.transmit()
        self.update()

    def test(self):
        return self.document.interpreter.event_test(self.content, self.author)

    @property
    def authorname(self):
        return (hasattr(self.author, "name") and self.author.name) or self.author
        
    @property
    def hashcontent(self):
        return [self.content, self.version, self.authorname]

    def hash(self):
        return self.quorum.hash

    @property
    def owner(self):
        return self.document.owner

def from_hashcontent(document, hashcontent, signatures={}):
    if type(hashcontent) != list or len(hashcontent) != 3:
        raise TypeError("event.from_hashcontent expects a list of length 3, got %r" % hashcontent)
    return Event(document, content, version, author, signatures)
