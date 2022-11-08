packs=('../flake8-unfinished')
py=python3.8
ezdir=$(pwd)
venv="$ezdir/venv"
exe="$venv/bin/python"

if [ "$1" = 'setup' ]; then
  echo "Creating venv at $venv..."
  $py -m venv "$venv"
  $exe -m pip install -U pip setuptools wheel
  echo "Installing pytest to venv..."
  $exe -m pip install -U pytest
  echo "Installing $ezdir to venv..."
  $exe -m pip install -e "$ezdir"

  for pack in ${packs[@]}; do
    echo "Installing $pack to venv..."
    $exe -m pip install -e "$pack"
  done

else
  for pack in ${packs[@]}; do
    echo "Running tests for $pack..."
    $exe -m pytest "$pack" $@
  done

fi
echo "Done"
