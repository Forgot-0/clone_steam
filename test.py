import os
import shutil

def remove_pycache_dirs(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if dirname == '__pycache__':
                pycache_path = os.path.join(dirpath, dirname)
                shutil.rmtree(pycache_path)

if __name__ == "__main__":
    root_directory = '/home/forgot/all_project/clone_steam'
    remove_pycache_dirs(root_directory)

# docker compose -f docker_compose/app.yaml --env-file .env up --build -d

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'welcome2038@gmail.com'
EMAIL_HOST_PASSWORD = 'xzvh iibl nxtv rxek'
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'welcome2038@gmail.com'

