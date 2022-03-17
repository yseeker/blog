rm -rf docs
hugo
git config core.filemode false
git add .
git commit -m 'updated'
git push origin HEAD:master
