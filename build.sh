echo "remove old file"
rm -r dist build

echo "install api"
pyinstaller api.spec
echo "install main"
pyinstaller main.spec
echo "install model"
pyinstaller model.spec

echo "copy api"
cp -rn dist/api/* dist/main
echo "copy model"
cp -rn dist/ModelMain/* dist/main

echo "make dirs"
mkdir -p dist/main/datasets
mkdir -p dist/main/deploy
mkdir -p dist/main/projects

echo "prepare dataset"
cp -r SALA_demo_data/Small_VL dist/main/datasets/
echo "prepare project"
cp -r SALA_demo_data/Demo dist/main/projects/
echo "prepare pretrained weight"
cp -r SALA_demo_data/PretrainedWeight dist/main/sample