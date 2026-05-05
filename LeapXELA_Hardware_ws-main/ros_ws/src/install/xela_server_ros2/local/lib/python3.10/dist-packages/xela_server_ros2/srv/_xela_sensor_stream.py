# generated from rosidl_generator_py/resource/_idl.py.em
# with input from xela_server_ros2:srv/XelaSensorStream.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_XelaSensorStream_Request(type):
    """Metaclass of message 'XelaSensorStream_Request'."""

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
                'xela_server_ros2.srv.XelaSensorStream_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__xela_sensor_stream__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__xela_sensor_stream__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__xela_sensor_stream__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__xela_sensor_stream__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__xela_sensor_stream__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class XelaSensorStream_Request(metaclass=Metaclass_XelaSensorStream_Request):
    """Message class 'XelaSensorStream_Request'."""

    __slots__ = [
        '_sensor',
    ]

    _fields_and_field_types = {
        'sensor': 'uint8',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.sensor = kwargs.get('sensor', int())

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
        if self.sensor != other.sensor:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def sensor(self):
        """Message field 'sensor'."""
        return self._sensor

    @sensor.setter
    def sensor(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'sensor' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'sensor' field must be an unsigned integer in [0, 255]"
        self._sensor = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_XelaSensorStream_Response(type):
    """Metaclass of message 'XelaSensorStream_Response'."""

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
                'xela_server_ros2.srv.XelaSensorStream_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__xela_sensor_stream__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__xela_sensor_stream__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__xela_sensor_stream__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__xela_sensor_stream__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__xela_sensor_stream__response

            from xela_server_ros2.msg import SensorFull
            if SensorFull.__class__._TYPE_SUPPORT is None:
                SensorFull.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class XelaSensorStream_Response(metaclass=Metaclass_XelaSensorStream_Response):
    """Message class 'XelaSensorStream_Response'."""

    __slots__ = [
        '_data',
    ]

    _fields_and_field_types = {
        'data': 'sequence<xela_server_ros2/SensorFull>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['xela_server_ros2', 'msg'], 'SensorFull')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.data = kwargs.get('data', [])

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
        if self.data != other.data:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def data(self):
        """Message field 'data'."""
        return self._data

    @data.setter
    def data(self, value):
        if __debug__:
            from xela_server_ros2.msg import SensorFull
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
                 all(isinstance(v, SensorFull) for v in value) and
                 True), \
                "The 'data' field must be a set or sequence and each value of type 'SensorFull'"
        self._data = value


class Metaclass_XelaSensorStream(type):
    """Metaclass of service 'XelaSensorStream'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('xela_server_ros2')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'xela_server_ros2.srv.XelaSensorStream')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__xela_sensor_stream

            from xela_server_ros2.srv import _xela_sensor_stream
            if _xela_sensor_stream.Metaclass_XelaSensorStream_Request._TYPE_SUPPORT is None:
                _xela_sensor_stream.Metaclass_XelaSensorStream_Request.__import_type_support__()
            if _xela_sensor_stream.Metaclass_XelaSensorStream_Response._TYPE_SUPPORT is None:
                _xela_sensor_stream.Metaclass_XelaSensorStream_Response.__import_type_support__()


class XelaSensorStream(metaclass=Metaclass_XelaSensorStream):
    from xela_server_ros2.srv._xela_sensor_stream import XelaSensorStream_Request as Request
    from xela_server_ros2.srv._xela_sensor_stream import XelaSensorStream_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
