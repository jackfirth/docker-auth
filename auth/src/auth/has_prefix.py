def has_prefix(prefix, string):
    return len(string) >= len(prefix) and string[:len(prefix)] == prefix
