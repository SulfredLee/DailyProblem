#/bin/sh
initialPath=`pwd`
donePath="${initialPath}/done_folder"
totalWorkers=4

mkdir -p "${donePath}"

# ======================================== Function
function convertTask(){
    local inputFile=$1
    local donePath=$2
    local srcType=$3
    local outputFile="${inputFile}_cht${srcType}"

    opencc -i "$inputFile" -o "$outputFile" -c /usr/share/opencc/s2hk.json

    # prepare to remove original files
    mv "$inputFile" "${donePath}"
}
# ======================================== Main
for src_type in "*.srt" "*.ass"; do
    echo "Conversion start: ${src_type}"

    readarray -d '' target_list < <(find "$initialPath" -type f -name "${src_type}" -print0)
    N=$totalWorkers
    curCount=0
    (
    for i in "${!target_list[@]}"; do
        ((curCount=curCount%N)); ((curCount++==0)) && wait
        echo "conversion progress: $(( i + 1 ))/${#target_list[@]}"

        convertTask "${target_list[$i]}" "${donePath}" "${src_type}" &
    done
    )

    echo "Conversion end: ${src_type}"
done
