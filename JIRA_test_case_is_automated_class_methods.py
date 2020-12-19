"""pip install jira"""
from jira import JIRA
import json


class IsAutomated:
    """verifies given list of test cases in jira if they are automated
    TODO
        be able to load file if given as parameter when called from different module and command line
        or load file as argument from command line
    """

    def __init__(self):

        pass

    def load_conf(self, filename):
        """example json file
        {
           "configuration": {
                "data_file_path": "G:\\temporary indement files\\regression_scope\\issue_list.txt",
                "output_file_path": "G:\\temporary indement files\\regression_scope\\automated_list.txt",
                "password": "heslo",
                "url": "https://bugs.web.com:9093",
                "username": "pszturc"
            }
        }
        """
        conf = dict()  # empty dictionary for the data
        with open(filename, 'r') as fconf:
            conf_json = json.load(fconf)
            conf["auth"] = (conf_json["configuration"]["username"], conf_json["configuration"]["password"])
            conf["url"] = conf_json["configuration"]["url"]
            conf["data_file_path"] = conf_json["configuration"]["data_file_path"]
            conf["output_file"] = conf_json["configuration"]["output_file_path"]
        return conf

    def load_issue_list(self, filename):
        """takes file and parse data from it into list
        """
        with open(filename, 'r') as fdata:
            issue_list = fdata.read().splitlines()
        return issue_list

    def get_response(self, jira, issue_key):
        return jira.issue(issue_key)

    def is_automated_bool(self, response):
        """takes given response (jira issue object, evaluates for custom field == "Automated" """
        # response.fields.customfield_14660.value
        # the custom field is unfortunately hardcoded with ID, hopefully it doesn't change
        if response.fields.customfield_14660 is not None:
            if response.fields.customfield_14660.value == "Automated":
                return True
        else:
            return False

    def is_automated_string(self, response):
        """takes given response (jira issue object, evaluates for custom field == "Automated" """
        # response.fields.customfield_14660.value
        # the custom field is unfortunately hardcoded with ID, hopefully it doesn't change
        if response.fields.customfield_14660 is not None:
            return response.fields.customfield_14660.value
        else:
            return "Not automated"

    def results_to_file(self, filename, issue_dict, delete=False):
        """"preferably? dictionary ZTM:boolean is automated
            filename:
            issue_dict: dictionary of issues and their state
            delete: boolean - delete the file content first
        """
        update = "w+"
        if delete:
            update = "w"
        with open(filename, update) as fresults:
            for key, value in issue_dict.items():
                fresults.write(key + ":" + value)
                fresults.write("\n")

    def result_to_file(self, filename, line, delete=False):
        """simplier output that write only one result at a time for different purpose"""
        update = "w+"
        if delete:
            update = "w"
        with open(filename, update) as fresults:
            fresults.write(line)
            fresults.write("\n")


if __name__ == '__main__':
    is_automated = IsAutomated()

    # may wanna use argparse with all files and conf, url, auth given as names arg
    conf_file_path = r"G:\temporary indement files\regression_scope\conf.json"
    data_file_path = is_automated.load_conf(conf_file_path)["data_file_path"]
    jira = JIRA(server=is_automated.load_conf(conf_file_path)["url"],
                basic_auth=is_automated.load_conf(conf_file_path)["auth"])

    print("Will take list of issues and verify if they are automated")

    # for issue_key in load_issue_list(load_conf(conf_file_path)["data_file_path"]): # not much readable
    # this loads results in memory and flushes them to file at once
    are_automated = {}
    for issue_key in is_automated.load_issue_list(data_file_path):
        are_automated[issue_key] = is_automated.is_automated_string(is_automated.get_response(jira, issue_key))
    is_automated.results_to_file(is_automated.load_conf(conf_file_path)["output_file"], are_automated, True)

    """
    # this updates file permanently
    for issue_key in is_automated.load_issue_list(data_file_path):
        is_automated.result_to_file(is_automated.load_conf(conf_file_path)["output_file"], 
        is_automated.is_automated_string((is_automated.get_response(jira, issue_key))))
    """
