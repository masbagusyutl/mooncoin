import requests
import json
import time
from datetime import datetime, timedelta

# Baca data dari file 'data.txt'
with open('data.txt', 'r') as file:
    account_data = file.readlines()

total_accounts = len(account_data)

def login(account):
    url_login = "https://moonapp-api.mooncoin.co/api/user/login"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "content-type": "application/json",
        "origin": "https://moon-app-mini.vercel.app",
        "referer": "https://moon-app-mini.vercel.app/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    }
    payload = {
        "data": account.strip(),  # Mengambil data payload dari setiap baris di 'data.txt'
        "refCode": ""
    }
    try:
        response = requests.post(url_login, headers=headers, json=payload)
        if response.status_code == 201:
            access_token = response.json().get('data', {}).get('accessToken', None)
            if access_token:
                print(f"Login sukses untuk akun ini")
                return access_token
        else:
            print(f"Login gagal untuk akun: {account.strip()} dengan status code: {response.status_code}")
    except Exception as e:
        print(f"Error saat login akun {account.strip()}: {str(e)}")
    return None

def get_account_info(access_token):
    url_info = "https://moonapp-api.mooncoin.co/api/user/me"
    headers = {
        "authorization": f"Bearer {access_token}",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    }
    try:
        response = requests.get(url_info, headers=headers)
        if response.status_code == 200:
            account_data = response.json().get('data', {})
            print(f"Informasi akun untuk user: {account_data.get('username')}")
            print(f"Balance: {account_data.get('balance')}")
            print(f"Ref Count: {account_data.get('refCount')}")
            print(f"Count Spin: {account_data.get('countSpin')}")

            # Jika ada spin yang tersisa, lakukan spin
            count_spin = account_data.get('countSpin', 0)
            if count_spin > 0:
                do_spin(access_token, count_spin)  # Lakukan spin sesuai jumlah yang tersisa
        else:
            print(f"Gagal mendapatkan informasi akun, status code: {response.status_code}")
    except Exception as e:
        print(f"Error saat mengambil informasi akun: {str(e)}")

def do_spin(access_token, count_spin):
    url_spin = "https://moonapp-api.mooncoin.co/api/spin"
    headers = {
        "authorization": f"Bearer {access_token}",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    }
    for spin in range(count_spin):
        try:
            response = requests.put(url_spin, headers=headers)
            if response.status_code == 200 and response.json().get('key'):
                print(f"Spin {spin+1} berhasil: {response.json().get('type')} - {response.json().get('amount')}")
            else:
                print(f"Gagal melakukan spin ke-{spin+1}, status code: {response.status_code}")
        except Exception as e:
            print(f"Error saat melakukan spin ke-{spin+1}: {str(e)}")
        time.sleep(2)  # Jeda 2 detik antar spin


def get_task_info(access_token):
    url_task = "https://moonapp-api.mooncoin.co/api/task"
    headers = {
        "authorization": f"Bearer {access_token}",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    }
    try:
        response = requests.get(url_task, headers=headers)
        if response.status_code == 200:
            task_data = response.json().get('data', [])
            print(f"Total tugas yang tersedia: {len(task_data)}")
            for task in task_data:
                print(f"Tugas: {task['title']} | Reward: {task['reward'][0]['amount']} {task['reward'][0]['type']} | Status: {'Selesai' if task['isCompleted'] else 'Aktif'}")
                if not task['isCompleted']:
                    # Coba selesaikan tugas jika belum selesai
                    complete_task(access_token, task['id'])
        else:
            print(f"Gagal mendapatkan informasi tugas, status code: {response.status_code}")
    except Exception as e:
        print(f"Error saat mengambil informasi tugas: {str(e)}")

def complete_task(access_token, task_id):
    url_complete_task = f"https://moonapp-api.mooncoin.co/api/task/check/{task_id}"
    headers = {
        "authorization": f"Bearer {access_token}",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    }
    try:
        response = requests.get(url_complete_task, headers=headers)
        if response.status_code == 200 and response.json().get('success'):
            print(f"Tugas berhasil diselesaikan.")
        else:
            print(f"Gagal menyelesaikan tugas, status code: {response.status_code}")
    except Exception as e:
        print(f"Error saat menyelesaikan tugas : {str(e)}")

def check_in(access_token):
    url_check_in = "https://moonapp-api.mooncoin.co/api/check-in"
    headers = {
        "authorization": f"Bearer {access_token}",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    }
    try:
        # Get check-in data
        response = requests.get(url_check_in, headers=headers)
        if response.status_code == 200 and response.json().get('success'):
            print(f"Data hadir: {response.json().get('data', {}).get('items', [])}")
            
            # Coba absen (PUT request)
            response_put = requests.put(url_check_in, headers=headers)
            if response_put.status_code == 200 and response_put.json().get('success'):
                print(f"Absen sukses pada tanggal: {response_put.json().get('data', {}).get('date')}")
            else:
                print(f"Gagal melakukan absen, status code: {response_put.status_code}")
        else:
            print(f"Gagal mendapatkan data hadir, status code: {response.status_code}")
    except Exception as e:
        print(f"Error saat check-in: {str(e)}")

def countdown(duration):
    print(f"\nHitung mundur {duration} detik dimulai...")
    while duration:
        mins, secs = divmod(duration, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        print(time_format, end='\r')
        time.sleep(1)
        duration -= 1


def process_accounts():
    print(f"Total akun yang diproses: {total_accounts}")
    
    for idx, account in enumerate(account_data, start=1):
        print(f"\nMemproses akun {idx} dari {total_accounts}: ")
        access_token = login(account)
        if access_token:
            get_account_info(access_token)
            get_task_info(access_token)  # Mengambil dan menyelesaikan tugas
            check_in(access_token)  # Check-in harian
        time.sleep(5)  # Jeda 5 detik antara proses akun

def main():
    while True:
        print(f"Mulai proses akun pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        process_accounts()
        print(f"\nSemua akun telah diproses. Menunggu 1 hari...")
        countdown(86400)  # 1 hari = 86400 detik

if __name__ == "__main__":
    main()
