for x in *__*.wav; do
    mv "$x" "$(echo $x | cut -c7-)"
done

