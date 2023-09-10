#!/bin/bash

variables=("agricultural" "airplane" "baseballdiamond" "beach" "buildings" "chaparral" "denseresidential" "forest" "freeway" "golfcourse" "harbor" "intersection" "mediumresidential" "mobilehomepark" "overpass" "parkinglot" "river" "runway" "sparseresidential" "storagetanks" "tenniscourt")
variables=("agricultural")
testImages="./data_set/"
testImages="./Images/"
testImages="./UCID1338/"
args_encoder_list=()

# 循环生成参数列表
# for variable in "${variables[@]}"; do
#   for i in {1..99}; do
#     image="${testImages}${i}"
#     image="${testImages}forest${i}"
#     image="$(printf "%s%02d" "${testImages}forest" "$i")"
#     image="$(printf "%s%02d" "${testImages}${variable}/${variable}" "$i")"
#     args_encoder_list+=("${image}.tif ${image}qq___")
#   done
# done

# 循环生成参数列表
for i in {1..1339}; do
  image="${testImages}${i}"
  args_encoder_list+=("${image}.tif ${image}")
done


# 循环执行 encoder.py
for args in "${args_encoder_list[@]}"; do
  python encoder.py ${args}
done

args_decoder_list=()

# 循环生成参数列表
for i in {1..1339}; do
  image="${testImages}${i}"
  args_decoder_list+=("${image} ${image}_res.jpg")
done

# 循环执行 decoder.py
for args in "${args_decoder_list[@]}"; do
  python decoder.py ${args}
done
