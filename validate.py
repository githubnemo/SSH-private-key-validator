#!/usr/bin/env python

"""
Copyright 2011 Marian Tietz. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY <COPYRIGHT HOLDER> ''AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of <copyright holder>.
"""

import re

def validSSHprivateKey(text):
	"""
		Expects a SSH private key as string.
		Returns a boolean and a error message.

		If the text is parsed as private key successfully,
		(True,'') is returned. Otherwise,
		(False, <message describing the error>) is returned.
	"""

	if not text:
		return False, 'No text given'

	startPattern = re.compile("^-----BEGIN [A-Z]+ PRIVATE KEY-----")
	optionPattern = re.compile("^.+: .+")
	contentPattern = re.compile("^(.{64}$|.+[=]{1,2}$)")
	endPattern = re.compile("^-----END [A-Z]+ PRIVATE KEY-----")

	def contentState(text):
		for i in range(0, len(text)):
			line = text[i]

			if endPattern.match(line):
				if i == len(text)-1 or len(text[i+1]) == 0:
					return True, ''
				else:
					return False, 'At end but content coming'

			elif not contentPattern.match(line):
				return False, 'Wrong string in content section'

		return False, 'No content or missing end line'

	def optionState(text):
		for i in range(0,len(text)):
			line = text[i]

			if line[-1:] == '\\':
				return optionState(text[i+2:])

			if not optionPattern.match(line):
				return contentState(text[i+1:])

		return False, 'Expected option, found nothing'

	def startState(text):
		if len(text) == 0 or not startPattern.match(text[0]):
			return False, 'Header is wrong'
		return optionState(text[1:])

	return startState([n.strip() for n in text.split("\n")])



if __name__ == "__main__":
	import sys

	f = file(sys.argv[1],"r")

	print validSSHprivateKey(f.read())

	f.close()
