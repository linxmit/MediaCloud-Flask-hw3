import ConfigParser, logging, datetime, os

from flask import Flask, render_template, request

import mediacloud


CONFIG_FILE = 'settings.config'
basedir = os.path.dirname(os.path.realpath(__file__))

# load the settings file
config = ConfigParser.ConfigParser()
config.read(os.path.join(basedir, 'settings.config'))

# set up logging
log_file_path = os.path.join(basedir,'logs','mcserver.log')
logging.basicConfig(filename=log_file_path,level=logging.DEBUG)
logging.info("Starting the MediaCloud example Flask app!")

# clean a mediacloud api client
mc = mediacloud.api.MediaCloud( config.get('mediacloud','api_key') )

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("search-form.html")

@app.route("/search",methods=['POST'])
def search_results():
    keywords = request.form['keywords']
    startYear = request.form['startYear']
    IstartYear = int(startYear)
    startMonth = request.form["startMonth"]
    IstartMonth = int(startMonth)
    startDay = request.form["startDay"]
    IstartDay = int(startDay)
    endYear = request.form['endYear']
    IendYear = int(endYear)
    endMonth = request.form["endMonth"]
    IendMonth = int(endMonth)
    endDay = request.form["endDay"]
    IendDay = int(endDay)
    startDate = ""
    startDate = str(startYear) + '-' + str(startMonth) + '-' + str(startDay)
    startDate = str(startDate)
    endDate = ""
    endDate = str(endYear) + '-' + str(endMonth) + '-' + str(endDay)
    endDate = str(endDate)
    results = mc.sentenceCount(keywords,
        solr_filter=[mc.publish_date_query( datetime.date( IstartYear, IstartMonth, IstartDay), 
                                            datetime.date( IendYear, IendMonth, IendDay) ),
                     'media_sets_id:1' ],split = True, split_start_date = startDate, split_end_date = endDate)
    splitedResults = str(results['split'])
    splitedResults = splitedResults.split(',')
    dateSplited = ''
    countSplited = ''
    for splitedResult in splitedResults:
        #check if the string is date with 
        if (splitedResult[3] == '2')| (splitedResult[3] =='1'):
            dateSplited = dateSplited + splitedResult[3:13] + ','
            countSplited = countSplited + splitedResult[25:] + ','

    return render_template("search-results.html", 
        keywords=keywords, sentenceCount=results['count'], dateSplitedHTML=dateSplited, countSplitedHTML= countSplited )

if __name__ == "__main__":
    app.debug = True
    app.run()
