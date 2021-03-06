"""
    INPUT: aoi xml file
    OUTPUT:
    ontrans/atlsOnTrans20170101.csv to atlsOnTrans20170130.csv which has all transactions with
    atlas applied


"""



import glob
import pandas as pd
import os.path

def ParseAOI(xml):

    # Open xml and pass it to var content
    with open(xml, 'r') as content_file:
        content = content_file.read()

    """
    Extract atlas score, status, included or excluded status
    The parsing method is very specific suitable to the aoi transaction data xml
    and may not work for other xml fiels or if the aoi xml structure changed

    """

    # res array holds each transaction as elements
    res = []
    # each transaction
    subres = []

    # Split to construct transactions
    for w in content.split(">"):
        if "<" in w and '' != w.split("<")[0]:
            values = w.split("<")[0]
            if values.isdigit():
                res.append(subres)
                subres = []
            subres.append(values)

    # Extract into list

    # agents included in each transaction
    includes = [x for x in res if len(x) == 4]
    # agents exluded in each transaction
    excludes =  [x for x in res if len(x) > 4][1:]
    # number of transactions
    num_trans = len([x for x in includes if x[0] == '1'])
    # number of transactions with atlas score on
    num_ats_on = len([x for x in includes if x[0]=='1' and x[3] == 'true'])
    # number of transactions with atlas score off
    num_ats_off = len([x for x in includes if x[0]=='1' and x[3] == 'false'])

    return res,includes,excludes,num_trans,num_ats_on,num_ats_off

if __name__ == '__main__':

    # Fetch all the xml files in the directory
    xmlFiles = glob.glob("*xml")

    # Set saving path
    save_path = 'ontrans/'

    # Parse xml files iteratively
    for xml in xmlFiles:

        date = xml.split('_')[1] # Get the date

        res,includes,excludes,num_trans,num_ats_on,num_ats_off = ParseAOI(xml) # Pasre xml

        # Construct a df to store includes
        dfincludes = pd.DataFrame(includes,columns = ['Pos','ATLS_SCORE','ASSOC_ID','ATLS_APPLIED'])

        # Include date column
        dfincludes['Date'] = date

        # Array to hold counting of transaction numbers
        transnums = []

        # Get list of agents whose atlas score is applied
        # df_on = dfincludes[dfincludes.ATLS_APPLIED == 'true']

        # Parse all records regardless of atlas applied status
        df_on = dfincludes

        ## Counting transaction numbers

        # Initiate transaction
        transnum = 1

        # If the pos increase all the way till it decreases, all the previous records belong to one transaction
        for i in range(1, df_on.shape[0]):
            
            if float(df_on['Pos'].iloc[i]) <= float(df_on['Pos'].iloc[i-1]):
                transnum += 1        
            transnums.append(transnum)

        # Insert 1
        transnums =  [1] + transnums

        # Pass the array to the df column
        df_on['Trans'] = transnums

        # Save the atlas-on-transaction data to csv
        filename = 'atlsAllTrans' + date + '.csv'
        # saving file path
        compfilename = os.path.join(save_path,filename )
        # save df
        df_on.to_csv(compfilename,index = None)
        # print out
        print 'saved file: ' + filename
        


