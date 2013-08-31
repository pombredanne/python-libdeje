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

from ejtp.util.compat  import unittest
from deje.historystate import HistoryState
from deje.resource     import Resource

class TestHistoryState(unittest.TestCase):

    def setUp(self):
        self.resource = Resource()

    def test_init(self):
        hs = HistoryState()
        self.assertEqual(hs.hash, None)
        self.assertEqual(hs.resources, {})

    def test_init_with_hash(self):
        hs = HistoryState("example")
        self.assertEqual(hs.hash, "example")
        self.assertEqual(hs.resources, {})

    def test_init_with_resources(self):
        hs = HistoryState(resources=[self.resource])
        self.assertEqual(hs.hash, None)
        self.assertEqual(hs.resources, {'/':self.resource})

    def test_init_with_both(self):
        hs = HistoryState("example", [self.resource])
        self.assertEqual(hs.hash, "example")
        self.assertEqual(hs.resources, {'/':self.resource})

    def test_add_resource(self):
        hs = HistoryState()
        hs.add_resource(self.resource)
        self.assertEqual(hs.resources, {'/':self.resource})

    def test_enact(self):
        # TODO : Hook in with event.enact
        pass

    def test_clone(self):
        hs1 = HistoryState("example", [self.resource])
        hs2 = hs1.clone()
        self.assertEqual(hs1.hash, hs2.hash)

        # Each resource compared by ref, not value
        self.assertNotEqual(hs1.resources, hs2.resources)
        self.assertEqual(hs1.serialize(), hs2.serialize())

    def test_serialize_resources(self):
        hs = HistoryState("example", [self.resource])
        self.assertEqual(hs.serialize_resources(), {
            '/' : {
                'comment': '',
                'content': '',
                'path': '/',
                'type': 'application/x-octet-stream',
            }
        })

    def test_serialize(self):
        hs = HistoryState("example", [self.resource])
        self.assertEqual(hs.serialize(), {
            "hash" : "example",
            "resources" : hs.serialize_resources(),
        })