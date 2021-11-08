import xml.etree.ElementTree as et
import pandas as pd

tree = et.parse('U_Cisco_IOS_Router_NDM_STIG_V2R2_Manual-xccdf.xml')
root = tree.getroot()

# for child in root:
#     print(child.tag,child.attrib)
columns = ['Group ID', 'Group Title', ' Rule Version (STIG-ID)', 'Rule Title',
           'Legacy ID 1', 'Legacy Id 2', 'VulDiscuss', 'Check Content',
           'Fix text', 'CCI', 'config check', 'ConfigCommands']
dfstig = pd.DataFrame(columns=columns)

groupID = groupTitle = ruleVersion = ruleTitle = ""
legacyId1 = legacyId2 = checkCon = vulDis = fixText = cci = ""

# need group.attrib here
#          Group ID
for group in root.iter('{http://checklists.nist.gov/xccdf/1.1}Group'):
    groupID = group.attrib

    # need tag title here
    #   Group Title
    for child in group:
        if "title" in child.tag:
            groupTitle = child.text

        # need tags: version, title, description, ident, ident, ident, fixtext
        for child1 in child:
            if "version" in child1.tag:
                ruleVersion = child1.text
            if "title" in child1.tag:
                ruleTitle = child1.text
            if "description" in child1.tag:
                vulDis = child1.text
            if "ident" in child1.tag:
                if "SV" in child1.text:
                    legacyId2 = child1.text
                if "CCI" in child1.text:
                    cci = child1.text
                else:
                    legacyId1 = child1.text
            if "fixtext" in child1.tag:
                fixText = child1.text

            #need tag check-content
            for child2 in child1:
                if "check-content" in child2.tag:
                    if "ref" in child2.tag:
                        pass
                    else:
                        checkCon = child2.text
    temp = [groupID, groupTitle, ruleVersion, ruleTitle,
            legacyId1, legacyId2, vulDis, checkCon, fixText, cci, "", ""]
    dfstig = dfstig.append(pd.DataFrame([temp], columns=columns), ignore_index=True)


dfstig.to_pickle("pickledstigXML.pkl")
dfstig.to_csv('stigXML.csv')