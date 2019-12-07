package main

import (
    "github.com/patrikeh/go-topics"
    "log"
)

func TopicalModeling(domains []string){
    var texts []string;

    for _, domain := range domains{
        texts = append(texts, TextsGet(domain, 10)...)
    }

    processor := topics.NewProcessor(
		topics.Transformations{topics.ToLower, topics.RemoveTwitterUsernames, topics.Sanitize, topics.MinLen,},
	)
    
	corpus := processor.AddStrings(topics.NewCorpus(), texts)

	lda := topics.NewLDA(&topics.Configuration{Verbose: true, PrintInterval: 500, PrintNumWords: 8})
	err := lda.Init(corpus, 2, 0, 0)

	_, err = lda.Train(1000)
    log.Println(err)
	lda.PrintTopWords(8)

}
