import configparser
import os

# reads top level ini file, searches for ini file references or directories and proceses them also.
# produces a dict of configuration objects that contain the content of the ini files
# key = key from top ini file or filename of inifile in directory
# value = list containing configuration object and path to ini file belonging to the configuration object


class KoswatIniReader:

    top_ini_name = "TOP"
    ini_mask = ".ini"
    comment_character = "#"

    def delete_comment_from_string(self, path_string):
        # 1- Split string on pre and post comment character
        # 2- Take left side, this contains the value of the key value pair in the ini file
        # 3- Remove spaces
        # 4- Remove double quotes around string
        return path_string.split(self.comment_character)[0].strip().strip('"')

    def add_config(self, configs, name, path):
        config = configparser.ConfigParser()
        config.read(path)
        configs.update({name: [config, path]})

    def read(self, path) -> dict:
        configs = dict()
        # Read the top level ini file and add it to the configurations dict.
        self.add_config(configs, self.top_ini_name, path)
        # Looking for other ini file references
        top_config = configs[self.top_ini_name][0]
        for section in top_config.sections():
            for key in top_config[section]:
                # The section key can reference an ini file or a directory containing ini files
                # if so, add it to the configurations dict.
                section_key = self.delete_comment_from_string(top_config[section][key])
                if section_key.endswith(self.ini_mask):
                    self.add_config(configs, key, section_key)
                if os.path.isdir(section_key):
                    # Process all files in the directory
                    for file_name in os.listdir(section_key):
                        section_key_and_file = os.path.join(section_key, file_name)
                        if os.path.isfile(section_key_and_file):
                            # If file is an ini file, add it to the configurations dict
                            if file_name.endswith(self.ini_mask):
                                self.add_config(
                                    configs, file_name, section_key_and_file
                                )
        return configs


config_file_path = "p:\\frm-koswat\\KOSWAT v2022\\Invoer\\ini files\\KOSWAT2022.ini"

koswatIniReader = KoswatIniReader()
configs = koswatIniReader.read(config_file_path)
print(len(configs))
