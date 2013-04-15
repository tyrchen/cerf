# How to use this tool?

$ vint start <exam_id>

Please provide your authentication code: xYabd
Nice to meet you, Tyr Chen! Thanks for your interest in Juniper China R&D.
Creating the exam environment...Done!
You can start your exam now.

$ vint finish
Thank you! Your exam is done! Total time spent: 1h15m.
Notifying the hiring manager...Done!
Please wait for a short moment. If no one comes in 5m, please inform frontdesk.

$ vint-admin create-exam --template 60001
Creating exam tarball based on 60001...Done!
Created a new exam in 60001-copy. You can make proper change on it, 
then submit with "vint-admin upload-exam 60001-copy".

$ vint-admin upload-exam <dir>
Uploaded! The exam id is 60002.

$ vint-admin list
ID       Description
60001    Firewall test.
60002    Flow test.

$ vint-admin create-interview <exam-id>
Please specify candidate name: Tyr Chen
Interview has been created successfully!
Authenticate code for Tyr Chen is: zAxBI
Interview id is 100001.
Please provide it to the candidate for the code exam.
Your teammate can view interview via http://j-interview.com/interviews/100001/.

# Format of the vint exam

title: general exam for MTS4
created: Tyr Chen

description: This exam aims to see candidate's coding skill, problem solving skill, data structure skill and TCP/IP knowledge.
instruction: |
	Bla bla bla
cases:
	- desc: Giving the header node of a single link list, reverse it and return the header of the new list.
	  code: |
		#include <stdio.h>
		typedef struct {
			int value;
			struct Node *next;
		} Node;

		Node *reverse(Node *head) {
			// provide your functionality here.
		}

		int main() {
			// provide your code to test the reverse function (please provide useful output to indicate it is working).
		}
	- desc: Write a TCP server to calculate the Fabonacci sequence. Client code is provided, please write the server to make them work together.
	  code: |
	  	#include <stdio.h>
		#include <net.h>
		// blabla

	- desc: 

		

# misc

* make a pypi package for this.
	
