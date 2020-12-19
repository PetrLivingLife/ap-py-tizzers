"""pip install jira"""
from jira import JIRA

auth = ("pszturc", "heslo")
jira = JIRA(server="https://bugs.casenetllc.com:9093", basic_auth=auth)
# joptions = {'server':"https://bugs.casenetllc.com:9093", 'verify':"False"}
# jira = JIRA(joptions, auth)

with open('g:\\temporary indement files\\regression_scope\\issue_list.txt', 'r') as fin:
    issue_list = fin.read().splitlines()

with open('g:\\temporary indement files\\regression_scope\\isautomatedlist.txt', 'w+') as fout:
    for item in issue_list:
        if jira.issue(item).fields.customfield_14660 is not None:
            if jira.issue(item).fields.customfield_14660.value == "Automated":
                fout.write(item)
                fout.write("\n")
