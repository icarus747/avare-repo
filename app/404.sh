tail /config/log/nginx/access.log | awk '/zip.+404/{print $7}' | awk -F '/' '{print $3}' >> config/limitdir/limit_list.tmp

sort -u /config/limitdir/limit_list.tmp > /config/limitdir/limit_list.db

python3 /app/repo_setup.py
sh /app/repo.sh