package main

import (
    "log"
    "github.com/go-echarts/go-echarts/charts"
    "net/http"
    "os"
)

var graphNodes = []charts.GraphNode{

}


func NetworkGet(userIds []int) ([][2]int){
    var edges [][2]int

    for i := 0; i < len(userIds); i++{
        for j := 0; j < len(userIds); j++{
            find := Find(GetFriendsIds(userIds[i]), userIds[j])

            if find{
                edges = append(edges, [2]int{i, j})
            }
        }
    }

    return edges
}


func PlotGraph() (*charts.Graph){
    parni := []int{364629895, 157476821, 194537108, 313489913, 336500287, 113647571, 251901608}

    for _, id := range parni{
        graphNodes = append(graphNodes, charts.GraphNode{Name: GetUserName(id)})
    }

    graph := charts.NewGraph()

	graph.SetGlobalOptions(charts.TitleOpts{Title: "Поиск сообществ"})
	graph.Add("graph", graphNodes, genLinks(parni),
		charts.GraphOpts{Force: charts.GraphForce{Repulsion: 8000}},
	)

	return graph
}


func genLinks(userIds []int) []charts.GraphLink {
    edges := NetworkGet(userIds)

    links := make([]charts.GraphLink, 0)

    for _, ed := range edges{
        links = append(links,
            charts.GraphLink{Source: graphNodes[ed[0]].Name, Target: graphNodes[ed[1]].Name})

    }

    return links
}


func Find(slice []int, val int) (bool) {
    for _, item := range slice {
        if item == val {
            return true
        }
    }
    return false
}


func graphHandler(w http.ResponseWriter, _ *http.Request) {
	page := charts.NewPage(orderRouters("graph")...)
	page.Add(
		PlotGraph(),
	)
	f, err := os.Create(getRenderPath("graph.html"))
	if err != nil {
		log.Println(err)
	}
	page.Render(w, f)
}
