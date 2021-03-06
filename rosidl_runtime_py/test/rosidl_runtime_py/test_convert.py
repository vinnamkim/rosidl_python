# Copyright 2017-2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import OrderedDict

from rosidl_runtime_py import message_to_csv
from rosidl_runtime_py import message_to_ordereddict
from rosidl_runtime_py import message_to_yaml
from rosidl_runtime_py.convert import _convert_value

from test_msgs import message_fixtures


def test_primitives():
    # Smoke-test the formatters on a bunch of messages
    msgs = []
    msgs.extend(message_fixtures.get_msg_arrays())
    msgs.extend(message_fixtures.get_msg_basic_types())
    msgs.extend(message_fixtures.get_msg_bounded_sequences())
    msgs.extend(message_fixtures.get_msg_builtins())
    msgs.extend(message_fixtures.get_msg_constants())
    msgs.extend(message_fixtures.get_msg_defaults())
    msgs.extend(message_fixtures.get_msg_empty())
    msgs.extend(message_fixtures.get_msg_multi_nested())
    msgs.extend(message_fixtures.get_msg_nested())
    msgs.extend(message_fixtures.get_msg_strings())
    msgs.extend(message_fixtures.get_msg_unbounded_sequences())
    for m in msgs:
        message_to_csv(m, 100)
        message_to_csv(m, None)
        message_to_ordereddict(m, 100)
        message_to_ordereddict(m, None)
        message_to_yaml(m, 100)
        message_to_yaml(m, None)


def test_convert_primitives():
    assert 5 == _convert_value(5)
    assert 5 == _convert_value(5, truncate_length=0)
    assert 5 == _convert_value(5, truncate_length=1)
    assert 5 == _convert_value(5, truncate_length=10000)
    assert 42.0 == _convert_value(42.0)
    assert 42.0 == _convert_value(42.0, truncate_length=0)
    assert 42.0 == _convert_value(42.0, truncate_length=1)
    assert 42.0 == _convert_value(42.0, truncate_length=10000)
    assert True is _convert_value(True)
    assert True is _convert_value(True, truncate_length=0)
    assert True is _convert_value(True, truncate_length=1)
    assert True is _convert_value(True, truncate_length=10000)
    assert False is _convert_value(False)
    assert False is _convert_value(False, truncate_length=0)
    assert False is _convert_value(False, truncate_length=1)
    assert False is _convert_value(False, truncate_length=10000)


def test_convert_tuple():
    assert (1, 2, 3) == _convert_value((1, 2, 3))
    assert ('...',) == _convert_value((1, 2, 3), truncate_length=0)
    assert (1, 2, '...') == _convert_value((1, 2, 3), truncate_length=2)
    assert ('123', '456', '789') == _convert_value(('123', '456', '789'))
    assert ('12...', '45...', '...') == _convert_value(('123', '456', '789'), truncate_length=2)
    assert ('123', '456', '789') == _convert_value(('123', '456', '789'), truncate_length=5)


def test_convert_list():
    assert [1, 2, 3] == _convert_value([1, 2, 3])
    assert ['...'] == _convert_value([1, 2, 3], truncate_length=0)
    assert [1, 2, '...'] == _convert_value([1, 2, 3], truncate_length=2)
    assert ['123', '456', '789'] == _convert_value(['123', '456', '789'])
    assert ['12...', '45...', '...'] == _convert_value(['123', '456', '789'], truncate_length=2)
    assert ['123', '456', '789'] == _convert_value(['123', '456', '789'], truncate_length=5)


def test_convert_str():
    assert 'hello world' == _convert_value('hello world')
    assert 'hello...' == _convert_value('hello world', truncate_length=5)
    assert 'hello world' == _convert_value('hello world', truncate_length=1000)


def test_convert_bytes():
    assert 'hello world' == _convert_value(b'hello world')
    assert 'hello...' == _convert_value(b'hello world', truncate_length=5)
    assert 'hello world' == _convert_value(b'hello world', truncate_length=1000)


def test_convert_ordered_dict():
    assert OrderedDict([(1, 'a'), ('2', 'b')]) == _convert_value(
        OrderedDict([(1, 'a'), ('2', 'b')]))
    assert OrderedDict([(1, 'a'), ('2', 'b')]) == _convert_value(
        OrderedDict([(1, 'a'), ('2', 'b')]), truncate_length=1)
    assert OrderedDict([(1, 'a'), ('2', 'b')]) == _convert_value(
        OrderedDict([(1, 'a'), ('2', 'b')]), truncate_length=1000)
    assert OrderedDict([(1, 'a...'), ('234', 'b...')]) == _convert_value(
        OrderedDict([(1, 'abc'), ('234', 'bcd')]), truncate_length=1)


def test_convert_dict():
    assert {1: 'a', '2': 'b'} == _convert_value({1: 'a', '2': 'b'})
    assert {1: 'a', '2': 'b'} == _convert_value({1: 'a', '2': 'b'}, truncate_length=1)
    assert {1: 'a', '2': 'b'} == _convert_value({1: 'a', '2': 'b'}, truncate_length=1000)
    assert {1: 'a...', '234': 'b...'} == _convert_value(
        {1: 'abc', '234': 'bcd'}, truncate_length=1)
