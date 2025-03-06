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

The accuracy is dropping, quite a lot. Retested with larger NN (see below). Might be an undertraining case (`max_steps` capped to 5000).

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

The training time is doubling, the accurace is degrading. Might be an undertraining case (`max_steps` capped to 5000).

## Architectures: TorchBiLSTMEncoder with more training time (3)

### Given

- Corpus: EWT + GUM + GENTLE, converted to CLEARNLP format, labels from `en_core_web_md`
- Ad hoc tokenizer
- Static Vectors: MD
- `tok2vec.model.encode: width = 128; depth = 6`

### Test

- Update `training: max_steps = 5000 -> 10000`, same `patience = 1000`.

### Results

```
Training time: 58:59 -> 2:14:14
TAGG_ACC: 89.40 -> 95.50
DEP_UAS: 82.65 -> 87.75
DEP_LAS: 77.91 -> 85.08 
SENTS_F: 72.50 -> 76.93
```

### Conclusion

The accuracy has improved. While the progress slowed down, it probably could continue. We got literally +1 extra hour of training for a couple of extra % of accuracy.

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

## Pretraining

### Given

- Corpus: EWT + GUM + GENTLE, converted to CLEARNLP format, labels from `en_core_web_md`
- Ad hoc tokenizer
- Static Vectors: MD
- `tok2vec.model.encode: width = 128; depth = 6`

### Test

- `spacy pretrain` on 500 sentences. Loss: 42K -> 32K.
- `spacy train` using the pretrained weights.
- `spacy pretrain` on 2500 sentences. Loss: 42K -> 29K.
- `spacy train` using the pretrained weights.

### Results

No measurable benefits. NN starts from higher scores (Epoch 0) but flattens to the same numbers as without pretraining.

### Conclusion

Probably due to limited size of pretraining corpus.
