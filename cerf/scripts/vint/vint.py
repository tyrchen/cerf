#!/usr/bin/env python
"""
Usage:
    vint start <id>
    vint finish
    vint reset

Options:
    -h, --help

"""
from datetime import datetime
from dateutil import parser
import json
from urlparse import urljoin
import requests

EXAM_CONFIG_FILE = '.interview.json'
CASE_CONFIG_FILE = '.case.json'
FIRST_EXTENSIONS = ['.h']

HOSTNAME = 'http://localhost:8000'

INSTRUCTION_FILE = 'README'
# Please provide a correct url which contains interview api.

EXAM_INSTRUCTION_TEMPLATE = '''
Hello %(candidate)s, Welcome to exam %(name)s

%(description)s

Instructions:

1. Write the code as fast as you can. Optimize when you have further time.
2. Verify the correctness and robustness of your code with proper output. For example:

    int fabonacci(int n) {
        // your code bla bla bla
    }

    int main() {
        printf("fabonacci(%%d) = %%d\n", 10, fabonacci(10));
        assert(100 == fabonacci(10));
        printf("fabonacci(%%d) = %%d\n", 0, fabonacci(-1));
        assert(0 == fabonacci(-5));
    }
3. When you finish the exam, please go back to this directory (where you see this file), and execute "vint finish".
    This is very important to do so since we will time your exam and submit your result back to the hiring manager.

Start your journey now, pal!

'''

CASE_INSTRUCTION_TEMPLATE = '''

Case%(position)d: %(name)s

%(description)s

Instructions:

1. You need to code in %(lang)s, with acceptable extentisons: %(extentions)s.
2. You'd better to write down the code inside one file unless you find it is not readable.
'''

from docopt import docopt
import os


class InterviewManager(object):
    interview_api_base = HOSTNAME + '/api/interviews/'
    exam_api_base = HOSTNAME + '/api/exams/'
    answer_api_base = HOSTNAME + '/api/answers/'

    def __init__(self, id=None):
        self.id = id
        if self.id:
            self.exam_path = 'exam%s' % self.id
        else:
            self.exam_path = None
        self.code = None
        self.interview = None
        self.exam_id = None

    def get_interview_api_url(self, id=None):
        if not id:
            id = self.id
        return urljoin(self.interview_api_base, str(id)) + '/'

    def get_exam_api_url(self):
        return urljoin(self.exam_api_base, str(self.exam_id)) + '/'

    def write_file(self, filename, content):
        f = open(filename, 'w+')
        f.write(content)
        f.close()

    def generate_environment(self):
        # create exam dir
        os.mkdir(self.exam_path)

        # write .interview.json for further use
        filename = os.path.join(os.getcwd(), self.exam_path, EXAM_CONFIG_FILE)
        content = json.dumps(self.interview)
        self.write_file(filename, content)

        # retrieve exam and write general instruction file
        r = requests.get(self.get_exam_api_url())
        data = json.loads(r.text)
        if len(data) == 0:
            print('Can not retrieve proper exam by id %s. Please contact your hiring manager.' % self.exam_id)
            exit(-1)

        filename = os.path.join(os.getcwd(), self.exam_path, INSTRUCTION_FILE)
        content = EXAM_INSTRUCTION_TEMPLATE % {
            'candidate': self.interview['candidate'],
            'name': data['name'],
            'description': data['description'],
        }
        self.write_file(filename, content)

        # generate cases
        for case in data['cases']:
            self.generate_case(case)

    def generate_case(self, case):
        os.mkdir('%s/case%s' % (self.exam_path, case['position']))
        path = os.path.join(os.getcwd(), self.exam_path, 'case%s' % str(case['position']))

        # write .case.json for further use
        filename = os.path.join(path, CASE_CONFIG_FILE)
        content = json.dumps(case)
        self.write_file(filename, content)

        # write instruction
        instruction = os.path.join(path, INSTRUCTION_FILE)
        content = CASE_INSTRUCTION_TEMPLATE % {
            'position': case['position'],
            'name': case['name'],
            'description': case['description'],
            'lang': case['lang'],
            'extentions': case['extentions']
        }
        self.write_file(instruction, content)

        # write code
        ext = case['extentions'].split(',')[0].strip()
        filename = os.path.join(path, 'main%s' % ext)
        self.write_file(filename, case['code'])

    def prepare_environment(self):

        self.generate_environment()

    def enter_environment(self):
        os.chdir(self.exam_path)

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
        self.exam_id = self.interview['exam']

        print('Nice to meet you, %s! Thanks for your interest in Juniper China R&D.' % data['candidate'])
        print('Creating the exam environment...'),
        self.prepare_environment()
        print('Done!\nYou can "cd %s" to start your exam now.' % self.exam_path)

    def load_data(self, interview):
        self.id = interview['id']
        self.code = interview['authcode']
        self.interview = interview
        self.exam_id = interview['exam']
        self.exam_path = 'exam%d' % self.exam_id

    def get_valid_files(self, path, extentions):
        first_list = []
        second_list = []
        normal_list = []
        for root, dirs, files in os.walk(path):
            for f in files:
                for ext in extentions:
                    if f.endswith(ext):
                        normal_list.append(f)
                        break

        for f in normal_list:
            for ext in FIRST_EXTENSIONS:
                if f.endswith(ext):
                    first_list.append(f)
                    break
            else:
                second_list.append(f)

        return first_list, second_list

    def read_content(self, filename):
        return open(filename).read()

    def submit_case(self, case):
        path = os.path.join(os.getcwd(), 'case%s' % case['position'])
        print('\tSubmit case%s...' % case['position']),
        extentions = [ext.strip() for ext in case['extentions'].split(',')]
        first_list, second_list = self.get_valid_files(path, extentions)
        content = ''
        for name in first_list + second_list:
            s = '/* %s */\n\n%s' % (name, self.read_content(os.path.join(path, name)))
            content += s

        data = {
            'interview': self.id,
            'author': self.interview['candidate_id'],
            'case': case['cid'],
            'content': content
        }
        headers = {'Content-type': 'application/json', 'Accept': '*/*'}
        r = requests.post(self.answer_api_base, data=json.dumps(data), headers=headers)
        if r.status_code != requests.codes.created:
            print('Cannot submit case%s, please contact your hiring manager.' % case['position'])
            # do not bail out so that we could try the latter cases.
            # exit(-1)
        else:
            print('Done!')

    def submit_cases(self):
        path = os.getcwd()
        for root, dirs, files in os.walk('.'):
            for d in dirs:
                if d.startswith('case'):
                    config = open(os.path.join(path, d, CASE_CONFIG_FILE), 'r')
                    self.submit_case(json.load(config))

    def finish_interview(self):
        api = self.get_interview_api_url(self.id)
        r = requests.put(api, data={'authcode': self.code, 'action': 'finish'})
        data = json.loads(r.text)
        if len(data) == 0:
            print('Can not finish interview by id %s. Please contact your hiring manager.' % self.id)
            exit(-1)

    def finish(self):
        if not os.path.exists(EXAM_CONFIG_FILE):
            print('Please change to the root of the exam directory, then execute this command again.')
            exit(-1)

        # do not trust existing data, retrieve interview data from server again

        interview = json.load(open(EXAM_CONFIG_FILE))
        r = requests.get(self.get_interview_api_url(interview['id']), data={'authcode': interview['authcode']})
        interview = json.loads(r.text)
        self.load_data(interview)

        if interview['time_spent']:
            print('Your exam is over. Please stay tuned.')
            exit(-1)

        started = parser.parse(interview['started'])
        now = datetime.now()
        diff = now - started
        print('Thank you! Your exam is done! Total time spent: %dh%dm.' % (
            diff.seconds / 3600, (diff.seconds % 3600) / 60)
        )

        print('Submitting your code to generate report...')
        self.submit_cases()
        print('Done!')

        print('Notifying the hiring manager...'),
        self.finish_interview()
        print('Done!')

        print('Please wait for a short moment. If no one comes in 5m, please inform frontdesk.')


def main(arguments):
    is_finish = arguments['finish']
    is_start = arguments['start']
    # sanity check
    if is_finish:
        if os.path.exists(EXAM_CONFIG_FILE):
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
        reset()


def reset():
    id = 1
    code = 'KZZ2NG'
    mgr = InterviewManager(id)
    api = mgr.get_interview_api_url()
    os.system('rm -rf %s' % mgr.exam_path)

    # reset the status
    requests.put(api, data={'authcode': code, 'action': 'reset'})


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
