A website with python flask server implementing a slideshow which works on an iPad 2 running iOS 9 - plus any newer device. Uses very basic Javascript of the iOS 9 era.

Repurpose an iPad 2 as a digital photo frame where images are stored on your NAS or the web server host. Photos are not copied to the iPad making it easy to change the image list.

Developed on a Raspberry PI 2B using lighttpd, python, flask and libvips-tools.

The iPad 2 cannot handle down-scaling large photos, eg 8MB, to its native resolution of 1024 x 768 so the flask server downscales images on the fly (storing in a local cache) if a device running iOS 9 is making the request.

iPad:
  Swipe Left:  Previous Image
  Swipe Right: Next Image
  Double Tap:  Pause / Play

Non-iPad Web Browser:
  Left Arrow:  Previous Image
  Right Arrow: Next Image
  Space Key:   Pause / Play

Instructions: (assuming lighttpd web server on Debian / Raspberry Pi OS / DietPi)

1. sudo apt install libvips-tools (used for fast image downscaling)

2. Copy the www/slideshow directory contents to /var/www/slideshow

3. Copy the systemd service file and lighttpd configuration file to their respective locations.

4. create a symlink to the directory where your photos are stored and call it 'photos' in /var/www/slideshow

5. create a symlink to index-full.html and call it index.html in /var/www/slideshow

6. create a symlink from /etc/lighttpd/conf-available/99-photo-proxy.conf
       sudo ln -s ../conf-available/99-photo-proxy.conf /etc/lighttpd/conf-enabled/99-photo-proxy.conf
       sudo systemctl restart lighttpd

7. for enabling the systemd service:
       sudo systemctl daemon-reload
       sudo systemctl enable photo-resize-server.service
       sudo systemctl start photo-resize-server.service

       to test a regular browser request: (the journal will show serving original image)
         curl -I http://localhost:5005/slideshow/photos/IMG_0001.JPG
   
       to test an iPad 2 browser request: (the journal will show serving resized image)
         curl -I "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G36 Safari/601.1" http://127.0.0.1:5005/photos/IMG_0006.JPG

9. to follow the log

       journalctl -f -u photo-resize-server.service

   

