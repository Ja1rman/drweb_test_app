import requests


url = "http://127.0.0.1:3000/api/file"


def post_test():
    local_file_to_send = 'tests/example_file.txt'
    with open(local_file_to_send, 'w') as f:
        f.write('I am a super file\n')

    files = [
        ('file', open(local_file_to_send, 'rb'))
    ]
    r = requests.post(url, files=files, auth=requests.auth.HTTPBasicAuth('aboba', 'abobas'))
    print(r.status_code)
    print(r.json())
    if r.status_code >= 200 and r.status_code < 300:
        return r.json()['hash']
    else:
        return ''


def get_test(file_hash):
    r = requests.get(url + f'?hash={file_hash}')
    print(r.status_code)
    print(r.content)


def delete_test(file_hash):
    r = requests.delete(url + f'?hash={file_hash}', auth=requests.auth.HTTPBasicAuth('aboba', 'abobas'))
    print(r.status_code)
    print(r.json())


file_hash = post_test()
print('======')
if file_hash != '':
    get_test(file_hash)
    print('======')
    delete_test(file_hash)
    print('======')
