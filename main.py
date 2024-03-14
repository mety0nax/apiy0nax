import os
import fastapi

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                             #
#              Constants and other global things              #
#                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Initializing fastAPI without access to the documentation
apiApp = fastapi.FastAPI(docs_url = None)

# API Key for security measures
apikey = '38d7f633e0111ce302de5b477a1d133a7b5c8d309024caf91ae9c19b363ef475'
keys_file = './keys/Keys'
keys_used_file = './keys/KeysUsed'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                             #
#                       Util Functions                        #
#                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Documentation
def validate_apikey(ak):
  return True if ak == apikey else False

# Documentation
def check_dek(dek):
  keys_database = [ l.strip( ) for l in open(keys_file , 'r').readlines( ) ]
  for line in keys_database:
    if dek == line:
      return True
  return False

def dek_used(dek):
  if os.path.exists(keys_used_file):
    used_keys_database = [ l.strip( ) for l in open(keys_used_file, 'r').readlines( ) ]
    for line in used_keys_database:
      if dek == line.split(';')[0]:
        return True
  return False

def add_dek_guid(dek, guid):
  with open(keys_used_file, 'a') as used_keys_fd:
    used_keys_fd.write(f'{dek};{guid}\n')

def check_dek_and_guid_match(dek, guid):
  used_keys_database = [ l.strip( ) for l in open(keys_used_file, 'r').readlines( ) ]
  for line in used_keys_database:
    dek_used, guid_assigned = line.split(';')
    if guid.strip( ) == guid_assigned:
      return True
  return False

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                             #
#                      Server Functions                       #
#                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Rewriting reply for '/' request (root of the server)
@apiApp.get('/')
async def server_root(apk: str, dek: str, guid: str):
  if not validate_apikey(apk):
    return {'info': 'Wrong API Key'}

  if check_dek(dek):
    if not dek_used(dek):
      add_dek_guid(dek, guid)
      return {'info': 'New Registration'}
    elif check_dek_and_guid_match(dek, guid):
      return {'info': 'Registered'}
    else:
      return {'info': 'Key in Use'}
  else:
    return {'info': 'Wrong Key'}

  return {'info': 'None'}
  