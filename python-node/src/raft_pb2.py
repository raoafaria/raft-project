# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: raft.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'raft.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nraft.proto\"b\n\x12RequestVoteRequest\x12\x13\n\x0b\x63\x61ndidateId\x18\x01 \x01(\x05\x12\x0c\n\x04term\x18\x02 \x01(\x05\x12\x14\n\x0clastLogIndex\x18\x03 \x01(\x05\x12\x13\n\x0blastLogTerm\x18\x04 \x01(\x05\"1\n\x0cVoteResponse\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x13\n\x0bvoteGranted\x18\x02 \x01(\x08\"\x93\x01\n\x14\x41ppendEntriesRequest\x12\x10\n\x08leaderId\x18\x01 \x01(\x05\x12\x0c\n\x04term\x18\x02 \x01(\x05\x12\x14\n\x0cprevLogIndex\x18\x03 \x01(\x05\x12\x13\n\x0bprevLogTerm\x18\x04 \x01(\x05\x12\x1a\n\x07\x65ntries\x18\x05 \x03(\x0b\x32\t.LogEntry\x12\x14\n\x0cleaderCommit\x18\x06 \x01(\x05\"6\n\x15\x41ppendEntriesResponse\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0f\n\x07success\x18\x02 \x01(\x08\":\n\x08LogEntry\x12\r\n\x05index\x18\x01 \x01(\x05\x12\x0c\n\x04term\x18\x02 \x01(\x05\x12\x11\n\toperation\x18\x03 \x01(\t\",\n\x17\x45xecuteOperationRequest\x12\x11\n\toperation\x18\x01 \x01(\t\"+\n\x18\x45xecuteOperationResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\xc6\x01\n\x08RaftNode\x12\x31\n\x0bRequestVote\x12\x13.RequestVoteRequest\x1a\r.VoteResponse\x12>\n\rAppendEntries\x12\x15.AppendEntriesRequest\x1a\x16.AppendEntriesResponse\x12G\n\x10\x45xecuteOperation\x12\x18.ExecuteOperationRequest\x1a\x19.ExecuteOperationResponseB#\n\x10\x63om.example.raftB\rRaftNodeProtoP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'raft_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\020com.example.raftB\rRaftNodeProtoP\001'
  _globals['_REQUESTVOTEREQUEST']._serialized_start=14
  _globals['_REQUESTVOTEREQUEST']._serialized_end=112
  _globals['_VOTERESPONSE']._serialized_start=114
  _globals['_VOTERESPONSE']._serialized_end=163
  _globals['_APPENDENTRIESREQUEST']._serialized_start=166
  _globals['_APPENDENTRIESREQUEST']._serialized_end=313
  _globals['_APPENDENTRIESRESPONSE']._serialized_start=315
  _globals['_APPENDENTRIESRESPONSE']._serialized_end=369
  _globals['_LOGENTRY']._serialized_start=371
  _globals['_LOGENTRY']._serialized_end=429
  _globals['_EXECUTEOPERATIONREQUEST']._serialized_start=431
  _globals['_EXECUTEOPERATIONREQUEST']._serialized_end=475
  _globals['_EXECUTEOPERATIONRESPONSE']._serialized_start=477
  _globals['_EXECUTEOPERATIONRESPONSE']._serialized_end=520
  _globals['_RAFTNODE']._serialized_start=523
  _globals['_RAFTNODE']._serialized_end=721
# @@protoc_insertion_point(module_scope)
