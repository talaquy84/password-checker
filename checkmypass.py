import hashlib
import requests
import sys

def getPasswordData(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check API!')
    return res

def getPasswordLeaks(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def checkPasswordAPI(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = getPasswordData(first5_char)
    return getPasswordLeaks(response, tail)

def main(args):
  for password in args:
    count = checkPasswordAPI(password)
    if count:
      print(f'Password \'{password}\' was found {count} times in the internet!')
    else:
      print(f'{password} was NOT found. Strong password!')
  return 'Password checking is done!'

#Only run if this is main
if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))