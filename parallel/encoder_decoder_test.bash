#!/bin/bash

testImages="./testImages/t"
args_encoder_list=()

# 循环生成参数列表
for i in {1..19}; do
  image="${testImages}${i}"
  args_encoder_list+=("${image}.jpg ${image}")
done

# 循环执行 encoder.py
for args in "${args_encoder_list[@]}"; do
  python encoder.py ${args}
done

args_decoder_list=()

# 循环生成参数列表
for i in {1..19}; do
  image="${testImages}${i}"
  args_decoder_list+=("${image} ${image}_res.jpg")
done

# 循环执行 decoder.py
for args in "${args_decoder_list[@]}"; do
  python decoder.py ${args}
done
