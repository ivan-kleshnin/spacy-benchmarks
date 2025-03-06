# spaCy Benchmarks

Comparison of Spacy performance with different architectures, corpuses, hyperparams...

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

Negligible difference, you shouldn't probably start with `depth = 8`

## MultiHashEmbed + MaxoutWindowEncoder vs HashEmbedCNN

### Given

- Corpus: EWT + GUM + GENTLE, converted to CLEARNLP format, labels from `en_core_web_md`
- Ad hoc tokenizer
- Static Vectors: MD
- `tok2vec.model.encode: width = 128`
- `tok2vec.model.encode: depth = 8`

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

## MultiHashEmbed + MaxoutWindowEncoder vs TorchBiLSTMEncoder

### Given

- Corpus: EWT + GUM + GENTLE, converted to CLEARNLP format, labels from `en_core_web_md`
- Ad hoc tokenizer
- Static Vectors: MD
- `tok2vec.model.encode: width = 128`
- `tok2vec.model.encode: depth = 6`

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

Performance is dropping quite a lot. Retested with larger NN (see below).


