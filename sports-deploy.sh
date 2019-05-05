# run as root !
if [ `whoami` != 'root' ]; then
  echo "You should run as root."
  echo "$ sudo bash sports-deploy.sh"
  return 1
fi

# Reset & Clone
cd /opt/sports/sports-fes-entry-site2019
git add -A
git commit -m 'foo'
git reset --hard HEAD^
git pull origin master && \
echo "*** Cloned repository ***"

# Build
cd frontend
docker run -it --rm -v $PWD:/app node:11.4 /bin/bash -c "cd /app && npm install && npm run build" && \
echo "*** Build finished ***"

# Deploy
cp dist/* /opt/sports/html/ && \
echo "*** Deploy finished ***"

