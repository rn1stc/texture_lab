spfile=`find . -name '*.spectralOut'`
echo $spfile
export HDF5_DISABLE_VERSION_CHECK=3
echo $HDF5_DISABLE_VERSION_CHECK
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo $DIR
export DIR
postResults --info $spfile > sp_info
python3 $DIR"/list_variables.py"
source sp_runpp.sh
python3 $DIR"/dam_avg.py"
python3 $DIR"/dtpp.py"