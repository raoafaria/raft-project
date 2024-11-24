from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RequestVoteRequest(_message.Message):
    __slots__ = ("candidateId", "term", "lastLogIndex", "lastLogTerm")
    CANDIDATEID_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    LASTLOGINDEX_FIELD_NUMBER: _ClassVar[int]
    LASTLOGTERM_FIELD_NUMBER: _ClassVar[int]
    candidateId: int
    term: int
    lastLogIndex: int
    lastLogTerm: int
    def __init__(self, candidateId: _Optional[int] = ..., term: _Optional[int] = ..., lastLogIndex: _Optional[int] = ..., lastLogTerm: _Optional[int] = ...) -> None: ...

class VoteResponse(_message.Message):
    __slots__ = ("term", "voteGranted")
    TERM_FIELD_NUMBER: _ClassVar[int]
    VOTEGRANTED_FIELD_NUMBER: _ClassVar[int]
    term: int
    voteGranted: bool
    def __init__(self, term: _Optional[int] = ..., voteGranted: bool = ...) -> None: ...

class AppendEntriesRequest(_message.Message):
    __slots__ = ("leaderId", "term", "prevLogIndex", "prevLogTerm", "entries", "leaderCommit")
    LEADERID_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    PREVLOGINDEX_FIELD_NUMBER: _ClassVar[int]
    PREVLOGTERM_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    LEADERCOMMIT_FIELD_NUMBER: _ClassVar[int]
    leaderId: int
    term: int
    prevLogIndex: int
    prevLogTerm: int
    entries: _containers.RepeatedCompositeFieldContainer[LogEntry]
    leaderCommit: int
    def __init__(self, leaderId: _Optional[int] = ..., term: _Optional[int] = ..., prevLogIndex: _Optional[int] = ..., prevLogTerm: _Optional[int] = ..., entries: _Optional[_Iterable[_Union[LogEntry, _Mapping]]] = ..., leaderCommit: _Optional[int] = ...) -> None: ...

class AppendEntriesResponse(_message.Message):
    __slots__ = ("term", "success")
    TERM_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    term: int
    success: bool
    def __init__(self, term: _Optional[int] = ..., success: bool = ...) -> None: ...

class LogEntry(_message.Message):
    __slots__ = ("index", "term", "operation")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    index: int
    term: int
    operation: str
    def __init__(self, index: _Optional[int] = ..., term: _Optional[int] = ..., operation: _Optional[str] = ...) -> None: ...

class ExecuteOperationRequest(_message.Message):
    __slots__ = ("operation",)
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    operation: str
    def __init__(self, operation: _Optional[str] = ...) -> None: ...

class ExecuteOperationResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
