# generated from rosidl_generator_py/resource/_idl.py.em
# with input from xela_server_ros2:msg/SensorFull.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_SensorFull(type):
    """Metaclass of message 'SensorFull'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('xela_server_ros2')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'xela_server_ros2.msg.SensorFull')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__sensor_full
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__sensor_full
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__sensor_full
            cls._TYPE_SUPPORT = module.type_support_msg__msg__sensor_full
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__sensor_full

            from xela_server_ros2.msg import Forces
            if Forces.__class__._TYPE_SUPPORT is None:
                Forces.__class__.__import_type_support__()

            from xela_server_ros2.msg import Taxel
            if Taxel.__class__._TYPE_SUPPORT is None:
                Taxel.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class SensorFull(metaclass=Metaclass_SensorFull):
    """Message class 'SensorFull'."""

    __slots__ = [
        '_message',
        '_time',
        '_model',
        '_sensor_pos',
        '_taxels',
        '_forces',
    ]

    _fields_and_field_types = {
        'message': 'uint32',
        'time': 'double',
        'model': 'string',
        'sensor_pos': 'uint8',
        'taxels': 'sequence<xela_server_ros2/Taxel>',
        'forces': 'sequence<xela_server_ros2/Forces>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['xela_server_ros2', 'msg'], 'Taxel')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['xela_server_ros2', 'msg'], 'Forces')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.message = kwargs.get('message', int())
        self.time = kwargs.get('time', float())
        self.model = kwargs.get('model', str())
        self.sensor_pos = kwargs.get('sensor_pos', int())
        self.taxels = kwargs.get('taxels', [])
        self.forces = kwargs.get('forces', [])

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.message != other.message:
            return False
        if self.time != other.time:
            return False
        if self.model != other.model:
            return False
        if self.sensor_pos != other.sensor_pos:
            return False
        if self.taxels != other.taxels:
            return False
        if self.forces != other.forces:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def message(self):
        """Message field 'message'."""
        return self._message

    @message.setter
    def message(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'message' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'message' field must be an unsigned integer in [0, 4294967295]"
        self._message = value

    @builtins.property
    def time(self):
        """Message field 'time'."""
        return self._time

    @time.setter
    def time(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'time' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'time' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._time = value

    @builtins.property
    def model(self):
        """Message field 'model'."""
        return self._model

    @model.setter
    def model(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'model' field must be of type 'str'"
        self._model = value

    @builtins.property
    def sensor_pos(self):
        """Message field 'sensor_pos'."""
        return self._sensor_pos

    @sensor_pos.setter
    def sensor_pos(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'sensor_pos' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'sensor_pos' field must be an unsigned integer in [0, 255]"
        self._sensor_pos = value

    @builtins.property
    def taxels(self):
        """Message field 'taxels'."""
        return self._taxels

    @taxels.setter
    def taxels(self, value):
        if __debug__:
            from xela_server_ros2.msg import Taxel
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, Taxel) for v in value) and
                 True), \
                "The 'taxels' field must be a set or sequence and each value of type 'Taxel'"
        self._taxels = value

    @builtins.property
    def forces(self):
        """Message field 'forces'."""
        return self._forces

    @forces.setter
    def forces(self, value):
        if __debug__:
            from xela_server_ros2.msg import Forces
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, Forces) for v in value) and
                 True), \
                "The 'forces' field must be a set or sequence and each value of type 'Forces'"
        self._forces = value
