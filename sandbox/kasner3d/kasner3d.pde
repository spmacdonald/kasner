float th = 0;

void setup() {
  size(500, 500, P3D);
  lights();
  fill(200);
}

void draw() {

  float x0 = 2;
  float y0 = 0;
  float z0 = 0;

  float x1 = -1;
  float y1 = sqrt(3);
  float z1 = 0;

  float x2 = -1;
  float y2 = -sqrt(3);
  float z2 = 0;

  float x3 = 0;
  float y3 = 0;
  float z3 = 3;

  translate(width/2, height/2);
  scale(50);
  // float ct = cos(radians(th));
  // float st = sin(radians(th));
  // applyMatrix(  ct, 0.0,  st,  0.0,
               // 0.0, 1.0, 0.0,  0.0,
               // -st, 0.0,  ct,  0.0,
               // 0.0, 0.0, 0.0,  1.0);
  // th += 0.1;
  //
  // rotateY(PI/3);
  // rotateX(PI/3);
  // rotateZ(PI/3);
  sphere(1);
  line(x0, y0, z0, x1, y1, z1);
  line(x0, y0, z0, x2, y2, z2);
  line(x0, y0, z0, x3, y3, z3);
  line(x1, y1, z1, x2, y2, z2);
  line(x1, y1, z1, x3, y3, z3);
  line(x2, y2, z2, x3, y3, z3);

}
