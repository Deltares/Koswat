## Koswat Ini Reader module.

This module contains the general reading of an INI file and its transformation into a FOM.
The ini reading is done using de python default library `configparser`. 
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