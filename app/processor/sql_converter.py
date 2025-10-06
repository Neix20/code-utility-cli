from .base import Processor
from typing import List, Dict

import pandas as pd
from io import StringIO

class SqlConverterProcessor(Processor):

    def __init__(self, type: str, tbl_name: str = "tbl_name"):
        self.type = type.lower()
        self.tbl_name = tbl_name

        self.headers = []

        selection = ["csv-to-insert", "csv-to-update", "csv-to-select"]

        if self.type not in selection:
            raise ValueError(f"Type must be either '{"', ".join(selection[:-1])}' or '{selection[-1]}'")
        
    def gen_select(self, row) -> str:

        """Generate a single SQL SELECT statement."""

        if "id" in self.headers:
            s_columns = ", ".join(self.headers[1:])
            s_body = f"\nAND id = {row['id']};"
        else:
            s_columns = ", ".join(self.headers)
            s_body = f";"

        return f"""
SELECT {s_columns}
FROM {self.tbl_name}
WHERE 1=1{s_body}""".strip()
    
    def gen_update(self, row) -> str:
        """Generate a single SQL UPDATE wrapped in a transaction."""

        # Get Values of Row
        d = row.to_dict()

        if "id" in self.headers:
            s_values = []

            for key, value in d.items():
                if key == "id":
                    continue
                s_values.append(f"{key} = '{value}'")

            s_values = ",\n    ".join(s_values)
            s_body = f"\nAND id = {row['id']};"
        else:
            s_values = []

            for key, value in d.items():
                s_values.append(f"{key} = '{value}'")

            s_values = ",\n    ".join(s_values)
            s_body = ";"

        return f"""UPDATE {self.tbl_name}
SET
    {s_values}
WHERE 1=1{s_body}"""
    
    def gen_insert(self, row) -> str:
        """Generate a single SQL INSERT wrapped in a transaction."""

        # Get Values of Row
        values = list(row.to_dict().values())
        values = [str(x) for x in values]

        if "id" in self.headers:
            s_columns = ",\n    ".join(self.headers[1:])
            s_values = ",\n    ".join(values[1:])
        else:
            s_columns = ",\n    ".join(self.headers)
            s_values = ",\n    ".join(values)

        return f"""INSERT INTO {self.tbl_name}
(
    {s_columns}
)
VALUES
(
    {s_values}
);"""
    

    def process(self, data: str) -> List[str]:
        """Convert list of strings into a JSON array string."""

        # Parse Text File as Original
        data = "\n".join(data)

        # Convert to DataFrame
        df = pd.read_csv(StringIO(data))

        # Retrieve Columns
        self.headers = df.columns.tolist()

        output_ls = []

        # Generate SQL Statements
        if self.type in ["csv-to-insert", "csv-to-update"]:
             output_ls.append("BEGIN TRANSACTION;")

        for _, row in df.iterrows():
            if self.type == "csv-to-select":
                stmt = self.gen_select(row)
            elif self.type == "csv-to-insert":
                stmt = self.gen_insert(row)
            elif self.type == "csv-to-update":
                stmt = self.gen_update(row)
            output_ls.append(stmt.strip())

        if self.type in ["csv-to-insert", "csv-to-select"]:
             output_ls.append("COMMIT TRANSACTION;")

        # Generate Output Statement
        sql_statements = "\n".join(output_ls)
        return sql_statements