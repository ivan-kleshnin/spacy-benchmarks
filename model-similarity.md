### CTeTex corpus

All errors: `Counter({'Heads': 869, 'Deps': 827, 'Tags': 675})`.
Conclusion: there's no single dominating source of errors.

- sm-md errors: `Counter({'Heads': 206, 'Deps': 202, 'Tags': 146}) => 554`
- md-lg errors: `Counter({'Heads': 211, 'Deps': 202, 'Tags': 160}) => 573`
- md-tr errors: `Counter({'Heads': 224, 'Deps': 214, 'Tags': 186}) => 624`
- lg-tr errors: `Counter({'Heads': 228, 'Deps': 209, 'Tags': 183}) => 620`

Conclusion: sm/md models' results are the most similar, md/tr results are the most different of the list (sm/tr weren't compared).

#### Mismatch example

`text = "Report on any water use amounts sold or given."`
- sm: `[(Report, 'VB'), (on, 'IN'), (any, 'DT'), (water, 'NN'), (use, 'NN'), (amounts, 'NNS'), (sold, 'VBN'), (or, 'CC'), (given, 'VBN'), (., '.')]`
- md: `[(Report, 'NN'), (on, 'IN'), (any, 'DT'), (water, 'NN'), (use, 'NN'), (amounts, 'NNS'), (sold, 'VBN'), (or, 'CC'), (given, 'VBN'), (., '.')]`
- lg: `[(Report, 'VB'), (on, 'IN'), (any, 'DT'), (water, 'NN'), (use, 'NN'), (amounts, 'NNS'), (sold, 'VBN'), (or, 'CC'), (given, 'VBN'), (., '.')]`
- tr: `[(Report, 'VB'), (on, 'IN'), (any, 'DT'), (water, 'NN'), (use, 'NN'), (amounts, 'NNS'), (sold, 'VBN'), (or, 'CC'), (given, 'VBN'), (., '.')]`

MD model treated `Report` word as an order, while other models treated that as a title.

### Gentle corpus with all the poetry cut-out

All errors: `Counter({'Heads': 2302, 'Deps': 2167, 'Tags': 1706})`
Conclusion: matches the previous, there's no single dominating source of errors.

- sm-md errors: `Counter({'Heads': 509, 'Deps': 478, 'Tags': 365}) => 1352`
- md-lg errors: `Counter({'Heads': 491, 'Deps': 470, 'Tags': 354}) => 1315`
- md-tr errors: `Counter({'Heads': 642, 'Deps': 596, 'Tags': 493}) => 1731`
- lg-tr errors: `Counter({'Heads': 660, 'Deps': 623, 'Tags': 494}) => 1777`

Conclusion: md/lg models' results are the most similar on this corpus, lg/tr results are the most different.  It's different from the previous test.

### Conclusion

For corpus generation it's reasonable to pick several:
- the most powerful models
- the most different models

lg/tr combination, therefore, looks adequate. These two models do not produce the same result, which is explainable and expected due to their architectural difference.
