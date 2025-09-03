# packet_generator

lazy shree :) write this down!


video conf nathaniel

https://googlechromelabs.github.io/chrome-for-testing/#stable

python webrtc.py --mode sender --server_ip [SERVER_IP] --server_port [SEVER_PORT] --call_duration [CALL_DURATION] --audio /opt/medias/elephants_dream/ED-CM-St-16bit.flac --video /opt/medias/elephants_dream/elephants_dream_1080p24.y4m

Start the nodejs handoff server:
npm run dev [sever_ip] [server_port]
2. Start the webrtc sender (these are my paramters):
   python webrtc.py --mode sender --server_ip localhost --server_port 3000 --call_duration 1000 --audio /opt/medias/elephants_dream/ED-CM-St-16bit.flac --video /opt/medias/elephants_dream/elephants_dream_1080p24.y4m
3. Start the webrtc receiver:
   python webrtc.py --mode receiver --server_ip localhost --server_port 3000 --call_duration 1000 --audio /opt/medias/elephants_dream/ED-CM-St-16bit.flac --video /opt/medias/elephants_dream/elephants_dream_1080p24.y4m
   Other notes:
   Make sure in webrtc.py, chrome options headless is turned on (uncommented)
   Make sure that CHROME_DRIVER is set to the path you downloaded the chrome driver from
   Make sure that chrome "binary_location" is set to path you installed chrome from
   (edited)