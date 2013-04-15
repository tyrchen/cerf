#!/usr/bin/env python
"""
Usage:
    vint start <id>
    vint finish
    vint test
    
Options:
    -h, --help

"""
import json
from urlparse import urljoin
import requests

CONFIG_FILE = 'interview.json'
# Please provide a correct url which contains interview api.


from docopt import docopt
import os

class InterviewManager(object):
    interview_api_base = 'http://localhost:8000/api/interviews/'
    exam_api_base = 'http://localhost:'

    def __init__(self, id=None):
        self.id = id
        if self.id:
            self.exam_path = 'exam%s' % self.id
        else:
            self.exam_path = None
        self.code = None
        self.interview = None

    def get_interview_api_url(self, id):
        return urljoin(self.interview_api_base, str(id)) + '/'

    def get_exam_api_url(self):
        return urljoin(self.exam_api_base, str(self.interview['exam'])) + '/'

    def generate_interview_config(self):
        os.mkdir(self.exam_path)
        filename = os.path.join(os.getcwd(), self.exam_path, CONFIG_FILE)
        f = open(filename, 'w+')
        json.dump(self.interview, f)
        f.close()

    def generate_case(self, case):
        os.mkdir('case%s' % case['position'])

    def prepare_environment(self):
        self.generate_interview_config()

    def enter_environment(self):
        os.system('cd exam%s' % self.id)

    def start(self):
        code = raw_input('Please provide your authentication code:')
        self.code = code
        api = self.get_interview_api_url(self.id)
        r = requests.put(api, data={'authcode': code, 'action': 'start'})
        data = json.loads(r.text)
        if len(data) == 0:
            print('Can not retrieve proper interview by id %s. Please contact your hiring manager.' % self.id)
            exit(-1)

        self.interview = data

        print('Nice to meet you, %s! Thanks for your interest in Juniper China R&D.' % data['candidate'])
        print('Creating the exam environment...'),
        self.prepare_environment()
        print('Done!\nYou can start your exam now.')
        self.enter_environment()

    def finish(self):
        pass


def main(arguments):
    is_finish = arguments['finish']
    is_start = arguments['start']
    mgr = InterviewManager()
    # sanity check
    if is_finish:
        if os.path.exists(CONFIG_FILE):
            InterviewManager().finish()
        else:
            print('Please go to the exam directory then execute this command. If your exam directory is empty, you need to start the exam first.')
    elif is_start:
        try:
            id = int(arguments['<id>'])
        except:
            print('id is not valid.')
            exit(-1)

        InterviewManager(id).start()
    else:
        test()


def test():
    id = 1
    code = 'KZZ2NG'
    api = InterviewManager().get_interview_api_url(id)

    # reset the status
    requests.put(api, data={'authcode': code, 'action': 'reset'})



if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
