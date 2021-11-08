import pandas as pd


with open('dummy.txt', 'r') as stigF:
    stig = stigF.readlines()

#columns for dataframe

columns = ['Group ID', 'Group Title', 'Rule ID', 'Severity',
           ' Rule Version (STIG-ID)', 'Rule Title', 'Legacy ID 1', 'Legacy Id 2', 'VulDiscuss', 'Check Content',
           'Needed Config', 'Fix text', 'Fix Config', 'CCI', 'config check', 'ConfigCommands']
dfstig = pd.DataFrame(columns=columns)

#conditionals

check = fix = goneThru = ccBool = False

#reduce time spent on first rows and false positives

i = 41
while i < len(stig):
    groupID = groupTitle = ruleId = severity = ruleVersion = ruleTitle = ""
    legacyId1 = legacyId2 = checkCon = vulDis = fixText = cci = ""
# Simple matching and reading down the text file
#

    if "Group ID" in stig[i]:
        groupID = stig[i][17:-1]
        i += 1
        goneThru = True
    if "Group Title" in stig[i]:
        groupTitle = stig[i][13:-1]
        i += 1
    if "Rule ID" in stig[i]:
        ruleId = stig[i][10:-1]
        i += 1
    if "Severity" in stig[i]:
        severity = stig[i][10:-1]
        i += 1
    if "Rule Version" in stig[i]:
        ruleVersion = stig[i][26:-1]
        i += 1
    if "Rule Title" in stig[i]:
        ruleTitle = stig[i][12:-1]
        i += 1
    if "Legacy ID" in stig[i]:
        legacyId1 = stig[i][11:-1]
        i += 1
    if "Legacy ID" in stig[i]:
        legacyId2 = stig[i][11:-1]
        i += 3
    if "Vulnerability Discussion" in stig[i]:
        vulDis = stig[i][27:-1]
        i += 3
        ccBool = True
    while ccBool:
        if "Check Content:" in stig[i]:
            checkCon = stig[i+1]
            i += 3
            ccBool = False
            check = True
            break
        i += 1
    neededConfig = ""
    while True and check:
        neededConfig += stig[i]
        if "Fix Text" in stig[i+2]:
            check = False
            i += 2
            break
        i += 1

    if "Fix Text" in stig[i]:
        fixText = stig[i][10:-1]
        fix = True
        i += 2
    fixConfig = ""
    while True and fix:
        if "CCI" in stig[i]:
            fix = False
            break
        fixConfig += stig[i]
        if "CCI" in stig[i+2]:
            fix = False
            i += 2
            break
        i += 1
    if "CCI" in stig[i]:
        cci = stig[i]
        i += 2

#makes sure we don't throw in a ton of rows for no reason

    if goneThru:
        temp = [groupID, groupTitle, ruleId, severity, ruleVersion, ruleTitle,
                legacyId1, legacyId2, vulDis, checkCon, neededConfig, fixText, fixConfig, cci, "", ""]
        dfstig = dfstig.append(pd.DataFrame([temp], columns=columns), ignore_index=True)
        goneThru = False
    i += 1

dfstig.to_pickle("pickledstig.pkl")