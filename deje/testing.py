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
identities = {
    "mitzi":("mitzi@lackadaisy.com", ["rsa","-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQDAZQNip0GPxFZsyxcgIgyvuPTHsruu66DBsESG5/Pfbcye3g4W\nwfg+dBP3IfUnLB4QXGzK42BAd57fCBXOtalSOkFoze/C2q74gYFBMvIPbEfef8yQ\n83uoNkYAFBVp6yNlT51IQ2mY19KpqoyxMZftxwdtImthE5UG1knZE64sIwIDAQAB\nAoGAIGjjyRqj0LQiWvFbU+5odLGTipBxTWYkDnzDDnbEfj7g2WJOvUavqtWjB16R\nDahA6ECpkwP6kuGTwb567fdsLkLApwwqAtpjcu96lJpbRC1nq1zZjwNB+ywssqfV\nV3R2/rgIEE6hsWS1wBHufJeqBZtlkeUp/VEx/uopyuR/WgECQQDJOaFSutj1q1dt\nNO23Q6w3Ie4uMQ59rWeRxXA5+KjDZCxrizzo/Bew5ZysJzHB2n8QQ15WJ7gTSjwJ\nMQdl/7SJAkEA9MQG/6JivkhUNh45xMYqnMHuutyIeGE17QndSfknU+8CX9UBLjsL\nw1QU+llJ3iYfMPEDaydn0HJ8+iinyyAISwJAe7Z2vEorwT5KTdXQoG92nZ66tKNs\naVAG8NQWH04FU7tuo9/C3uq+Ff/UxvKB4NDYdcM1aHqa7SEir/P4vHjtIQJAFKc9\n1/BB2MCNqoteYIZALj4HAOl+8nlxbXD5pTZK5UAzuRZmJRqCYZcEtiM2onIhC6Yq\nna4Tink+pnUrw24OhQJBAIjujQS5qwOf2p5yOqU3UYsBv7PS8IitmYFARTlcYh1G\nrmcIPHRtkxIwNuFxy3ZRRPEDGFa82id5QHUJT8sJbqY=\n-----END RSA PRIVATE KEY-----"], ['local', None, 'mitzi']),
    "atlas":("atlas@lackadaisy.com", ["rsa","-----BEGIN RSA PRIVATE KEY-----\nMIICXgIBAAKBgQCvCM8MTSOSeA8G62b9Fg2Ic18JoHoswqn7kmU+qmYxJnTd0rSS\nYaQWiSflchTBgGcbItR4jsktYifOSfp7Cl1k5IHXqGKLHtIt8Fo02k/ajR5DzGJN\n2yAJfbBCi43ifOaVKwjuJqcFKhuPUqNJecFn8m62QOQehrIlUAlnnM7OXQIDAQAB\nAoGBAJGrVRU5xZcKUAdENkv+5Hhg/AE5CzThNTJnXddPXQkepjhOOXVxyWvv7cIo\ntVltEWImFInY21jnzZUDQHDR6XLCe8B3LRlOWrkv7+byesIFkNH9C7uvheD5xxiG\nzPpOkpwcms3QW+/FmhN5Wia+4oeHB4J9uAjJmNoaddfqAhWBAkEAwdEjMzJaKIx5\n6OIyYAEnC6lvVI6Qx/ssKQH7GhaItxzLZRaIaK4XUgrL5q1OHNNCCFgREw7nhyu3\nZnt8v833rQJBAOcw/wQ0iQktluqKoT4i73hRkGk7MTB2Y/4e2YTVnypUtQC+jxs1\nND3CJj59oJojfA3SJg0M0pWXcMKIIhRxx3ECQQCVl6zafBeYSmxhsgx9iwYu+xSh\np/PZVmTMNeowRYo6AvB90nlwikYXnZupLMQofWnu9MIg+pT7AGPqpo8vn3J1AkAU\nowEAhRf+Y71m7jz6aO/rU4yKeCgp5UeDtYlBHDh69Ni7Wkc37IXfRWdYiKo/WA+I\nxEt1OsHJbJ06ICC6pnVhAkEAio1qXj8vLi9t9xocRe8LIthaYBslw4B8yY69fRhd\nuQifuvld7xjeXsfCWRmA4t72SmcAyzMaG5wnqhLNeCXXYw==\n-----END RSA PRIVATE KEY-----"], ['local', None, 'atlas']),
}

def identity(name="mitzi"):
    from identity import Identity
    return Identity(*identities[name])

def checkpoint(doc = None):
    from checkpoint import Checkpoint
    if not doc:
        doc = document()
    return Checkpoint(doc, {'x':'y'}, 0, 'mick-and-bandit')

def handler_lua(source):
    return document(handler_lua = source)

def document(handler_lua = None, handler_lua_template = None):
    from document import Document
    from resource import Resource
    doc = Document()
    if handler_lua_template:
        import deje.handlers.lua as handlers
        handler_lua = getattr(handlers, handler_lua_template)()
    if handler_lua:
        handler = Resource('/handler.lua', handler_lua, 'The primary handler', 'text/lua')
        doc.add_resource(handler)
    return doc

def quorum():
    doc = document(handler_lua_template="echo_chamber")
    cp  = checkpoint(doc)
    return cp.quorum

def owner():
    from owner import Owner
    return Owner(identity(), make_jack=False)
