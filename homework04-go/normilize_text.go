package main

import (
    "strings"
    "github.com/tmdvs/Go-Emoji-Utils"
    "github.com/bbalet/stopwords"
)


func removeLinks(text string) (string){
    textArray := strings.Split(text, " ")

    for i := 0; i < len(textArray); i++{
        if strings.HasSuffix(textArray[i], ".ru") || strings.HasPrefix(textArray[i], "http"){
            textArray[i] = ""
        }
    }

    return strings.Join(textArray, " ")

}


func removeTrash(text string) string{
    trash := []string{".", ",", "?", "!", "-", "[", "]"}

    for _, s := range trash{
        text = strings.ReplaceAll(text, s, " ")
    }

    return text
}


func cleanText(text string) string{
    text = emoji.RemoveAll(text)
    text = removeLinks(text)
    text = removeTrash(text)
    text = stopwords.CleanString(text, "ru", true)

    return text
}


func TextsGet(domain string, count int) []string{
    texts := GetWallTexts(domain, count)

    for i, text := range texts{
        texts[i] = cleanText(text)
    }

    return texts
}
