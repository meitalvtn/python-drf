import requests


def convert_to_satoshis(amount, currency):
    try:
        resp = requests.get(f'https://blockchain.info/tobtc?currency={currency}&value={amount}')
        if resp.status_code == 400:
            print(resp.content.decode())
            raise RuntimeError('Could not fetch with the data supplied.')
    except requests.exceptions.RequestException as e:
        print(e)
        raise RuntimeError('Error fetching request.')
    return resp.json() * 10 ** 8
