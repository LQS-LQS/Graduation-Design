#!/bin/bash

testImages="./UCID_dada_set/t"
testImages="./data_set/"
testImages="./Images/agricultural/"
args_encoder_list=()

# 循环生成参数列表1
for i in {1..99}; do
  image="${testImages}${i}"
  image="${testImages}agricultural${i}"
  image="$(printf "%s%02d" "${testImages}agricultural" "$i")"
  args_encoder_list+=("${image}.tif ${image}")
done

# 循环执行 encoder.py
for args in "${args_encoder_list[@]}"; do
  python encoder.py ${args}
done

args_decoder_list=()

# 循环生成参数列表
for i in {1..99}; do
  image="${testImages}${i}"
  image="${testImages}agricultural${i}"
  image="$(printf "%s%02d" "${testImages}agricultural" "$i")"
  args_decoder_list+=("${image} ${image}_res.jpg")
done

# 循环执行 decoder.py
for args in "${args_decoder_list[@]}"; do
  python decoder.py ${args}
done
