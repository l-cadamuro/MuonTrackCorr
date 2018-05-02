GLOB_FLDR="/eos/uscms/store/user/lcadamur/L1MuTrks_ntuples"

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "Usage:"
    echo "source makeFileList tag_name output_name"
    return
fi

LOCAL_FLDR=$1
ONAME=$2

FLDR=${GLOB_FLDR}/${LOCAL_FLDR}

if [ ! -d "$FLDR" ]; then
  echo "Folder $FLDR"
  echo "does not exist"
  return
fi

echo ".. listing files is $FLDR"

ls -1 -v ${FLDR}/output/*.root > ${ONAME}
echo "Read `cat ${ONAME} | wc -l` files", 
source replaceEOSserver.sh ${ONAME}