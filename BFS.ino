int nodes[][3][4] {//{{nodes},{weight}{#nodes,origin,total weight}}
  {{4,7,8}, {3,5,20}, {3}}, //0
  {{6,7}, {1,3}, {2}}, //1
  {{3,7}, {3,5}, {2}}, //2
  {{2,6}, {3,12}, {2}}, //3
  {{0,6}, {3,12}, {2}}, //4
  {{6}, {5}, {1}}, //5
  {{1,3,4,5}, {1,12,12,5}, {4}}, //6
  {{0,1,2}, {5,3,5}, {3}}, //7
  {{0}, {20}, {1}}, //8
};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void bfs(int start, int target) {
  nodes[target][2][1] = -1;
  nodes[target][2][2] = 0;
  int passed = 0;
  int queuelen = 1;
  int queue[] = {target,-1,-1,-1,-1,-1,-1,-1,-1,-1};
  int marked[] = {-1,-1,-1,-1,-1,-1,-1,-1,-1,-1};
  int distance[] = {-1,-1,-1,-1,-1,-1,-1,-1,-1,-1};
  while (queuelen > 0) {
    marked[passed] = queue[0]; //mark node
    //add new nodes to queue
    for (int i=0;i<nodes[queue[0]][2][0];i++) {
      int duplicate = 0;
      int k = queuelen;
      for (int j=0;j<passed;j++) {
        if (marked[j] == nodes[queue[0]][0][i]) {
          duplicate = 1;
          j = passed;
        }
      }
      for (int j=0;j<queuelen;j++) {
        if (queue[j] == nodes[queue[0]][0][i]) {
          if (nodes[queue[j]][2][2] > (nodes[queue[0]][2][2]+nodes[queue[0]][1][i])) {
            k = j;
            queuelen--; //incremented later, so decremented to keep same length
          }
          else {
            duplicate = 1;
          }
          j = queuelen;
        }
      }
      if (duplicate == 0) {
        //normal
        /*
        queue[queuelen] = nodes[queue[0]][0][i];
        //queueorigin[queuelen] = queue[0];
        nodes[nodes[queue[0]][0][i]][2][1] = queue[0];
        queuelen++;
        */
        //weighted
        //path length of indexed node = path lengh of current node+weight of indexed node
        nodes[nodes[queue[0]][0][i]][2][2] = nodes[queue[0]][2][2]+nodes[queue[0]][1][i];
        //origin of indexed node = current node
        nodes[nodes[queue[0]][0][i]][2][1] = queue[0];
        while (nodes[queue[k-1]][2][2] > nodes[nodes[queue[0]][0][i]][2][2]) {
          queue[k] = queue[k-1];
          k--;
        }
        queue[k] = nodes[queue[0]][0][i];
        queuelen++;
      }
    }
    //remove node from queue
    for (int j=0;j<queuelen;j++) {
      queue[j] = queue[j+1];
    }
    queuelen--;
    passed++;
  }
  int route[passed] = {};
  route[0] = start;
  int i = 0;
  //Serial.print(target);
  //Serial.print("\t");
  while (route[i] != target) {
    Serial.print(route[i]);
    Serial.print("(");
    Serial.print(nodes[route[i]][2][1]); 
    Serial.print(")");
    Serial.print("(");
    Serial.print(nodes[route[i]][2][2]);
    Serial.print(")");
    Serial.print("\t");
    route[i+1] = nodes[route[i]][2][1];
    i++;
  }
  Serial.println(route[i]);
}

void loop() {
  // put your main code here, to run repeatedly: 
  bfs(0,2);
  bfs(0,4);
  bfs(0,0);
  while (1) {}
}
