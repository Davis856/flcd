class TokenHashTable:
    def __init__(self):
        self.size = 10  # Initial size
        self.table = [None] * self.size

    def insert(self, token, attribute):
        index = self.hash_function(token)
        if self.table[index] is None:
            self.table[index] = []
        self.table[index].append((token, attribute))

        # Check if the load factor exceeds a threshold (e.g., 0.7) and resize the table if needed
        load_factor = sum(1 for entry in self.table if entry) / self.size
        if load_factor > 0.7:
            self.resize()

    def lookup(self, token):
        index = self.hash_function(token)
        if self.table[index] is not None:
            for t, attr in self.table[index]:
                if t == token:
                    return attr
        return None

    def hash_function(self, token):
        return len(token) % self.size

    def resize(self):
        # Double the size and rehash all entries
        self.size *= 2
        new_table = [None] * self.size
        for entry in self.table:
            if entry:
                for token, attribute in entry:
                    index = self.hash_function(token)
                    if new_table[index] is None:
                        new_table[index] = []
                    new_table[index].append((token, attribute))
        self.table = new_table


# Create a hash table for your tokens
token_table = TokenHashTable()

# Insert tokens and their attributes into the hash table
token_table.insert("binary", "DATATYPE")
token_table.insert("func", "IDENTIFIER")
token_table.insert("when", "IDENTIFIER")
token_table.insert("is", "IDENTIFIER")
token_table.insert("truth", "IDENTIFIER")
token_table.insert("contrarily", "IDENTIFIER")
token_table.insert("give-back", "IDENTIFIER")
token_table.insert("as long as", "IDENTIFIER")
token_table.insert("fur", "IDENTIFIER")
token_table.insert("times", "IDENTIFIER")
token_table.insert("increase", "IDENTIFIER")
token_table.insert("engrave", "IDENTIFIER")
token_table.insert("dump", "IDENTIFIER")
token_table.insert("nr", "DATATYPE")
token_table.insert("cap", "IDENTIFIER")
token_table.insert("word", "DATATYPE")
token_table.insert("remainder", "IDENTIFIER")

print(token_table.table)


# Function to extract tokens from code and lookup their attributes
def analyze_code(code):
    import re

    # Define a regular expression pattern to match tokens
    token_pattern = r'\bas long as\b|\bgive-back\b|\b\w+\b'

    # Find all tokens in the code
    code_tokens = re.findall(token_pattern, code)

    token_attributes = []
    for token in code_tokens:
        attribute = token_table.lookup(token)
        if attribute:
            token_attributes.append((token, attribute))
    return token_attributes


# Test the token table with code snippets
code1 = """
binary even_or_odd(nr check) {
binary even = cap.
when check remainder 2 is 0:
even = truth.
contrarily:
even = cap.
give-back even.
}
"""

code2 = """
func printEvenNumbers(nr number) {
nr i = 2.
as long as i <= n:
engrave(i).
i = i increase 2.
}
"""

code3 = """
nr factorial(nr var) {
nr result = 1.
fur nr i=1<=var:
result = result times i.
give-back result.
}
"""

# Analyze and print token attributes for each code snippet
print("Token attributes for code 1:")
print(analyze_code(code1))

print("Token attributes for code 2:")
print(analyze_code(code2))

print("Token attributes for code 3:")
print(analyze_code(code3))
