for x in {0..9}*__*.wav; do
    mv "$x" "$(echo $x | cut -c7-)"
done

