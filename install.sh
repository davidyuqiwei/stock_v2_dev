while read requirement; do
    if [ -z "$requirement" ] || [[ "$requirement" == \#* ]]; then
        continue
    fi
    echo $requirement
    pip install "$requirement" || true
done < requirements.txt

