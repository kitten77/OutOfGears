# Field classes
from hachoir.field.field import Field, FieldError, MissingField, joinPath
from hachoir.field.bit_field import Bit, Bits, RawBits
from hachoir.field.byte_field import Bytes, RawBytes
from hachoir.field.sub_file import SubFile, CompressedField
from hachoir.field.character import Character
from hachoir.field.integer import (
    Int8, Int16, Int24, Int32, Int64,
    UInt8, UInt16, UInt24, UInt32, UInt64,
    GenericInteger)
from hachoir.field.enum import Enum
from hachoir.field.string_field import (GenericString,
                                        String, CString, UnixLine,
                                        PascalString8, PascalString16, PascalString32)
from hachoir.field.padding import (PaddingBits, PaddingBytes,
                                   NullBits, NullBytes)

# Functions
from hachoir.field.helper import (isString, isInteger,
                                  createPaddingField, createNullField, createRawField,
                                  writeIntoFile, createOrphanField)

# FieldSet classes
from lib.hachoir.field.fake_array import FakeArray
from lib.hachoir.field.basic_field_set import (BasicFieldSet,
                                           ParserError, MatchError)
from lib.hachoir.field.generic_field_set import GenericFieldSet
from lib.hachoir.field.seekable_field_set import SeekableFieldSet, RootSeekableFieldSet
from lib.hachoir.field.field_set import FieldSet
from lib.hachoir.field.static_field_set import StaticFieldSet
from lib.hachoir.field.parser import Parser
from lib.hachoir.field.vector import GenericVector, UserVector

# Complex types
from lib.hachoir.field.float import Float32, Float64, Float80
from lib.hachoir.field.timestamp import (GenericTimestamp,
                                     TimestampUnix32, TimestampUnix64, TimestampMac32, TimestampUUID60, TimestampWin64,
                                     DateTimeMSDOS32, TimeDateMSDOS32, TimedeltaWin64)

# Special Field classes
from lib.hachoir.field.link import Link, Fragment
from lib.hachoir.field.fragment import FragmentGroup, CustomFragment

available_types = (
    Bit, Bits, RawBits,
    Bytes, RawBytes,
    SubFile,
    Character,
    Int8, Int16, Int24, Int32, Int64,
    UInt8, UInt16, UInt24, UInt32, UInt64,
    String, CString, UnixLine,
    PascalString8, PascalString16, PascalString32,
    Float32, Float64,
    PaddingBits, PaddingBytes,
    NullBits, NullBytes,
    TimestampUnix32, TimestampMac32, TimestampWin64,
    DateTimeMSDOS32, TimeDateMSDOS32,
    #    GenericInteger, GenericString,
)
