# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: falcon.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='falcon.proto',
  package='falcon',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0c\x66\x61lcon.proto\x12\x06\x66\x61lcon\"\x17\n\x04Ping\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x17\n\x04Pong\x12\x0f\n\x07message\x18\x01 \x01(\t23\n\x06\x46\x61lcon\x12)\n\x0bHealthCheck\x12\x0c.falcon.Ping\x1a\x0c.falcon.Pongb\x06proto3'
)




_PING = _descriptor.Descriptor(
  name='Ping',
  full_name='falcon.Ping',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='falcon.Ping.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=47,
)


_PONG = _descriptor.Descriptor(
  name='Pong',
  full_name='falcon.Pong',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='falcon.Pong.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=49,
  serialized_end=72,
)

DESCRIPTOR.message_types_by_name['Ping'] = _PING
DESCRIPTOR.message_types_by_name['Pong'] = _PONG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Ping = _reflection.GeneratedProtocolMessageType('Ping', (_message.Message,), {
  'DESCRIPTOR' : _PING,
  '__module__' : 'falcon_pb2'
  # @@protoc_insertion_point(class_scope:falcon.Ping)
  })
_sym_db.RegisterMessage(Ping)

Pong = _reflection.GeneratedProtocolMessageType('Pong', (_message.Message,), {
  'DESCRIPTOR' : _PONG,
  '__module__' : 'falcon_pb2'
  # @@protoc_insertion_point(class_scope:falcon.Pong)
  })
_sym_db.RegisterMessage(Pong)



_FALCON = _descriptor.ServiceDescriptor(
  name='Falcon',
  full_name='falcon.Falcon',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=74,
  serialized_end=125,
  methods=[
  _descriptor.MethodDescriptor(
    name='HealthCheck',
    full_name='falcon.Falcon.HealthCheck',
    index=0,
    containing_service=None,
    input_type=_PING,
    output_type=_PONG,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_FALCON)

DESCRIPTOR.services_by_name['Falcon'] = _FALCON

# @@protoc_insertion_point(module_scope)
