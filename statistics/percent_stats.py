from pymongo import MongoClient
import csv


def get_percent_stats(event_in, rumor_in):
    # Setup our connection to mongo.
    dbclient = MongoClient('z')

    #Ex.     Mongo.sydneysiege.hadley
    db = dbclient[event_in][rumor_in]

    total = db.count()

    # A function to take
    def get_count(code_level, code_name):

        if type(code_level) == type(code_name) != str:
            raise TypeError('Invalid code_level or code_name type: ' +str(type(code_level))+' and '+str(type(code_name)))

        field_name = 'codes.' + code_level
        query = {field_name: code_name}

        return db.find(query).count()

    def get_percent(code_level,code_name):

        if type(code_level) == type(code_name) != str:
            raise TypeError('Invalid code_level or code_name type: ' +str(type(code_level))+' and '+str(type(code_name)))

        field_name = 'codes.' + code_level
        query = {field_name: code_name}

        return float(db.find(query).count())/float(total)

    def get_overlap_count(first_code, second_code):
        if type(first_code) == type(second_code) != str:
            raise TypeError('Invalid code_level or code_name type: ' +str(type(first_code))+' and '+str(type(second_code)))
        query = {'$and':[{'codes.first_code':first_code}, {'codes.second_code':second_code}]}
        if get_count('second_code', second_code) == 0:
            return 0
        else:
            return float(db.find(query).count())/float((get_count('second_code', second_code)))

    def get_overlap_percent(first_code, second_code):
        if type(first_code) == type(second_code) != str:
            raise TypeError('Invalid code_level or code_name type: ' +str(type(first_code))+' and '+str(type(second_code)))
        query = {'$and':[{'codes.first_code':first_code}, {'codes.second_code':second_code}]}
        if get_count('first_code', first_code) == 0:
            return 0
        else:
            return float(db.find(query).count())/float((get_count('first_code', first_code)))

    def get_nothing(first_code):
        query = {'$and' : [{'codes.first_code': first_code}, {'codes.second_code' : []}]}
        if get_count('first_code', first_code) == 0:
            return 0
        else:
            return float(db.find(query).count()) / float(get_count('first_code', first_code))


    first_level = ['Affirm', 'Deny', 'Neutral', 'Unrelated', 'Uncodable']
    second_level = ['Implicit', 'Uncertainty', 'Ambiguity']


    with open(event_in+'_'+rumor_in+'_statistics.csv', 'wb') as f:
        f_writer = csv.writer(f)
        # Write headers
        f_writer.writerow(first_level + second_level)

        # Get the counts
        level_one_counts = [get_count('first_code', code) for code in first_level]
        level_two_counts = [get_count('second_code', code) for code in second_level]

        # Glue them together
        all_counts = level_one_counts + level_two_counts

        level_one_percents = [get_percent('first_code', code) for code in first_level]
        level_two_percents = [get_percent('second_code', code) for code in second_level]

        all_percents = level_one_percents + level_two_percents

        # Write them to the file
        f_writer.writerow(all_counts)
        f_writer.writerow(all_percents)

        totals_row = ['Total Tweets:', total]
        f_writer.writerow(totals_row)

        #new counts #dictionary compression with a list compression inside
        f_writer.writerow([])
        f_writer.writerow(['Cross-Tabulation by second level code'])
        lines = [[code]+ [get_overlap_percent(first_code, code) for first_code in first_level] for code in second_level]

        '''
        equivalent to:
        results = {}
        for first in first_level:
                results[first] = []
            for second in second_level:
                results[first = get_overlap_count(first, second)'''

        header = ['In Percents'] + first_level
        f_writer.writerow(header)

        for line in lines:
            f_writer.writerow(line)

        f_writer.writerow(['None']+[get_nothing(code) for code in first_level])

        f_writer.writerow([])
        f_writer.writerow(['Cross-Tabulation by first level code'])
        lines = [[first_code]+ [get_overlap_count(first_code, code) for code in second_level] for first_code in first_level]


        header = ['In Percents'] + second_level
        f_writer.writerow(header)

        for line in lines:
            f_writer.writerow(line)

    print 'Stats file generated.  Please upload to the drive.'

# Make dictionary of events with values = list of rumors and loop function over all of them

''' Event: Rumors
baltimore: church_fire, purse ? (only some tweets have been coded, ask someone about it)
sydneysiege: airspace, flag, hadley, lakemba, suicide
mh17: americans_onboard
WestJet_Hijacking: hijacking
'''
# Dictionary of events, Events are keys, values are list of rumors
events = {'baltimore':['church_fire'],'sydneysiege':['airspace','flag','hadley','lakemba','suicide'],'mh17':['americans_onboard'],'WestJet_Hijacking':['hijacking']}

for k in events.keys():
    for x in events[k]:
        get_percent_stats(k,x)








