from django.shortcuts import render
import re
from queue import PriorityQueue

def index (request):
    allO={}
    Graph={}
    straight_line ={}
    for x in request.POST:
        if(re.search('[0-9]', x) and request.POST.get(x) !=""):
          allO[x]=request.POST[x]
     
    def create(city):
        mycity=city+"toCity[0-9]{1,}cost$"
        heuristic="heuristic"+city
        boss={}
        for x in allO.keys():
            if(re.search(heuristic, x)):
                straight_line[allO[city].strip()]=int(allO[x].strip())
            if(re.search(mycity, x)):
                boss[allO[x[:(len(x)-4)]].strip()]=int(allO[x].strip())
        if not Graph.get(allO[city]):
            Graph[allO[city].strip()]=boss
        return
    
    for x in allO.keys():
        if(re.search("^City[0-9]{1,}$", x.strip())):
            for q in Graph.keys():
                if q.strip()==allO[x].strip():
                    continue
            create(x)
    def a_star(source, destination):
    
     p_q,visited = PriorityQueue(),{}
     p_q.put((straight_line[source], 0, source, [source]))
     visited[source] = straight_line[source]
     while not p_q.empty():
        (heuristic, cost, vertex, path) = p_q.get()
        if vertex == destination:
           return heuristic, cost, path
        for next_node in Graph[vertex].keys():
            current_cost = cost + Graph[vertex][next_node]
            heuristic = current_cost + straight_line[next_node]
            if not next_node in visited or visited[next_node] >= heuristic:
                visited[next_node] = heuristic
                p_q.put((heuristic, current_cost, next_node,path + [next_node]))
    
    def main():
     try:
      source=request.POST.get("sour")
      destination=request.POST.get("des")
      if len(Graph)==0:
           return "" 
      elif source not in Graph or destination not in Graph:
        s="CITY DOES NOT EXIST."
        return s
      else:
        heuristic, cost, optimal_path = a_star(source, destination)
        s="min of total heuristic_value ="+str(heuristic)+"\n"+"total min cost ="+str(cost)+"\nRoute:\n"+" -> ".join(city for city in optimal_path)
        return s
     except Exception as e:
         return "Wrong!! please make sure you entre all cities with their info"
    main()
    return render(request,'index.html',{'result':main()})