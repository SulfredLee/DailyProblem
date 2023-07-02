# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: peacock.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rpeacock.proto\x12\x07peacock\".\n\x17GetDataByStrategyId_Msg\x12\x13\n\x0bstrategy_id\x18\x01 \x01(\t\"\x80\x01\n\x19GetDataByStrategyId_Reply\x12\x0b\n\x03\x63\x66g\x18\x01 \x03(\t\x12\n\n\x02\x63i\x18\x02 \x03(\t\x12\n\n\x02si\x18\x03 \x01(\t\x12\x10\n\x08ord_snap\x18\x04 \x01(\t\x12\x10\n\x08ord_hist\x18\x05 \x01(\t\x12\x0b\n\x03trd\x18\x06 \x01(\t\x12\r\n\x05price\x18\x07 \x01(\t\"c\n\x19GetBacktestWarmupData_Msg\x12\x13\n\x0bstrategy_id\x18\x01 \x01(\t\x12\x0e\n\x06msg_id\x18\x02 \x01(\t\x12\x10\n\x08msg_type\x18\x03 \x01(\x05\x12\x0f\n\x07\x66id_num\x18\x04 \x01(\x05\"+\n\x1bGetBacktestWarmupData_Reply\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"*\n\x10GetUSLEIData_Msg\x12\x16\n\x0elookback_month\x18\x01 \x01(\x05\"\x91\x01\n\x12GetUSLEIData_Reply\x12\x46\n\x0fus_lei_data_map\x18\x01 \x03(\x0b\x32-.peacock.GetUSLEIData_Reply.UsLeiDataMapEntry\x1a\x33\n\x11UsLeiDataMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\\\n\x18RemoveStrategyConfig_Msg\x12\x15\n\rstrategy_name\x18\x01 \x01(\t\x12\x0f\n\x07is_live\x18\x02 \x01(\x08\x12\x18\n\x10strategy_id_list\x18\x03 \x03(\t\"#\n\x13RemoveOldConfig_Msg\x12\x0c\n\x04\x64\x61ys\x18\x01 \x01(\x05\"\x1c\n\x0b\x44ummy_Reply\x12\r\n\x05\x64ummy\x18\x01 \x01(\t\"?\n\x15GetStrategyConfig_Msg\x12\x15\n\rstrategy_name\x18\x01 \x01(\t\x12\x0f\n\x07is_live\x18\x02 \x01(\x08\";\n\x17GetStrategyConfig_Reply\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x10\n\x08\x63\x66g_list\x18\x02 \x03(\t\"1\n\x16SaveStrategyConfig_Msg\x12\x17\n\x0fstrategy_config\x18\x01 \x01(\t\"*\n\x18SaveStrategyConfig_Reply\x12\x0e\n\x06status\x18\x01 \x01(\t\">\n\x13SaveFileToColud_Msg\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x14\n\x0c\x66ile_content\x18\x02 \x01(\t\"Z\n\x1aSaveRefDataPriceFromQC_Msg\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x14\n\x0c\x66ile_content\x18\x02 \x01(\t\x12\x13\n\x0b\x61\x63tion_mode\x18\x03 \x01(\t\"U\n\x15SaveRefDataFromQC_Msg\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x14\n\x0c\x66ile_content\x18\x02 \x01(\t\x12\x13\n\x0b\x61\x63tion_mode\x18\x03 \x01(\t\"\x1a\n\tNoneReply\x12\r\n\x05reply\x18\x01 \x01(\t\"\x17\n\x04Ping\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x17\n\x04Pong\x12\x0f\n\x07message\x18\x01 \x01(\t2\xe8\x06\n\x07Peacock\x12\x43\n\x0fSaveFileToColud\x12\x1c.peacock.SaveFileToColud_Msg\x1a\x12.peacock.NoneReply\x12Q\n\x16SaveRefDataPriceFromQC\x12#.peacock.SaveRefDataPriceFromQC_Msg\x1a\x12.peacock.NoneReply\x12G\n\x11SaveRefDataFromQC\x12\x1e.peacock.SaveRefDataFromQC_Msg\x1a\x12.peacock.NoneReply\x12X\n\x12SaveStrategyConfig\x12\x1f.peacock.SaveStrategyConfig_Msg\x1a!.peacock.SaveStrategyConfig_Reply\x12U\n\x11GetStrategyConfig\x12\x1e.peacock.GetStrategyConfig_Msg\x1a .peacock.GetStrategyConfig_Reply\x12O\n\x14RemoveStrategyConfig\x12!.peacock.RemoveStrategyConfig_Msg\x1a\x14.peacock.Dummy_Reply\x12\x45\n\x0fRemoveOldConfig\x12\x1c.peacock.RemoveOldConfig_Msg\x1a\x14.peacock.Dummy_Reply\x12[\n\x13GetDataByStrategyId\x12 .peacock.GetDataByStrategyId_Msg\x1a\".peacock.GetDataByStrategyId_Reply\x12\x61\n\x15GetBacktestWarmupData\x12\".peacock.GetBacktestWarmupData_Msg\x1a$.peacock.GetBacktestWarmupData_Reply\x12\x46\n\x0cGetUSLEIData\x12\x19.peacock.GetUSLEIData_Msg\x1a\x1b.peacock.GetUSLEIData_Reply\x12+\n\x0bHealthCheck\x12\r.peacock.Ping\x1a\r.peacock.Pongb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'peacock_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETUSLEIDATA_REPLY_USLEIDATAMAPENTRY._options = None
  _GETUSLEIDATA_REPLY_USLEIDATAMAPENTRY._serialized_options = b'8\001'
  _GETDATABYSTRATEGYID_MSG._serialized_start=26
  _GETDATABYSTRATEGYID_MSG._serialized_end=72
  _GETDATABYSTRATEGYID_REPLY._serialized_start=75
  _GETDATABYSTRATEGYID_REPLY._serialized_end=203
  _GETBACKTESTWARMUPDATA_MSG._serialized_start=205
  _GETBACKTESTWARMUPDATA_MSG._serialized_end=304
  _GETBACKTESTWARMUPDATA_REPLY._serialized_start=306
  _GETBACKTESTWARMUPDATA_REPLY._serialized_end=349
  _GETUSLEIDATA_MSG._serialized_start=351
  _GETUSLEIDATA_MSG._serialized_end=393
  _GETUSLEIDATA_REPLY._serialized_start=396
  _GETUSLEIDATA_REPLY._serialized_end=541
  _GETUSLEIDATA_REPLY_USLEIDATAMAPENTRY._serialized_start=490
  _GETUSLEIDATA_REPLY_USLEIDATAMAPENTRY._serialized_end=541
  _REMOVESTRATEGYCONFIG_MSG._serialized_start=543
  _REMOVESTRATEGYCONFIG_MSG._serialized_end=635
  _REMOVEOLDCONFIG_MSG._serialized_start=637
  _REMOVEOLDCONFIG_MSG._serialized_end=672
  _DUMMY_REPLY._serialized_start=674
  _DUMMY_REPLY._serialized_end=702
  _GETSTRATEGYCONFIG_MSG._serialized_start=704
  _GETSTRATEGYCONFIG_MSG._serialized_end=767
  _GETSTRATEGYCONFIG_REPLY._serialized_start=769
  _GETSTRATEGYCONFIG_REPLY._serialized_end=828
  _SAVESTRATEGYCONFIG_MSG._serialized_start=830
  _SAVESTRATEGYCONFIG_MSG._serialized_end=879
  _SAVESTRATEGYCONFIG_REPLY._serialized_start=881
  _SAVESTRATEGYCONFIG_REPLY._serialized_end=923
  _SAVEFILETOCOLUD_MSG._serialized_start=925
  _SAVEFILETOCOLUD_MSG._serialized_end=987
  _SAVEREFDATAPRICEFROMQC_MSG._serialized_start=989
  _SAVEREFDATAPRICEFROMQC_MSG._serialized_end=1079
  _SAVEREFDATAFROMQC_MSG._serialized_start=1081
  _SAVEREFDATAFROMQC_MSG._serialized_end=1166
  _NONEREPLY._serialized_start=1168
  _NONEREPLY._serialized_end=1194
  _PING._serialized_start=1196
  _PING._serialized_end=1219
  _PONG._serialized_start=1221
  _PONG._serialized_end=1244
  _PEACOCK._serialized_start=1247
  _PEACOCK._serialized_end=2119
# @@protoc_insertion_point(module_scope)
