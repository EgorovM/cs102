package main

import (
    "github.com/himidori/golang-vk-api"
    "strings"
    "strconv"
    "time"
    "sort"
)


func GetAge(user_id int) (int){
    var friend_ages []int

    client, _ := vkapi.NewVKClientWithToken(access_token, nil)
    friend_count, friends, _ := client.FriendsGet(user_id, 999)

    for i := 0; i < friend_count; i++{
        age, err := getAgeFromBDate(friends[i].BDate)

        if err == 1{
            friend_ages = append(friend_ages, age)
        }
    }

    return mean(friend_ages)
}


func getAgeFromBDate(bdate string) (int, int){
    var d, m, y int

    secInYear := 60 * 60 * 24 * 365
    year := strings.Split(bdate, ".")

    if len(year) == 3{
        d, _ = strconv.Atoi(year[0])
        m, _ = strconv.Atoi(year[1])
        y, _ = strconv.Atoi(year[2])

        bdateSec := time.Since(time.Date(y, time.Month(m), d, 0, 0, 0, 0, time.UTC)).Seconds()
        nowInSec := time.Since(time.Now()).Seconds()

        return (int(bdateSec) - int(nowInSec)) / secInYear, 1
    }

    return 0, 2
}


func mean(list []int) (int) {
    sort.Ints(list)

    return list[len(list) / 2]
}
