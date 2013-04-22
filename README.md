cerf - simple code examination software
====

## What is cerf?

cerf is a clean and simple live code exam tool. It enables team to hiring high quality coders.

## Ideas behind cerf

Let's see a typical scenario on live code exam (vint below is a CLI tool along with cerf service):

1. Hiring manager generate an exam (through a list of existing exams) for a applicant via admin interface.
The system return an instruction page including exam id and authentication code. Hiring manager prints it out.
2. When applicant comes, she will receive a print instruction from hiring manager.
3. She starts the exam by “vint start <exam_id>”. This will grab the predefined exam and generate the exam
environment. (actually a folder containing instructions, code to work with, etc.)
5. She then works on the cases with editors(vim/emacs), parser or compilers(python, ruby or gcc/gdb/binutils)
and other tools.
6. After the exam is done, she could issues “vint finish” to finish the code exam. The data (code she wrote
plus the environment) will be submitted to the server. Server will then generate the exam report with proper
syntax highlighting.

![Vint & Cerf](https://raw.github.com/tyrchen/cerf/master/cerf/static/cerf/img/prototype/vint.jpg)

## How to use cerf

### For Hiring Managers

Currently you have to create exam case, exam and interview via admin interface. The frontend UI is under its way.
Please stay tuned.


#### Creating Interview

An interview is tie to an exam. A exam has several cases you want to test for the applicant. You can choose from 
existing exams, or create a new one.

#### Preparing Environment

I suggest you to use a ubuntu as the interview environment. Basically all linux distribution and osx should work 
as well (but I haven't tested them). If this is the first time to build the environment you need to run 
```
$ pip install vint
```
to ge the CLI work. Then for any interview you created, there's a instrucion page for you to create the exam 
environment. You can print it and hand it over to the applicant, or you can create the exam yourself right before
the exam (the exam is timed so don't start it too early).

### For Hiring Team

You can view the exam result from the interview page once the exam is done (all exam data is uploaded).

## Installation

### Mysql

You need the latest version of mysql server as the database server for cerf. To install mysql:

Ubuntu:
```
$ sudo apt-get install mysql-server
```

OSX with homebrew:
```
$ brew install mysql
```

For windows and other platforms, please refer to the related documents.

### bower

Twitter bower is used for managing the javascript components. To install bower, you need to install node first:

Ubuntu:
```
$ sudo apt-get install node
```

OSX with homebrew:
```
$ brew install node
```

Then you can install bower with npm: ```npm install -g bower```.

### cerf

It is fairly easy to install cerf:

1. Clone the repo: ```git clone git://github.com/tyrchen/cerf.git; cd cerf```
2. Create virtualenv: ```virtualenv --no-site-packages ~/.virtualenvs/cerf```
3. Activate the venv: ```source ~/.virtualenvs/cerf```
4. Install requirements: ```pip install -r requirements.txt```
5. Retrieve javascript dependencies: ```cd cerf; bower install; cd ..```
6. Collect static files: ```./manage.py collectstatic```
7. Initialize database: ```./manage.py syncdb; ./manage.py migrate```

You're all set. Now try ```./manage.py runserver``` and start your chrome to play with it.

## License

cerf is licensed under the MIT License.

## Issues

In case you find any issue using the software, please submit it in: [https://github.com/tyrchen/cerf/issues](https://github.com/tyrchen/cerf/issues).

## Contributors

cerf is designed and implemented by @tyrchen. For more information about the author, please visit: http://tchen.me/pages/aboutme.html

You can add your name below once you made contribution to it.