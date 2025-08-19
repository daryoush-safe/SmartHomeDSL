class SymbolTable:
    class Record:
        def __init__(self, record_name, record_scope, record_type, record_value, record_file, record_line,
                     record_offset,
                     record_length):
            self.record_name: str = record_name
            self.record_scope = record_scope
            self.record_type = record_type
            self.record_value = record_value
            self.record_file = record_file
            self.record_line = record_line
            self.record_offset = record_offset
            self.record_length = record_length

        def __str__(self):
            return ("{ name: " + f"{self.record_name}, " +
                    f"scope: {self.record_scope}, " +
                    f"type: {self.record_type}, " +
                    f"value: {self.record_value}, " +
                    f"file: {self.record_file}, " +
                    f"line: {self.record_line}, " +
                    f"offset: {self.record_offset}, " +
                    f"length: {self.record_length}" + " }"
                    )



    def __init__(self):
        self.table: list[SymbolTable.Record] = []

    def lookup(self,record_name,record_scope='global'):
        for entry in self.table:
            if entry.record_name == record_name and entry.record_scope == record_scope:
                return entry
        return None

    def insert(self,record:Record):
        for entry in self.table:
            if entry.record_name == record.record_name and entry.record_scope == record.record_scope:
                print("redefinition")
        self.table.append(record)

