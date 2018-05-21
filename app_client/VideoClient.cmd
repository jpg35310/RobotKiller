@echo off
echo Affichage du flux vidéo depuis Gstreamer
echo.
echo.
C:\gstreamer\1.0\x86_64\bin\gst-launch-1.0 -v udpsrc port=5001 caps="application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264" ! rtph264depay ! h264parse config-interval=96 ! avdec_h264 ! videoconvert ! autovideosink sync=False

pause