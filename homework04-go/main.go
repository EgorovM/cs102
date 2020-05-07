package main


import (
	"net/http"
    "path"
    "log"

    "github.com/go-echarts/go-echarts/charts"
)


const (
	host   = "http://127.0.0.1:8000"
	maxNum = 50
)


var(
    routers = []router{
        {"graph", charts.RouterOpts{URL: host + "/", Text: "Cообщество"}},
    }
)

func orderRouters(chartType string) []charts.RouterOpts {
	for i := 0; i < len(routers); i++ {
		if routers[i].name == chartType {
			routers[i], routers[0] = routers[0], routers[i]
			break
		}
	}

	rs := make([]charts.RouterOpts, 0)
	for i := 0; i < len(routers); i++ {
		rs = append(rs, routers[i].RouterOpts)
	}
	return rs
}


func getRenderPath(f string) string {
	return path.Join("html", f)
}


type router struct {
	name string
	charts.RouterOpts
}


func logTracing(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Tracing request for %s\n", r.RequestURI)
		next.ServeHTTP(w, r)
	}
}


func main() {
    // TopicalModeling([]string{"itmoru","python"})
    http.HandleFunc("/", logTracing(graphHandler))

    log.Println("Run server at " + host)
	http.ListenAndServe(":8000", nil)
}
