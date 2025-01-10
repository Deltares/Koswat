# Koswat Ini Reader module.

This module contains the general reading of an INI file and its transformation into an instance of a `FileObjectModelProtocol`.
The ini reading is done using de python default library [configparser.ConfigParser](https://docs.python.org/3/library/configparser.html). This allows us to simply delegate the mapping responsibility to the instance of a `KoswatIniFomProtocol`, easily achieved by using the class method `from_config`.

## INI file format:
The following is accepted:
```ini
[section]
a_true_bool_value = True 
a_false_bool_value = False 
a_str_value = This is a string.
a_path_value = this/is/a/path
a_float_value = 4.2
# A comment
an_int_value = 42
```

This is not accepted:
```ini
a_true_bool_value = true # or false
a_str_value = This is a string. # comment in-line will get parsed as a value.
a_path_value = "this/is/a/path" # Path (or string) will now contain commas.
```