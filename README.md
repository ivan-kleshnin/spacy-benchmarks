# spaCy Benchmarks

Comparison of Spacy performance with different architectures, corpuses, hyperparams...

Current benchmarks:
- `Training time`
- `TAGG_ACC`
- `DEP_UAS`
- `DEP_LAS`
- `SENTS_F`

Global defaults:
- `nlp: batch_size = 512`
- `training: patience = 1000; max_steps = 5000`

## tok2vec.model depth

### Given

- Corpus: EWT + GUM + GENTLE, converted to CLEARNLP format, labels from `en_core_web_md`
- Ad hoc tokenizer
- Static Vectors: MD
- `tok2vec.model.embed: @architectures = MultiHashEmbed.v2`
- `tok2vec.model.encode: @architectures = MaxoutWindowEncoder.v2`
- `tok2vec.model.encode: width = 128`

### Test

- `tok2vec.model.encode: depth = 8 -> 6`

### Results

```
Training time: 1:08:17 -> 56:45
TAGG_ACC: 96.33 -> 96.44
DEP_UAS: 89.61 -> 89.53
DEP_LAS: 87.38 -> 87.22
SENTS_F: 80.92 -> 81.32
```

### Conclusion

Negligible difference, you shouldn't probably start with `depth = 8`.

## Architectures: MultiHashEmbed + MaxoutWindowEncoder vs HashEmbedCNN

### Given

- Corpus: EWT + GUM + GENTLE, converted to CLEARNLP format, labels from `en_core_web_md`
- Ad hoc tokenizer
- Static Vectors: MD
- `tok2vec.model.encode: width = 128; depth = 8`

### Test

- Remove `tok2vec.model.embed: @architectures = MultiHashEmbed.v2`
- Remove `tok2vec.model.encode: @architectures = MaxoutWindowEncoder.v2`
- Add `tok2vec.model: @architectures = HashEmbedCNN.v2` (with corresponding changes)

### Results

```
Training time: 1:08:17 -> 1:11:51
TAGG_ACC: 96.33 -> 96.21
DEP_UAS: 89.61 -> 89.20
DEP_LAS: 87.38 -> 86.92
SENTS_F: 80.92 -> 81.17
```

### Conclusion

Negligible difference. Both look like the same thing, just a bit different config syntax. 

## Architectures: MultiHashEmbed + MaxoutWindowEncoder vs TorchBiLSTMEncoder

### Given

- Corpus: EWT + GUM + GENTLE, converted to CLEARNLP format, labels from `en_core_web_md`
- Ad hoc tokenizer
- Static Vectors: MD
- `tok2vec.model.encode: width = 128; depth = 6`

### Test

- Remove `tok2vec.model.embed: @architectures = MultiHashEmbed.v2`
- Remove `tok2vec.model.encode: @architectures = MaxoutWindowEncoder.v2`
- Add `tok2vec.model.encode: @architectures = TorchBiLSTMEncoder.v1` (with corresponding changes)

### Results

```
Training time: 56:45 -> 58:59
TAGG_ACC: 96.33 -> 93.45
DEP_UAS: 89.53 -> 84.19
DEP_LAS: 87.22 -> 80.58
SENTS_F: 81.32 -> 72.73
```

### Conclusion

The accuracy is dropping, quite a lot. Retested with larger NN (see below).

## Architectures: MultiHashEmbed + MaxoutWindowEncoder vs TorchBiLSTMEncoder (2)

### Given

Same as above but:
- `tok2vec.model.encode: width = 192; depth = 8`

### Results

```
Training time: 58:59 -> 2:01:11
TAGG_ACC: 93.45 -> 89.40
DEP_UAS: 84.19 -> 82.65
DEP_LAS: 80.58 -> 77.91
SENTS_F: 72.73 -> 72.50
```

### Conclusion

The training time is double, the results are worse. Might be an undertraining case (`max_steps` capped to 5000).

## Larger Static Vectors

### Given

- Corpus: EWT + GUM + GENTLE, converted to CLEARNLP format, labels from `en_core_web_md`
- Ad hoc tokenizer
- `tok2vec.model.embed: @architectures = MultiHashEmbed.v2`
- `tok2vec.model.encode: @architectures = MaxoutWindowEncoder.v2`
- `tok2vec.model.encode: width = 128; depth = 8`

### Test

- Static Vectors: MD -> LG

### Results

```
Training time: 1:08:17 -> 1:08:54
TAGG_ACC: 96.44 -> 96.86
DEP_UAS: 89.61 -> 90.15
DEP_LAS: 87.38 -> 88.16
SENTS_F: 80.92 -> 81.60
```

### Conclusion

The accuracy is improving here.

## Larger Corpus

### Given

- Ad hoc tokenizer
- Static Vectors: MD
- `tok2vec.model.embed: @architectures = MultiHashEmbed.v2`
- `tok2vec.model.encode: @architectures = MaxoutWindowEncoder.v2`
- `tok2vec.model.encode: width = 128; depth = 6`

### Test

- Corpus 1: EWT
- Corpus 2: EWT + GUM

### Results

```
Training time: 1:08:17 -> 1:08:54
TAGG_ACC: 93.89 -> 95.11
DEP_UAS: 84.42 -> 85.86
DEP_LAS: 80.65 -> 82.39
SENTS_F: 76.90 -> 82.53
```

### Conclusion

The accuracy is improving here.
