a=1
for i in *.wav; do
  new=$(printf "drum%03d.wav" "$a")
  mv -- "$i" "$new"
  let a=a+1
done
