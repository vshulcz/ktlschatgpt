REPO_URL='https://github.com/xtekky/gpt4free.git'
REPO_NAME='gpt4free'

if [ -d "gpt4free" ] 
then
    rm -rf "gpt4free"
fi

git clone --depth 1 $REPO_URL
