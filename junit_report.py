from flask import Flask, render_template
import os

import xml.etree.ElementTree as ET

app = Flask(__name__)

def parse_test_results(file_path):
    # parse the xml file 
    tree = ET.parse(file_path)
    # get the root element
    root = tree.getroot()

    test_suites = []
    #associate the test suite with the test cases found
    for testsuite in root.findall('testsuite'):
        suite = {
            'name': testsuite.get('name'),
            'tests': testsuite.get('tests'),
            'failures': testsuite.get('failures'),
            'errors': testsuite.get('errors'),
            'skipped': testsuite.get('skipped'),
            'time': testsuite.get('time'),
            'timestamp': testsuite.get('timestamp'),
            'hostname': testsuite.get('hostname'),
            #initialize the test cases dictionary for appending the test cases
            'testcases': []
        }
        # loop through the test cases to identify the test case name, class name, time taken and failure message
        for testcase in testsuite.findall('testcase'):
            case = {
                'classname': testcase.get('classname'),
                'name': testcase.get('name'),
                'time': testcase.get('time'),
                'failure': None
            }
            # check if the test case has a failure message
            failure = testcase.find('failure')
            if failure is not None:
                case['failure'] = failure.text
            #append the test case to the test cases as dictionary values
            suite['testcases'].append(case)
        #append the test suite to the test suites list
        test_suites.append(suite)

    return test_suites

@app.route('/')
def index():
    test_results_dir = os.path.join(os.path.dirname(__file__), 'test_results')
    # check if the test_results directory exists and 
    # read the xml files into a dictionary if it ends in .xml
    xml_files = [
        f for f in os.listdir(test_results_dir) 
        if f.endswith('.xml')
    ]
    # if not send prompt
    if not xml_files:
        return "No XML files found in the test_results directory."
    file_path = os.path.join(test_results_dir, xml_files[0])
    test_suites = parse_test_results(file_path)
    return render_template('index.html', test_suites=test_suites)

if __name__ == '__main__':
    app.run(debug=True)