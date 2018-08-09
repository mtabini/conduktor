cd client
source "$JENKINS_HOME/.jj-lib/nvm.bash"
npm install
npm run build
cd ..
cp -r client/static server/conduktor/
cd server/
vex build3 python3 setup.py -q sdist --dist-dir ../dist/
cd ..