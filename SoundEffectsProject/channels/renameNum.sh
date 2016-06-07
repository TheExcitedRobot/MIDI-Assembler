a=0
for i in *.wav; do
  new=$(printf "channel%02d.wav" "$a")
  old = $(printf "channel%02d.wav" "$a+1")
  printf $new,  $old   '\n'
  #mv -- "$i" "$new"
  let a=a+1
done
