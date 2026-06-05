"""Database schema definitions."""

from __future__ import annotations

from pydantic import Field, model_validator

from .base import StrictBaseModel, ensure_non_empty_strings, ensure_unique_values, set_field_value
from .types import DatabaseEngine


class ColumnSchema(StrictBaseModel):
    name: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z][A-Za-z0-9_]*$")
    data_type: str = Field(min_length=1, max_length=128)
    nullable: bool = False
    primary_key: bool = False
    unique: bool = False
    default: str | None = None
    description: str | None = Field(default=None, max_length=2_000)


class ForeignKeySchema(StrictBaseModel):
    column: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z][A-Za-z0-9_]*$")
    referenced_table: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z][A-Za-z0-9_]*$")
    referenced_column: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z][A-Za-z0-9_]*$")
    on_delete: str = Field(default="RESTRICT", min_length=3, max_length=32)
    on_update: str = Field(default="CASCADE", min_length=3, max_length=32)


class IndexSchema(StrictBaseModel):
    name: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z][A-Za-z0-9_]*$")
    columns: list[str] = Field(default_factory=list)
    unique: bool = False

    @model_validator(mode="after")
    def validate_columns(self) -> "IndexSchema":
        set_field_value(self, "columns", ensure_non_empty_strings(self.columns, "index.columns"))
        return self


class TableSchema(StrictBaseModel):
    name: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z][A-Za-z0-9_]*$")
    description: str | None = Field(default=None, max_length=2_000)
    columns: list[ColumnSchema] = Field(default_factory=list)
    foreign_keys: list[ForeignKeySchema] = Field(default_factory=list)
    indexes: list[IndexSchema] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_table(self) -> "TableSchema":
        if not self.columns:
            raise ValueError("columns must contain at least one column")

        column_names = [column.name for column in self.columns]
        ensure_unique_values(column_names, f"columns for table {self.name}")

        primary_keys = [column.name for column in self.columns if column.primary_key]
        if not primary_keys:
            raise ValueError(f"table {self.name} must define at least one primary key column")

        for index in self.indexes:
            invalid_columns = sorted(column for column in index.columns if column not in column_names)
            if invalid_columns:
                raise ValueError(
                    f"index {index.name} in table {self.name} references unknown columns: {', '.join(invalid_columns)}"
                )

        for foreign_key in self.foreign_keys:
            if foreign_key.column not in column_names:
                raise ValueError(
                    f"foreign key on table {self.name} references unknown column {foreign_key.column}"
                )

        return self


class DatabaseSchema(StrictBaseModel):
    engine: DatabaseEngine = DatabaseEngine.POSTGRESQL
    database_name: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z][A-Za-z0-9_]*$")
    schemas: list[str] = Field(default_factory=lambda: ["public"])
    tables: list[TableSchema] = Field(default_factory=list)
    connection_pool_size: int = Field(default=10, ge=1, le=1_000)
    enable_migrations: bool = True

    @model_validator(mode="after")
    def validate_database(self) -> "DatabaseSchema":
        if not self.tables:
            raise ValueError("tables must contain at least one table")

        set_field_value(self, "schemas", ensure_non_empty_strings(self.schemas, "schemas"))
        table_names = [table.name for table in self.tables]
        ensure_unique_values(table_names, "tables")

        table_lookup = {table.name: table for table in self.tables}
        for table in self.tables:
            for foreign_key in table.foreign_keys:
                referenced = table_lookup.get(foreign_key.referenced_table)
                if referenced is None:
                    raise ValueError(
                        f"table {table.name} references unknown table {foreign_key.referenced_table}"
                    )
                referenced_columns = {column.name for column in referenced.columns}
                if foreign_key.referenced_column not in referenced_columns:
                    raise ValueError(
                        f"table {table.name} references unknown column {foreign_key.referenced_column} on table {foreign_key.referenced_table}"
                    )

        return self