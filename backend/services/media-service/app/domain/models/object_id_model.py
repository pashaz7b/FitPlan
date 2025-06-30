from typing import Any

from bson import ObjectId
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from bson.errors import InvalidId
from fastapi import HTTPException, status
import re
from loguru import logger


class ObjectIdPydanticAnnotation:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> ObjectId:
        if isinstance(v, ObjectId):
            return v

        s = handler(v)
        if ObjectId.is_valid(s):
            return ObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(
            cls, source_type, _handler
    ) -> core_schema.CoreSchema:
        assert source_type is ObjectId
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class ObjectIdConverter:
    def __init__(self):
        self.hex_pattern = re.compile(r'^[0-9a-fA-F]{24}$')

    async def convert_to_object_id(self, id_str: str) -> ObjectId:
        try:
            return ObjectId(id_str)
        except (TypeError, InvalidId):
            logger.error("Invalid image ID format for coach")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image ID format"
            )
