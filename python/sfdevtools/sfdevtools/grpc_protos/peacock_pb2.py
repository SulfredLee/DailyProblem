# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: peacock.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='peacock.proto',
  package='peacock',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rpeacock.proto\x12\x07peacock\">\n\x13SaveFileToColud_Msg\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x14\n\x0c\x66ile_content\x18\x02 \x01(\t\"U\n\x15SaveRefDataFromQC_Msg\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x14\n\x0c\x66ile_content\x18\x02 \x01(\t\x12\x13\n\x0b\x61\x63tion_mode\x18\x03 \x01(\t\"\x1a\n\tNoneReply\x12\r\n\x05reply\x18\x01 \x01(\t\"\x17\n\x04Ping\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x17\n\x04Pong\x12\x0f\n\x07message\x18\x01 \x01(\t2\xc4\x01\n\x07Peacock\x12\x43\n\x0fSaveFileToColud\x12\x1c.peacock.SaveFileToColud_Msg\x1a\x12.peacock.NoneReply\x12G\n\x11SaveRefDataFromQC\x12\x1e.peacock.SaveRefDataFromQC_Msg\x1a\x12.peacock.NoneReply\x12+\n\x0bHealthCheck\x12\r.peacock.Ping\x1a\r.peacock.Pongb\x06proto3'
)




_SAVEFILETOCOLUD_MSG = _descriptor.Descriptor(
  name='SaveFileToColud_Msg',
  full_name='peacock.SaveFileToColud_Msg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_name', full_name='peacock.SaveFileToColud_Msg.file_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='file_content', full_name='peacock.SaveFileToColud_Msg.file_content', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=26,
  serialized_end=88,
)


_SAVEREFDATAFROMQC_MSG = _descriptor.Descriptor(
  name='SaveRefDataFromQC_Msg',
  full_name='peacock.SaveRefDataFromQC_Msg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_name', full_name='peacock.SaveRefDataFromQC_Msg.file_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='file_content', full_name='peacock.SaveRefDataFromQC_Msg.file_content', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='action_mode', full_name='peacock.SaveRefDataFromQC_Msg.action_mode', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  serialized_start=90,
  serialized_end=175,
)


_NONEREPLY = _descriptor.Descriptor(
  name='NoneReply',
  full_name='peacock.NoneReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='reply', full_name='peacock.NoneReply.reply', index=0,
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
  serialized_start=177,
  serialized_end=203,
)


_PING = _descriptor.Descriptor(
  name='Ping',
  full_name='peacock.Ping',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='peacock.Ping.message', index=0,
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
  serialized_start=205,
  serialized_end=228,
)


_PONG = _descriptor.Descriptor(
  name='Pong',
  full_name='peacock.Pong',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='peacock.Pong.message', index=0,
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
  serialized_start=230,
  serialized_end=253,
)

DESCRIPTOR.message_types_by_name['SaveFileToColud_Msg'] = _SAVEFILETOCOLUD_MSG
DESCRIPTOR.message_types_by_name['SaveRefDataFromQC_Msg'] = _SAVEREFDATAFROMQC_MSG
DESCRIPTOR.message_types_by_name['NoneReply'] = _NONEREPLY
DESCRIPTOR.message_types_by_name['Ping'] = _PING
DESCRIPTOR.message_types_by_name['Pong'] = _PONG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SaveFileToColud_Msg = _reflection.GeneratedProtocolMessageType('SaveFileToColud_Msg', (_message.Message,), {
  'DESCRIPTOR' : _SAVEFILETOCOLUD_MSG,
  '__module__' : 'peacock_pb2'
  # @@protoc_insertion_point(class_scope:peacock.SaveFileToColud_Msg)
  })
_sym_db.RegisterMessage(SaveFileToColud_Msg)

SaveRefDataFromQC_Msg = _reflection.GeneratedProtocolMessageType('SaveRefDataFromQC_Msg', (_message.Message,), {
  'DESCRIPTOR' : _SAVEREFDATAFROMQC_MSG,
  '__module__' : 'peacock_pb2'
  # @@protoc_insertion_point(class_scope:peacock.SaveRefDataFromQC_Msg)
  })
_sym_db.RegisterMessage(SaveRefDataFromQC_Msg)

NoneReply = _reflection.GeneratedProtocolMessageType('NoneReply', (_message.Message,), {
  'DESCRIPTOR' : _NONEREPLY,
  '__module__' : 'peacock_pb2'
  # @@protoc_insertion_point(class_scope:peacock.NoneReply)
  })
_sym_db.RegisterMessage(NoneReply)

Ping = _reflection.GeneratedProtocolMessageType('Ping', (_message.Message,), {
  'DESCRIPTOR' : _PING,
  '__module__' : 'peacock_pb2'
  # @@protoc_insertion_point(class_scope:peacock.Ping)
  })
_sym_db.RegisterMessage(Ping)

Pong = _reflection.GeneratedProtocolMessageType('Pong', (_message.Message,), {
  'DESCRIPTOR' : _PONG,
  '__module__' : 'peacock_pb2'
  # @@protoc_insertion_point(class_scope:peacock.Pong)
  })
_sym_db.RegisterMessage(Pong)



_PEACOCK = _descriptor.ServiceDescriptor(
  name='Peacock',
  full_name='peacock.Peacock',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=256,
  serialized_end=452,
  methods=[
  _descriptor.MethodDescriptor(
    name='SaveFileToColud',
    full_name='peacock.Peacock.SaveFileToColud',
    index=0,
    containing_service=None,
    input_type=_SAVEFILETOCOLUD_MSG,
    output_type=_NONEREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SaveRefDataFromQC',
    full_name='peacock.Peacock.SaveRefDataFromQC',
    index=1,
    containing_service=None,
    input_type=_SAVEREFDATAFROMQC_MSG,
    output_type=_NONEREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='HealthCheck',
    full_name='peacock.Peacock.HealthCheck',
    index=2,
    containing_service=None,
    input_type=_PING,
    output_type=_PONG,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_PEACOCK)

DESCRIPTOR.services_by_name['Peacock'] = _PEACOCK

# @@protoc_insertion_point(module_scope)
