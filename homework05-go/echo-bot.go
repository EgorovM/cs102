package main

import (
	"log"
	"github.com/go-telegram-bot-api/telegram-bot-api"
    "net/http"
	"net/url"
	"github.com/PuerkitoBio/goquery"
	"fmt"
	"crypto/tls"
	"strings"
	"strconv"
	"time"
)

var access_token = "927855723:AAEbpZxyCvZAmrGpEMkuNvvAJvXVaznkeV0";

var days = []string{
	"/monday",
	"/tuesday",
	"/wednesday",
	"/thursday",
	"/friday",
	"/saturday",
	"/sunday",
};

func SliceIndex(el string, slice []string) int {
    for i := 0; i < len(slice); i++ {
        if slice[i] == el {
            return i
        }
    }
    return -1
}


func setHttpConfig(){
    proxyUrl, _ := url.Parse("http://198.98.58.178:8080")
    http.DefaultTransport = &http.Transport{
		Proxy: http.ProxyURL(proxyUrl),
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}
}

//
// func Listener(update Update){
//
// }

func getPage(week, group string) (*goquery.Document){
	week = "/" + week
	group = strings.ToUpper(group)
	domain := "https://www.ifmo.ru/ru/schedule/0/"
	url := domain + group + week + "/raspisanie_zanyatiy_" + group + ".htm"

	fmt.Println("request: ", url)
	page, err := goquery.NewDocument(url)
	if err != nil{
		fmt.Println("Error: ", err)
	}

	return page
}


func getScheduleByWeekDay(page *goquery.Document, day string) (string, []string, []string, []string){
	var times_list, locations_list, lessons_list []string
	var weekDay string;

	page.Find("table").Each(func(_ int, s *goquery.Selection){
	    // получаем ссылку из атрибута
	    if id, ok := s.Attr("id"); ok {
	         if id == day + "day"{

				 weekDay = s.Find(".day span").Text()

				 s.Find(".time span").Each(func(i int, time *goquery.Selection){
					 if i % 2 == 0{
						 times_list = append(times_list, time.Text())
					 }
				 })

				 s.Find(".room span").Each(func(_ int, location *goquery.Selection){
					 locations_list = append(locations_list, location.Text())
				 })

				 s.Find(".lesson dd").Each(func(_ int, lesson *goquery.Selection){
					 lessons_list = append(lessons_list, lesson.Text())
				 })
			 }
	    }
	})

	return weekDay, times_list, locations_list, lessons_list
}

func getSchedule(day, week, group string, near bool) string{
	page := getPage(week, group)
	dayNum := strconv.Itoa(SliceIndex(day, days) + 1)
	weekDay, times_list, location_list, lessons_list := getScheduleByWeekDay(page, dayNum)

	log.Printf("%q\n", times_list)
	log.Printf("%q\n", location_list)
	log.Printf("%q\n", lessons_list)

	rasp := weekDay + "\n"

	if near{
		timenow := time.Now()
		hour, minute := timenow.Hour(), timenow.Minute()

		var index int
		var lesTime string

		for i, time := range times_list{
			les_hour, _ := strconv.Atoi(time[:2])
			les_minute, _ := strconv.Atoi(time[2:4])

			if (les_hour == hour && les_minute > minute) || les_hour > hour{
				index = i
				lesTime = time
				break
			}
		}

		if index < len(times_list){
			rasp += lesTime + "," + location_list[index] + "\n" + lessons_list[index] + "\n\n"
		}else{
			tomorrow(group, true)
		}

	}else{
		for i, time := range times_list{
			rasp += time + "," + location_list[i] + "\n" + lessons_list[i] + "\n\n"
		}
	}

	return rasp
}

func tomorrow(group string, near bool) string{
	time := time.Now()
	_, week_int := time.ISOWeek()
	week := strconv.Itoa((week_int + 1) % 2 + 1)
	weekday := time.Weekday()

	newInd := (weekday + 1) % 7

	if newInd == 0{
		week = strconv.Itoa(((week_int + 1) % 2 + 1) % 2 + 1)
	}

	return getSchedule(days[newInd], week, group, near)
}

func main() {
    setHttpConfig()

    bot, err := tgbotapi.NewBotAPI(access_token)
	if err != nil {
		log.Panic(err)
	}

	bot.Debug = true

	log.Printf("Authorized on account %s", bot.Self.UserName)

	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60

	updates, err := bot.GetUpdatesChan(u)

	for update := range updates {
		if update.Message == nil { // ignore any non-Message Updates
			continue
		}
		log.Printf("[%s] %s", update.Message.From.UserName, update.Message.Text)

		var answer = "Введите /help для получения помощи"
		splitted := strings.Split(update.Message.Text, " ")

		if splitted[0] == "/help"{
			answer =
				"Список команд:\n" +
				"/all [group]\n" +
				"/[weekDay] [week] [group]\n" +
				"/tomorrow [group]\n" +
				"/near [group]\n"

		}else if SliceIndex(splitted[0], days) != -1{
			_, week_int := time.Now().ISOWeek()
			week := strconv.Itoa((week_int + 1) % 2 + 1)

			var day, group string

			if len(splitted) == 3{
				day, week, group = splitted[0], splitted[1],splitted[2]
			}else{
				day, group = splitted[0], splitted[1]
			}

			answer = getSchedule(day, week, group, false)

		}else if len(splitted) == 2{

			group := splitted[1]

			time := time.Now()
			_, week_int := time.ISOWeek()
			week := strconv.Itoa((week_int + 1) % 2 + 1)
			weekday := time.Weekday()

			if splitted[0] == "/near"{
				answer = getSchedule(days[weekday], week, group, true)
			}else if splitted[0] == "/tomorrow"{
				answer = tomorrow(group, false)

			}else if splitted[0] == "/all"{
				answer = ""

				log.Println("")
				for _, v := range days{
					answer += getSchedule(v, week, group, false);
				}
			}

		}

		log.Println("answer: ", answer)

		if answer == "\n"{
			answer = "Отдыхай)"
		}

		msg := tgbotapi.NewMessage(update.Message.Chat.ID, answer)

		bot.Send(msg)
	}
}
