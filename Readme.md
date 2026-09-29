#Install python use these commands
yum install python -y
yum install pip -y
pip install flask
yum install nginx -y
Navigate to app directory
	pip install requirements.txt
Update nginx.conf with
	server {
    listen 80;
    server_name <Server_IP>;

    location / {
        proxy_pass http://127.0.0.1:8000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

systemctl enable nginx
systemctl start nginx

Run 
	gunicorn --bind 127.0.0.1:8000 app:app
Run 
	python app.py
