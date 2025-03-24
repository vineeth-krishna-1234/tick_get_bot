# create required folders
mkdir bin
mkdir bin/chrome

# download and move the chrome files
wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/linux64/chrome-linux64.zip
unzip chrome-linux64.zip
mv chrome-linux64/* bin/chrome/
rm -rf chrome-linux64
rm chrome-linux64.zip

# download and move the chrome driver files
wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip 
mv chromedriver-linux64/chromedriver bin/
rm -rf chromedriver-linux64
rm chromedriver-linux64.zip