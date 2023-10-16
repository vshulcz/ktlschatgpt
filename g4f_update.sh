REPO_URL='https://github.com/xtekky/gpt4free.git'
REPO_NAME='gpt4free'

if [ -d "g4f" ] 
then
    rm -rf "g4f"
fi

git clone --depth 1 $REPO_URL

cp -r $REPO_NAME/g4f g4f

rm -rf $REPO_NAME
rm -rf g4f/api g4f/gui
