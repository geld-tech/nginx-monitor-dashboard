#!/bin/sh
set -e

echo "### CLEANUP & CONFIGURE ###"
# Cleanup
rm -rf .local_dev/
mkdir .local_dev/
# Copy files
cp -r sources/server/ .local_dev/
cp -r sources/webapp/ .local_dev/
cd .local_dev/
# Replace place holders
find . -type f | xargs sed -i "s/__PACKAGE_NAME__/localdev/g"
find . -type f | xargs sed -i "s/__PACKAGE_DESC__/Running application locally/g"
find . -type f | xargs sed -i "s/__PACKAGE_AUTHOR__/geld.tech/g"
find . -type f | xargs sed -i "s/__VERSION__/0.0.1/g"
find . -type f | xargs sed -i "s/__DATE__/01-01-1970/g"

# Flask application, enforce no syntax errors or undefined names, and flags other issues
echo ""
echo "### PYTHON FLAKE8 ###"
cd server/
flake8 . --show-source --max-line-length=239 --max-complexity=10 --statistics --count
cd ..

# Build Vue application with DevTools enabled (Firefox or Chrome plugin)
echo ""
echo "### VUE DEVTOOLS ###"
cd webapp/
sed -i '/Vue.config.productionTip = false/a Vue.config.devtools = true' src/main.js

echo "### NPM INSTALL ###"
npm install

echo "### NPM LINT ###"
npm run lint

echo "### NPM AUDIT ###"
set +e     # Ignores a particular command
npm audit  2> /dev/null # Run conditionally as not installed on all systems
set -e     # Then return to normal failures on all errors

echo "### NPM BUILD ###"
npm run build
cd ..

# Prepare application
echo ""
echo "### PREPARE ###"
cd server/
mkdir templates/
mkdir static/
cp ../webapp/dist/*.html templates/
cp -r ../webapp/dist/static/* static/
cd ..
# Copy local config template if no configuration set (ignored via .gitignore)
if [ ! -f server/config/settings.cfg ]; then
    cp -p server/config/settings.cfg.template server/config/settings.cfg
fi

# Run background metrics collector
rm -f /dev/shm/monitor-collectord.sqlite3
cd server/
echo ""
echo "### METRICS COLLECTOR ###"
trap "python monitor-collectord.py stop" INT TERM
python monitor-collectord.py start
sleep 30

# Run application locally on port :5000 (Press CTRL+C to quit)
echo ""
echo "### RUN ###"
python application.py
