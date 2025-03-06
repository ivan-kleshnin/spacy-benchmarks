# spaCy Benchmarks

Comparison of Spacy performance with different architectures, corpuses, hyperparams...

## tok2vec.model depth

### Given

- Corpus: EWT + GUM + GENTLE, converted to CLEARNLP format, labels from `en_core_web_md`.
- Ad hoc tokenizer.
- Static Vectors: MD.
- `tok2vec.model.embed: @architectures = MultiHashEmbed.v2`
- `tok2vec.model.encode: @architectures = MaxoutWindowEncoder.v2`
- `tok2vec.model.encode: width = 128`

### Test

- `tok2vec.model.encode: depth = 8 -> 6`

### Results

```
Training time: 1:08:16.50 -> 56:44.51
TAGG_ACC: 96.33 -> 96.44
DEP_UAS: 89.61 -> 89.53
DEP_LAS: 87.38 -> 87.22
SENTS_F: 80.92 -> 81.32
```

### Conclusion

Negligible difference, you shouldn't probably start with `depth = 8`.

## MultiHashEmbed + MaxoutWindowEncoder vs HashEmbedCNN

### Given

- Corpus: EWT + GUM + GENTLE, converted to CLEARNLP format, labels from `en_core_web_md`.
- Ad hoc tokenizer.
- Static Vectors: MD.
- `tok2vec.model.embed: @architectures = MultiHashEmbed.v2`
- `tok2vec.model.encode: @architectures = MaxoutWindowEncoder.v2`
- `tok2vec.model.encode: width = 128`
- `tok2vec.model.encode: depth = 8`

### Test

- `tok2vec.model: @archictuctes = HashEmbedCNN.v2` with corresponding changes.

### Results

```
Training time: 1:08:16.50 -> 1:11:50.61
TAGG_ACC: 96.33 -> 96.21
DEP_UAS: 89.61 -> 89.20
DEP_LAS: 87.38 -> 86.92
SENTS_F: 80.92 -> 81.17
```

### Conclusion

Negligible difference.
