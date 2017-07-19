#!/bin/bash

. ./cmd.sh
. ./path.sh

# step 1: generate fbank features
obj_dir=data/fbank

for x in test; do
  # rm fbank/$x
  mkdir -p fbank/$x

  # compute fbank without pitch
  steps/make_fbank.sh --nj 8 --cmd "run.pl" $obj_dir/$x exp/make_fbank/$x fbank/$x || exit 1;
  # compute cmvn
  steps/compute_cmvn_stats.sh $obj_dir/$x exp/fbank_cmvn/$x fbank/$x || exit 1;
done

# #step 2: offline-decoding
test_data=data/fbank/test
dir=exp/chain/tdnn

steps/nnet3/decode.sh --acwt 1.0 --post-decode-acwt 10.0 \
  --nj 4 --num-threads 1 \
  --cmd "$decode_cmd" --iter final \
  --frames-per-chunk 50 \
  $dir/graph $test_data $dir/decode_test

# # note: the model is trained using "apply-cmvn-online",
# # so you can modify the corresponding code in steps/nnet3/decode.sh to obtain the best performance,
# # but if you directly steps/nnet3/decode.sh, 
# # the performance is also good, but a little poor than the "apply-cmvn-online" method.
