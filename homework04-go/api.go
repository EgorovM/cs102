package main

import (
    "github.com/himidori/golang-vk-api"
)

func GetWallTexts(domain string, count int) ([] string){
    var texts []string

    client, _ := vkapi.NewVKClientWithToken(access_token, nil)

    wall, _ := client.WallGet(domain, count, nil)

    for i := 0; i < count; i++{
        texts = append(texts, wall.Posts[i].Text)
    }

    return texts
}


func GetFriendsIds(user_id int) ([]int){
    var friendsList []int;

    client, _ := vkapi.NewVKClientWithToken(access_token, nil)
    _, friends, _ := client.FriendsGet(user_id, 999)

    for _, friend := range friends{
        friendsList = append(friendsList, friend.UID)
    }

    return friendsList
}


func GetUserName(id int) string{
    client, _ := vkapi.NewVKClientWithToken(access_token, nil)

    users, _ := client.UsersGet([]int{id})

    return users[0].FirstName
}
