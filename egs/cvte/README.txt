Copyright 2017- CVTE (http://www.cvte.com)
77;20003;0cAuthor: Yanqiang Lei
Email: leiyanqiang@cvte.com
QQ:415198468

=============================================================================================
This archive is provided by CVTE and contains the following features:
1) Acoustic model (chain,tdnn) trained with several thounsand of hours data;
2) Support online cmvn, since "apply-cmvn-online" is used during the training;
3) A 3-gram LM model is trained with 1000 GB text;
4) It is created by kaldi's master branch which is on May 02, 2017.

Files in this archive:
1) you should un-tar this inside the egs/ directory of kaldi;
2) create the soft-links, i.e., s5/steps, s5/utils, and s5/local/score.sh;
3) "conf" contains the fbank.conf used for feature extraction;
4) "data" contains ten utterances for testing;
5) "exp/chain/tdnn" includes the model;

Some results:
CVTE201701(1000 utts):       ppl 340;   cer: 4.55%
CVTE201703(10000 utts):      ppl 313;   cer: 4.5%
CVTE201705(5000 utts):       ppl 200;   cer: 15.7%
CVTE201705_02(7000 utts):    ppl 1000+; cer: 5.58%
THCHS30(2496 utts):          ppl 2000+; cer: 8.25%

Note: CVTE201705 is a very challenging test set with various noise and strong accent,
and the other CVTE sets are all recored by mobile phones or high-performance mics with standard Mandarin in office or quiet room.

=============================================================================================
How to use:
It is very easy to use these models, you can refer to "run.sh" in s5/ directory.
