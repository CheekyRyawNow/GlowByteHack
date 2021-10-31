import threading


class VKThread(threading.Thread):
    def __init__(self, requests_number, vk):
        threading.Thread.__init__(self)
        self.users = []
        self.requests_number = requests_number
        self.vk = vk

    def run(self):
        self.users = self.vk.get_users()
        return self.users
