1. create a symlink to the directory where your photos are stored and call it 'photos' in /var/www/slideshow

2. create a symlink to index-full.html and call it index.html in /var/www/slideshow

3. create a symlink from /etc/lighttpd/conf-available/99-photo-proxy.conf to
    same filename in /etc/lighttpd/conf-enabled/

	sudo ln -s ../conf-available/99-photo-proxy.conf /etc/lighttpd/conf-enabled/99-photo-proxy.conf
	sudo systemctl restart lighttpd

4. for enabling the systemd service:
   sudo systemctl daemon-reload
   sudo systemctl enable photo-resize-server.service
   sudo systemctl start photo-resize-server.service

5. to follow the log

    journalctl -u photo-resize-server.service -f

